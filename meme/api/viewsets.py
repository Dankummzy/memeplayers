import logging
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from ..models import User, Coin, Vote, Community, Post, Comment, Note, Rating, Badge, UserBadge, Notification, Analytics
from .serializers import UserSerializer, CoinSerializer, VoteSerializer, CommunitySerializer, PostSerializer, CommentSerializer, NoteSerializer, RatingSerializer, BadgeSerializer, UserBadgeSerializer, NotificationSerializer, AnalyticsSerializer

from .permissions import IsAdminUser, IsModeratorOrAdmin, IsOwnerOrReadOnly
from .throttles import VoteThrottle, PostThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination

# Configure logging
logger = logging.getLogger("django")

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

# User ViewSet
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]  # Only Admins can manage users

# Coin ViewSet
class CoinViewSet(viewsets.ModelViewSet):
    queryset = Coin.objects.all()
    serializer_class = CoinSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['name', 'symbol']
    ordering_fields = ['total_votes', 'created_at']

    def get_permissions(self):
        if self.action in ["create", "update", "destroy"]:
            return [IsAdminUser()]  # Only Admins can modify coins
        return [permissions.IsAuthenticated()]  # Authenticated users can view coins

    def perform_destroy(self, instance):
        # Allow only the creator to delete their coin
        if instance.created_by != self.request.user:
            raise PermissionDenied("You cannot delete a coin you did not create.")
        logger.info(f"Coin deleted: {instance.name} by {self.request.user.username}")
        instance.delete()

# Vote ViewSet
class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can vote
    throttle_classes = [VoteThrottle]  # Apply vote throttling

    def perform_create(self, serializer):
        """
        Handles voting and unvoting logic. If the user has already voted on the coin, 
        the vote is removed (unvoted). Otherwise, a new vote is created.
        """
        coin = serializer.validated_data["coin"]
        vote_type = serializer.validated_data["vote_type"]
        user = self.request.user

        # Check if the user has already voted
        existing_vote = Vote.objects.filter(user=user, coin=coin).first()
        if existing_vote:
            if existing_vote.vote_type == vote_type:
                # Unvote if the vote type matches
                existing_vote.delete()
                coin.total_votes -= 1 if vote_type == "upvote" else -1
                logger.info(f"Vote removed: {coin.name} by {user.username}")
            else:
                # Update the vote type
                existing_vote.vote_type = vote_type
                existing_vote.save()
                logger.info(f"Vote updated: {coin.name} by {user.username}")
        else:
            # Create a new vote
            serializer.save(user=user)
            coin.total_votes += 1 if vote_type == "upvote" else -1
            logger.info(f"Vote created: {coin.name} by {user.username}")
        coin.save()

# Community ViewSet
class CommunityViewSet(viewsets.ModelViewSet):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name', 'description']

    def get_permissions(self):
        if self.action in ["update", "destroy"]:
            return [IsModeratorOrAdmin()]  # Moderators or Admins can modify communities
        return [permissions.IsAuthenticated()]  # Authenticated users can view communities

    def perform_create(self, serializer):
        # Automatically set the creator of the community
        community = serializer.save(created_by=self.request.user)
        logger.info(f"Community created: {community.name} by {self.request.user.username}")

# Post ViewSet
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [PostThrottle]  # Apply post throttling
    pagination_class = StandardResultsSetPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at']

    def get_permissions(self):
        if self.action in ["update", "destroy"]:
            return [IsOwnerOrReadOnly()]  # Only post owners can modify or delete posts
        return super().get_permissions()

    def perform_create(self, serializer):
        post = serializer.save(author=self.request.user)
        logger.info(f"Post created: {post.title} by {self.request.user.username}")

    def perform_update(self, serializer):
        post = serializer.save()
        logger.info(f"Post updated: {post.title} by {self.request.user.username}")

    def perform_destroy(self, instance):
        logger.info(f"Post deleted: {instance.title} by {self.request.user.username}")
        instance.delete()

# Comment ViewSet
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = StandardResultsSetPagination

    def get_permissions(self):
        if self.action in ["update", "destroy"]:
            return [IsOwnerOrReadOnly()]  # Only comment owners can modify or delete comments
        return [permissions.IsAuthenticated()]  # Authenticated users can view and create comments

    def perform_create(self, serializer):
        comment = serializer.save(author=self.request.user)
        logger.info(f"Comment created by {self.request.user.username}")

# Note ViewSet
class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Restrict users to their own notes
        return Note.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        note = serializer.save(user=self.request.user)
        logger.info(f"Note created: {note.title} by {self.request.user.username}")

# Rating ViewSet
class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]  # Any authenticated user can rate others

# Badge ViewSet
class BadgeViewSet(viewsets.ModelViewSet):
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer
    permission_classes = [IsAdminUser]  # Only Admins can manage badges

# UserBadge ViewSet
class UserBadgeViewSet(viewsets.ModelViewSet):
    queryset = UserBadge.objects.all()
    serializer_class = UserBadgeSerializer
    permission_classes = [IsAdminUser]  # Only Admins can assign badges

# Notification ViewSet
class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]  # Notifications are private to users

    def get_queryset(self):
        # Restrict notifications to the logged-in user
        return Notification.objects.filter(user=self.request.user)

# Analytics ViewSet
class AnalyticsViewSet(viewsets.ModelViewSet):
    queryset = Analytics.objects.all()
    serializer_class = AnalyticsSerializer
    permission_classes = [IsAdminUser]  # Only Admins can view analytics
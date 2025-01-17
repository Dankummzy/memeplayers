from rest_framework.routers import DefaultRouter
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from .api.viewsets import UserViewSet, CoinViewSet, VoteViewSet, CommunityViewSet, PostViewSet, CommentViewSet, NoteViewSet, RatingViewSet, BadgeViewSet, UserBadgeViewSet, NotificationViewSet, AnalyticsViewSet

router = DefaultRouter()
router.register("users", UserViewSet, basename="user")
router.register("coins", CoinViewSet, basename="coin")
router.register("votes", VoteViewSet, basename="vote")
router.register("communities", CommunityViewSet, basename="community")
router.register("posts", PostViewSet, basename="post")
router.register("comments", CommentViewSet, basename="comment")
router.register("notes", NoteViewSet, basename="note")
router.register("ratings", RatingViewSet, basename="rating")
router.register("badges", BadgeViewSet, basename="badge")
router.register("user-badges", UserBadgeViewSet, basename="userbadge")
router.register("notifications", NotificationViewSet, basename="notification")
router.register("analytics", AnalyticsViewSet, basename="analytics")

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("", include(router.urls)),
]
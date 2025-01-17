from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from meme.models import Coin, Vote, Community, Post, Comment, Note, Rating, Badge, UserBadge, Notification, Analytics

User = get_user_model()

class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123", email="test@example.com")

    def test_user_creation(self):
        self.assertEqual(self.user.username, "testuser")
        self.assertTrue(self.user.check_password("password123"))

class CoinModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123", email="test@example.com")
        self.coin = Coin.objects.create(name="Test Coin", symbol="TC", description="Test Description", category="meme", created_by=self.user)

    def test_coin_creation(self):
        self.assertEqual(self.coin.name, "Test Coin")
        self.assertEqual(self.coin.symbol, "TC")
        self.assertEqual(self.coin.created_by.username, "testuser")

class VoteModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123", email="test@example.com")
        self.coin = Coin.objects.create(name="Test Coin", symbol="TC", description="Test Description", category="meme", created_by=self.user)
        self.vote = Vote.objects.create(user=self.user, coin=self.coin, vote_type="upvote")

    def test_vote_creation(self):
        self.assertEqual(self.vote.user.username, "testuser")
        self.assertEqual(self.vote.coin.name, "Test Coin")
        self.assertEqual(self.vote.vote_type, "upvote")

class CommunityModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123", email="test@example.com")
        self.community = Community.objects.create(name="Test Community", description="Test Description", created_by=self.user)

    def test_community_creation(self):
        self.assertEqual(self.community.name, "Test Community")
        self.assertEqual(self.community.description, "Test Description")
        self.assertEqual(self.community.created_by.username, "testuser")

class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123", email="test@example.com")
        self.post = Post.objects.create(title="Test Post", content="Test Content", author=self.user)

    def test_post_creation(self):
        self.assertEqual(self.post.title, "Test Post")
        self.assertEqual(self.post.content, "Test Content")
        self.assertEqual(self.post.author.username, "testuser")

class CommentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123", email="test@example.com")
        self.post = Post.objects.create(title="Test Post", content="Test Content", author=self.user)
        self.comment = Comment.objects.create(content="Test Comment", author=self.user, post=self.post)

    def test_comment_creation(self):
        self.assertEqual(self.comment.content, "Test Comment")
        self.assertEqual(self.comment.author.username, "testuser")
        self.assertEqual(self.comment.post.title, "Test Post")

class NoteModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123", email="test@example.com")
        self.note = Note.objects.create(user=self.user, title="Test Note", content="Test Content")

    def test_note_creation(self):
        self.assertEqual(self.note.title, "Test Note")
        self.assertEqual(self.note.content, "Test Content")
        self.assertEqual(self.note.user.username, "testuser")

class RatingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123", email="test@example.com")
        self.rated_user = User.objects.create_user(username="rateduser", password="password123", email="rated@example.com")
        self.rating = Rating.objects.create(user=self.user, rated_user=self.rated_user, rating=5, comment="Great user")

    def test_rating_creation(self):
        self.assertEqual(self.rating.user.username, "testuser")
        self.assertEqual(self.rating.rated_user.username, "rateduser")
        self.assertEqual(self.rating.rating, 5)
        self.assertEqual(self.rating.comment, "Great user")

class BadgeModelTest(TestCase):
    def setUp(self):
        self.badge = Badge.objects.create(name="Test Badge", description="Test Description")

    def test_badge_creation(self):
        self.assertEqual(self.badge.name, "Test Badge")
        self.assertEqual(self.badge.description, "Test Description")

class UserBadgeModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123", email="test@example.com")
        self.badge = Badge.objects.create(name="Test Badge", description="Test Description")
        self.user_badge = UserBadge.objects.create(user=self.user, badge=self.badge)

    def test_user_badge_creation(self):
        self.assertEqual(self.user_badge.user.username, "testuser")
        self.assertEqual(self.user_badge.badge.name, "Test Badge")

class NotificationModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123", email="test@example.com")
        self.notification = Notification.objects.create(user=self.user, content="Test Notification")

    def test_notification_creation(self):
        self.assertEqual(self.notification.user.username, "testuser")
        self.assertEqual(self.notification.content, "Test Notification")

class AnalyticsModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123", email="test@example.com")
        self.coin = Coin.objects.create(name="Test Coin", symbol="TC", description="Test Description", category="meme", created_by=self.user)
        self.analytics = Analytics.objects.create(coin=self.coin, views=100, upvotes=50, downvotes=10, total_votes=60)

    def test_analytics_creation(self):
        self.assertEqual(self.analytics.coin.name, "Test Coin")
        self.assertEqual(self.analytics.views, 100)
        self.assertEqual(self.analytics.upvotes, 50)
        self.assertEqual(self.analytics.downvotes, 10)
        self.assertEqual(self.analytics.total_votes, 60)

class UserViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(username="admin", password="admin123", email="admin@example.com", role="admin")
        self.client.force_authenticate(user=self.admin_user)

    def test_create_user(self):
        data = {
            "username": "newuser",
            "password": "password123",
            "email": "newuser@example.com"
        }
        response = self.client.post("/api/users/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.get(id=2).username, "newuser")

class CoinViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(username="admin", password="admin123", email="admin@example.com", role="admin")
        self.client.force_authenticate(user=self.admin_user)
        self.user = User.objects.create_user(username="testuser", password="password123", email="test@example.com")

    def test_create_coin(self):
        data = {
            "name": "New Coin",
            "symbol": "NC",
            "description": "New Coin Description",
            "category": "meme",
            "created_by": self.user.id
        }
        response = self.client.post("/api/coins/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Coin.objects.count(), 1)
        self.assertEqual(Coin.objects.get(id=1).name, "New Coin")

class VoteViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="password123", email="test@example.com")
        self.client.force_authenticate(user=self.user)
        self.coin = Coin.objects.create(name="Test Coin", symbol="TC", description="Test Description", category="meme", created_by=self.user)

    def test_create_vote(self):
        data = {
            "user": self.user.id,
            "coin": self.coin.id,
            "vote_type": "upvote"
        }
        response = self.client.post("/api/votes/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vote.objects.count(), 1)
        self.assertEqual(Vote.objects.get(id=1).vote_type, "upvote")

class CommunityViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="password123", email="test@example.com")
        self.client.force_authenticate(user=self.user)

    def test_create_community(self):
        data = {
            "name": "New Community",
            "description": "New Community Description",
            "members": [self.user.id],  
            "created_by": self.user.id
        }
        response = self.client.post("/api/communities/", data)
        if response.status_code != status.HTTP_201_CREATED:
            print(response.content)  # Print the response content for debugging
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Community.objects.count(), 1)
        self.assertEqual(Community.objects.get(id=1).name, "New Community")

class PostViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="password123", email="test@example.com")
        self.client.force_authenticate(user=self.user)

    def test_create_post(self):
        data = {
            "title": "New Post",
            "content": "New Post Content",
            "author": self.user.id
        }
        response = self.client.post("/api/posts/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.get(id=1).title, "New Post")

class CommentViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="password123", email="test@example.com")
        self.client.force_authenticate(user=self.user)
        self.post = Post.objects.create(title="Test Post", content="Test Content", author=self.user)

    def test_create_comment(self):
        data = {
            "content": "New Comment",
            "author": self.user.id,
            "post": self.post.id
        }
        response = self.client.post("/api/comments/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.get(id=1).content, "New Comment")

class NoteViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="password123", email="test@example.com")
        self.client.force_authenticate(user=self.user)

    def test_create_note(self):
        data = {
            "title": "New Note",
            "content": "New Note Content",
            "user": self.user.id
        }
        response = self.client.post("/api/notes/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Note.objects.count(), 1)
        self.assertEqual(Note.objects.get(id=1).title, "New Note")

class RatingViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="password123", email="test@example.com")
        self.rated_user = User.objects.create_user(username="rateduser", password="password123", email="rated@example.com")
        self.client.force_authenticate(user=self.user)

    def test_create_rating(self):
        data = {
            "user": self.user.id,
            "rated_user": self.rated_user.id,
            "rating": 5,
            "comment": "Great user"
        }
        response = self.client.post("/api/ratings/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Rating.objects.count(), 1)
        self.assertEqual(Rating.objects.get(id=1).rating, 5)

class BadgeViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(username="admin", password="admin123", email="admin@example.com", role="admin")
        self.client.force_authenticate(user=self.admin_user)

    def test_create_badge(self):
        data = {
            "name": "New Badge",
            "description": "New Badge Description"
        }
        response = self.client.post("/api/badges/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Badge.objects.count(), 1)
        self.assertEqual(Badge.objects.get(id=1).name, "New Badge")

class UserBadgeViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(username="admin", password="admin123", email="admin@example.com", role="admin")
        self.client.force_authenticate(user=self.admin_user)
        self.user = User.objects.create_user(username="testuser", password="password123", email="test@example.com")
        self.badge = Badge.objects.create(name="Test Badge", description="Test Description")

    def test_create_user_badge(self):
        data = {
            "user": self.user.id,
            "badge": self.badge.id
        }
        response = self.client.post("/api/user-badges/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UserBadge.objects.count(), 1)
        self.assertEqual(UserBadge.objects.get(id=1).user.username, "testuser")

class NotificationViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="password123", email="test@example.com")
        self.client.force_authenticate(user=self.user)

    def test_create_notification(self):
        data = {
            "content": "New Notification",
            "user": self.user.id
        }
        response = self.client.post("/api/notifications/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Notification.objects.count(), 1)
        self.assertEqual(Notification.objects.get(id=1).content, "New Notification")

class AnalyticsViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(username="admin", password="admin123", email="admin@example.com", role="admin")
        self.client.force_authenticate(user=self.admin_user)
        self.user = User.objects.create_user(username="testuser", password="password123", email="test@example.com")
        self.coin = Coin.objects.create(name="Test Coin", symbol="TC", description="Test Description", category="meme", created_by=self.user)

    def test_create_analytics(self):
        data = {
            "coin": self.coin.id,
            "views": 100,
            "upvotes": 50,
            "downvotes": 10,
            "total_votes": 60
        }
        response = self.client.post("/api/analytics/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Analytics.objects.count(), 1)
        self.assertEqual(Analytics.objects.get(id=1).views, 100)
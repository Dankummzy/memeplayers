from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    '''
    AbstractUser Class for the general model
    '''
    ROLE_CHOICES = [
        ("admin", "Admin"), 
        ("moderator", "Moderator"), 
        ("user", "User")
    ]
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    bio = models.TextField(blank=True)
    activity_points = models.IntegerField(default=0)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="user")
    
    # Adding related_name attributes to avoid conflicts
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='meme_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='meme_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )


class Coin(models.Model):
    '''
    Coin class
    '''
    CATEGORY_CHOICES = [
        ("meme", "Meme"), 
        ("utility", "Utility")
    ]
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="meme")
    logo = models.ImageField(upload_to="coin_logos/", null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_coins")
    created_at = models.DateTimeField(auto_now_add=True)
    total_votes = models.IntegerField(default=0)


class Vote(models.Model):
    '''
    Vote Class
    '''
    VOTE_TYPE_CHOICES = [
        ("upvote", "Upvote"),
        ("downvote", "Downvote")
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="votes")
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE, related_name="votes")
    vote_type = models.CharField(max_length=10, choices=VOTE_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)


class Community(models.Model):
    '''
    Community Class
    '''
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_communities")
    members = models.ManyToManyField(User, related_name="joined_communities")
    created_at = models.DateTimeField(auto_now_add=True)


class Post(models.Model):
    '''
    Post Class
    '''
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    '''
    Comment Class
    '''
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)


class Note(models.Model):
    '''
    Note Class
    '''
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Rating(models.Model):
    '''
    Rating Class
    '''
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ratings_given")
    rated_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ratings_received")
    rating = models.IntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Badge(models.Model):
    '''
    Badge Class
    '''
    name = models.CharField(max_length=50)
    description = models.TextField()
    icon = models.ImageField(upload_to="badges/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class UserBadge(models.Model):
    '''
    User Badge Class
    '''
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="badges")
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    awarded_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
    '''
    Notification Class
    '''
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    content = models.TextField()
    link = models.URLField(null=True, blank=True)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Analytics(models.Model):
    '''
    Analytics Class
    '''
    coin = models.OneToOneField(Coin, on_delete=models.CASCADE, related_name="analytics")
    views = models.IntegerField(default=0)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    total_votes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
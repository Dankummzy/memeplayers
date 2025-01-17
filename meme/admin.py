from django.contrib import admin
from .models import User, Coin, Vote, Community, Post, Comment, Note, Rating, Badge, UserBadge, Notification, Analytics


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'role')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'role')
    ordering = ('username',)

@admin.register(Coin)
class CoinAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol', 'category', 'created_by', 'total_votes', 'created_at')
    search_fields = ('name', 'symbol', 'category')
    list_filter = ('category', 'created_at')
    ordering = ('name',)

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'coin', 'vote_type', 'created_at')
    search_fields = ('user__username', 'coin__name', 'vote_type')
    list_filter = ('vote_type', 'created_at')
    ordering = ('-created_at',)

@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_by', 'created_at')
    search_fields = ('name', 'description', 'created_by__username')
    list_filter = ('created_at',)
    ordering = ('name',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at')
    search_fields = ('title', 'content', 'author__username')
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'author', 'post', 'created_at')
    search_fields = ('content', 'author__username', 'post__title')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at')
    search_fields = ('title', 'content', 'user__username')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'rated_user', 'rating', 'comment', 'created_at')
    search_fields = ('user__username', 'rated_user__username', 'rating', 'comment')
    list_filter = ('rating', 'created_at')
    ordering = ('-created_at',)

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)
    ordering = ('name',)

@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ('user', 'badge', 'created_at')
    search_fields = ('user__username', 'badge__name')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'created_at')
    search_fields = ('user__username', 'content')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

@admin.register(Analytics)
class AnalyticsAdmin(admin.ModelAdmin):
    list_display = ('coin', 'views', 'upvotes', 'downvotes', 'total_votes', 'created_at')
    search_fields = ('coin__name', 'views', 'upvotes', 'downvotes', 'total_votes')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
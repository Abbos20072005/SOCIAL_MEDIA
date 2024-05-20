from django.contrib import admin
from .models import MyUser, Post, CommentPost, LikePost, FollowMyUser


@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')
    list_display_links = ('id', 'user')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'is_published', 'created_at')
    list_display_links = ('id', 'author')


admin.site.register(CommentPost)
admin.site.register(LikePost)
admin.site.register(FollowMyUser)

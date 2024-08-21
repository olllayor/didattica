# urls.py
from django.urls import path

from . import views

urlpatterns = [
    path("", views.post_list, name="post_list"),
    path("api_keys/", views.api_keys, name="api_keys"),
    path("post/<int:post_id>/", views.post_detail, name="post_detail"),
    path("like_post/", views.like_post, name="like_post"),
    path("retweet_post/", views.retweet_post, name="retweet_post"),
    path("hashtag/<str:hashtag_name>/", views.hashtag_posts, name="hashtag_posts"),
    path("ai_chat/", views.ai_chat, name="ai_chat"),
]

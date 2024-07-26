# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('api_keys/', views.api_keys, name='api_keys'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('like_post/<int:post_id>/', views.like_post, name='like_post'),
    path('replied-tweets/<int:post_id>/', views.replied_tweets, name='replied_tweets'),
    path('hashtag/<str:hashtag_name>/', views.hashtag_posts, name='hashtag_posts'),
]

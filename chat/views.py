from django.contrib import messages
import re

from django.contrib.auth.decorators import login_required

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import APIKeyForm, PostForm, ReplyForm
from .models import APIKey, Hashtag, Post
from .upload_image import upload_image_to_telegraph


@login_required
def post_list(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            image_file = request.FILES.get('picture')
            if image_file:
                try:
                    image_url = upload_image_to_telegraph(image_file)
                    post.picture = image_url
                except Exception as e:
                    print('Image upload failed:', e)
                    messages.error(request, 'Failed to upload image. Please try again.')

            post.save()
            

            # Extract hashtags from the post content
            hashtags = re.findall(r'#(\w+)', post.content)
            for tag in hashtags:
                hashtag, created = Hashtag.objects.get_or_create(name=tag)
                post.hashtags.add(hashtag)

            post.save()
            messages.success(request, 'Your post was sent.')
            return redirect('post_list')
        else:
            print('Form is invalid:', form.errors)

    posts = Post.objects.all().order_by('-created_at')
    form = PostForm()
    return render(request, 'chat/post_list.html', {'posts': posts, 'form': form})

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    replies = post.replies.all()
    if request.method == 'POST':
        form = ReplyForm(request.POST, request.FILES)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.post = post
            image_file = request.FILES.get('picture1')
            if image_file:
                try:
                    image_url = upload_image_to_telegraph(image_file)
                    # print("Image URL:", image_url)  # Debugging line
                    reply.picture = image_url
                except Exception as e:
                    print('Image upload failed:', e)
                    messages.error(request, 'Failed to upload image. Please try again.')
            reply.save()
            return redirect('post_detail', post_id=post_id)
    else:
        form = ReplyForm()
    return render(request, 'chat/post_detail.html', {'post': post, 'replies': replies, 'form': form})

@login_required
@require_POST
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return JsonResponse({'total_likes': post.total_likes(), 'liked': liked})


@login_required
def replied_tweets(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    replies = post.replies.all()
    return render(request, 'chat/replied_tweets.html', {'post': post, 'replies': replies})

@login_required
def hashtag_posts(request, hashtag_name):
    hashtag = get_object_or_404(Hashtag, name=hashtag_name)
    posts = hashtag.posts.all().order_by('-created_at')
    return render(request, 'chat/hashtag_posts.html', {'posts': posts, 'hashtag': hashtag})


@login_required
def api_keys(request):
    user = request.user
    api_key, created = APIKey.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        form = APIKeyForm(request.POST, instance=api_key)
        if form.is_valid():
            api_key = form.save(commit=False)
            api_key.user = user
            api_key.save()
            messages.success(request, "API keys saved successfully.")
            return redirect('api_keys')
    else:
        form = APIKeyForm(instance=api_key)

    return render(request, 'chat/api_keys.html', {'form': form})
import json
import re

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import APIKeyForm, PostForm, ReplyForm
from .models import APIKey, Hashtag, Post
from .openai_chat import client, process_stream
from .upload_image import upload_image_to_telegraph
from .utils import check_read_articles, increment_post_views


@login_required
@require_POST
def ai_chat(request):
    data = json.loads(request.body)
    message = data["message"]
    model = data["model"]
    post_id = data["postId"]
    post_content = data["postContent"]
    post_image = data["postImage"]

    api_key = APIKey.objects.get(user=request.user)

    if model == "openai":
        if not api_key.openai_api_key:
            return JsonResponse({"error": "OpenAI API key not set"}, status=400)

        client.api_key = api_key.openai_api_key

        try:
            response = client.chat.completions.create(
                model="gpt-4-vision-preview",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant analyzing a social media post.",
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": f"Analyze this post: {post_content}",
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": post_image,
                                },
                            }
                            if post_image
                            else {},
                        ],
                    },
                    {"role": "user", "content": message},
                ],
                stream=True,
                temperature=0.0,
            )

            ai_response = process_stream(response)
            return JsonResponse({"response": ai_response})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        # Handle other AI models here
        return JsonResponse({"error": "Unsupported AI model"}, status=400)


@login_required
def post_list(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            image_file = request.FILES.get("picture")
            if image_file:
                try:
                    image_url = upload_image_to_telegraph(image_file)
                    post.picture = image_url
                except Exception as e:
                    print("Image upload failed:", e)
                    messages.error(request, "Failed to upload image. Please try again.")

            post.save()

            # Extract hashtags from the post content
            hashtags = re.findall(r"#(\w+)", post.content)
            for tag in hashtags:
                hashtag, created = Hashtag.objects.get_or_create(name=tag)
                post.hashtags.add(hashtag)

            post.save()
            messages.success(request, "Your post was sent.")
            return redirect("post_list")
        else:
            print("Form is invalid:", form.errors)

    posts = Post.objects.all().order_by("-created_at")
    for post in posts:
        post.is_liked = post.likes.filter(id=request.user.id).exists()
    form = PostForm()
    return render(request, "chat/post_list.html", {"posts": posts, "form": form})


@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    increment_post_views(request, post)  # Pass the request object
    replies = post.replies.all()

    if post.id in check_read_articles(request):
        pass
    else:
        check_read_articles(request).append(post.id)

    if request.method == "POST":
        form = ReplyForm(request.POST, request.FILES)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.post = post
            image_file = request.FILES.get("picture1")
            if image_file:
                try:
                    image_url = upload_image_to_telegraph(image_file)
                    reply.picture = image_url
                except Exception as e:
                    print("Image upload failed:", e)
                    messages.error(request, "Failed to upload image. Please try again.")
            reply.save()
            return redirect("post_detail", post_id=post_id)
    else:
        form = ReplyForm()
    return render(
        request,
        "chat/post_detail.html",
        {"post": post, "replies": replies, "form": form},
    )


@login_required
@require_POST
def like_post(request):
    data = json.loads(request.body)
    post_id = data.get("post_id")
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return JsonResponse({"total_likes": post.total_likes(), "liked": liked})


@login_required
@require_POST
def retweet_post(request):
    data = json.loads(request.body)
    post_id = data.get("post_id")
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.retweets.all():
        post.retweets.remove(request.user)
        retweeted = False
    else:
        post.retweets.add(request.user)
        retweeted = True
    return JsonResponse(
        {"total_retweets": post.total_retweets(), "retweeted": retweeted}
    )


@login_required
def hashtag_posts(request, hashtag_name):
    hashtag = get_object_or_404(Hashtag, name=hashtag_name)
    posts = hashtag.posts.all().order_by("-created_at")
    return render(
        request, "chat/hashtag_posts.html", {"posts": posts, "hashtag": hashtag}
    )


@login_required
def api_keys(request):
    user = request.user
    api_key, created = APIKey.objects.get_or_create(user=user)

    if request.method == "POST":
        form = APIKeyForm(request.POST, instance=api_key)
        if form.is_valid():
            api_key = form.save(commit=False)
            api_key.user = user
            api_key.save()
            messages.success(request, "API keys saved successfully.")
            return redirect("api_keys")
    else:
        form = APIKeyForm(instance=api_key)

    return render(request, "chat/api_keys.html", {"form": form})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Reply
from .forms import PostForm, ReplyForm

@login_required
def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'chat/post_list.html', {'posts': posts})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'chat/post_create.html', {'form': form})

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    replies = post.replies.all()
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.post = post
            reply.save()
            return redirect('post_detail', post_id=post_id)
    else:
        form = ReplyForm()
    return render(request, 'chat/post_detail.html', {'post': post, 'replies': replies, 'form': form})

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    # post.likes.add(request.user)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('post_list')
@login_required
def replied_tweets(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    replies = post.replies.all()
    return render(request, 'chat/replied_tweets.html', {'post': post, 'replies': replies})
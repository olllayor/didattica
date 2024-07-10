# chat/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Like, Reply
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
def post_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
    return redirect('post_list')

@login_required
def post_reply(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.post = post
            reply.save()
            return redirect('post_list')
    else:
        form = ReplyForm()
    return render(request, 'chat/post_reply.html', {'form': form, 'post': post})
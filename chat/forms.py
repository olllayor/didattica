from django import forms
from .models import Post, Reply

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'picture']

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content', 'picture']

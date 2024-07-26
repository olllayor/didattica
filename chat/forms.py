from django import forms
from .models import Post, Reply, APIKey

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'picture']

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content', 'picture']

class APIKeyForm(forms.ModelForm):
    class Meta:
        model = APIKey
        fields = ['openai_api_key', 
                  'anthropic_api_key', 
                  'google_gemini_api_key', 
                  'mistral_api_key', 
                  'perplexity_api_key',
                  'together_api_key'
                  ]

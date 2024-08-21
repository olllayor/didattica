from django.contrib.auth.models import User
from django.db import models

ACTION_CHOICES = (
    ("like", "Like"),
    ("save", "Saved"),
    ("view", "View"),
)


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    picture = models.URLField(max_length=1024, blank=True, null=True)
    hashtags = models.ManyToManyField("Hashtag", related_name="posts", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="liked_posts", blank=True)
    retweets = models.ManyToManyField(User, related_name="retweeted_posts", blank=True)
    views = models.PositiveIntegerField(default=0)

    def total_likes(self):
        return self.likes.count()

    def total_retweets(self):
        return self.retweets.count()

    def total_replies(self):
        return self.replies.count()

    def __str__(self):
        return self.content


# class Notification(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     def __str__(self):
#         return f"{self.user.username} - {self.post.content[:20]}"

# class LikedPost(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     def __str__(self):
#         return f"{self.user.username} - {self.post.content[:20]}"


class Hashtag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Reply(models.Model):
    post = models.ForeignKey(Post, related_name="replies", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    picture = models.URLField(max_length=1024, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content


class APIKey(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    openai_api_key = models.CharField(max_length=255, blank=True, null=True)
    anthropic_api_key = models.CharField(max_length=255, blank=True, null=True)
    google_gemini_api_key = models.CharField(max_length=255, blank=True, null=True)
    mistral_api_key = models.CharField(max_length=255, blank=True, null=True)
    perplexity_api_key = models.CharField(max_length=255, blank=True, null=True)
    together_api_key = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s API Keys"

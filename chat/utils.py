def check_read_articles(request):
    try:
        read_articles = request.session["read_articles"]
    except:
        request.session["read_articles"] = []
        read_articles = request.session["read_articles"]
    return read_articles


def increment_post_views(request, post):
    # Get or create a list of viewed post IDs for the current session
    viewed_posts = request.session.get("viewed_posts", [])

    # Check if the post has not been viewed in this session
    if str(post.id) not in viewed_posts:
        post.views += 1
        post.save()

        # Add the post ID to the list of viewed posts
        viewed_posts.append(str(post.id))
        request.session["viewed_posts"] = viewed_posts
        request.session.modified = True

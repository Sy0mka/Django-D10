from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        # Суммарный рейтинг статей автора * 3 (через related_name 'posts')
        post_rating = sum(post.rating * 3 for post in self.posts.all())

        # Суммарный рейтинг комментариев автора
        comment_rating = sum(
            comment.rating
            for comment in
            Comment.objects.filter(user=self.user)
        )

        # Суммарный рейтинг комментариев к статьям автора (через related_name 'comments')
        post_comments_rating = sum(
            comment.rating
            for post in self.posts.all()
            for comment in post.comments.all()
        )

        self.rating = post_rating + comment_rating + post_comments_rating
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    objects = None
    POST_TYPES = [('article', 'Статья'), ('news', 'Новость')]
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='posts'  # Явное указание related_name
    )
    post_type = models.CharField(max_length=7, choices=POST_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        content = str(self.text)
        return content[:124] + '...' if len(content) > 124 else content


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'  # Явное указание related_name
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    objects = models.Manager()  # Явное объявление менеджера

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


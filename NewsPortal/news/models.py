from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from .resources import *
from django.core.cache import cache
from django.utils.translation import gettext as _


class Author(models.Model):
    user_rating = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    def __str__(self):
        return self.user.username

    def update_rating(self):
        sum_post_rate = 0
        sum_auth_comm_rate = 0
        sum_auth_post_comm_rate = 0
        post_rate_query = Post.objects.filter(author_id=self).values('post_rating')
        for d in post_rate_query:
            for k in d.keys():
                sum_post_rate += d[k]
        auth_comm_rate_query = Comment.objects.filter(user_id=self.user_id).values('comment_rating')
        for d in auth_comm_rate_query:
            for k in d.keys():
                sum_auth_comm_rate += d[k]
        post_id_query = Post.objects.filter(author_id=self).values('id')
        for d in post_id_query:
            for k in d.keys():
                cur_post_rating_query = Comment.objects.filter(post_id=d[k]).values('comment_rating')
                for _ in cur_post_rating_query:
                    for i in _.keys():
                        sum_auth_post_comm_rate += _[i]
        self.user_rating = (sum_post_rate * 3) + sum_auth_comm_rate + sum_auth_post_comm_rate
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, related_name='categories')

    def __str__(self):
        return self.name


class Post(models.Model):
    post_time_in = models.DateTimeField(auto_now_add=True)
    post_type = models.CharField(max_length=3,
                                 choices=POSTS,
                                 default=article)
    title = models.CharField(max_length=255)
    post_text = models.TextField(default=_("There is no text yet."))
    post_rating = models.IntegerField(default=0)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    categories = models.ManyToManyField(Category, through='PostCategory',
                                        related_name='post')

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def preview(self):
        return self.post_text[:300] + '...'

    def __str__(self):
        return f'{self.title}: {self.post_text[:124]}'

    def get_absolute_url(self):
        return reverse('post', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'post-{self.pk}')  # затем удаляем его из кэша, чтобы сбросить его


class Comment(models.Model):
    comm_time_in = models.DateTimeField(auto_now_add=True)
    comment_text = models.TextField(default=_("There are no comments yet."))
    comment_rating = models.IntegerField(default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()

    def __str__(self):
        return f'{self.user.username}: {self.comment_text}'


class PostCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.category.name}: {self.post.title}'

# Create your models here.

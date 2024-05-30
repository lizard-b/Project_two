from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user_rating = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def update_rating(self):
        sum_post_rate = Post.objects.filter()
        self.user_rating += 1


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Post(models.Model):  # False - статья, True - новость
    post_time_in = models.DateTimeField(auto_now_add=True)
    post_type = models.BooleanField(default=False)
    title = models.CharField(max_length=255)
    post_text = models.TextField(default="Здесь пока никто ничего не написал.")
    post_rating = models.IntegerField(default=0)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def preview(self):
        return self.post_text[:124] + '...'


class Comment(models.Model):
    comm_time_in = models.DateTimeField(auto_now_add=True)
    comment_text = models.TextField(default="Комментариев пока нет.")
    comment_rating = models.IntegerField(default=0)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()


class PostCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


# Create your models here.

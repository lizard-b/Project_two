from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth import get_user_model
from django_ckeditor_5.fields import CKEditor5Field

User = get_user_model()


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, related_name='category_subscribers')

    def __str__(self):
        return self.name


class Advert(models.Model):
    """
    Модель объявлений
    """

    STATUS_OPTIONS = (
        ('published', 'Опубликовано'),
        ('draft', 'Черновик')
    )

    title = models.CharField(verbose_name='Заголовок', max_length=255)
    slug = models.SlugField(verbose_name='URL', max_length=255, blank=True, unique=True)
    thumbnail = models.ImageField(
        verbose_name='Превью объявления',
        blank=True,
        upload_to='media/images/thumbnails/',
        validators=[FileExtensionValidator(allowed_extensions=('png', 'jpg', 'webp', 'jpeg', 'gif'))]
    )
    content = CKEditor5Field(verbose_name='Содержание объявления', config_name='extends')
    status = models.CharField(choices=STATUS_OPTIONS, default='published', verbose_name='Статус объявления', max_length=10)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время добавления')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время обновления')
    author = models.ForeignKey(Author, verbose_name='Автор', on_delete=models.CASCADE, related_name='author_adverts')
    category = models.ManyToManyField(Category, through='AdvertCategory', related_name='advert_category')

    def __str__(self):
        return f'{self.title}'


# Create your models here.

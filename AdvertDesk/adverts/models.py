from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
from django.core.validators import FileExtensionValidator
from django.contrib.auth import get_user_model
from django_ckeditor_5.fields import CKEditor5Field
from modules.services.utils import unique_slugify

User = get_user_model()


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    class Meta:
        """
        Название модели в админ панели
        """
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

    def __str__(self):
        return self.user.username


class Category(MPTTModel):
    """
    Модель категорий с вложенностью
    """
    name = models.CharField(max_length=255, unique=True, verbose_name='Название категории')
    subscribers = models.ManyToManyField(User, related_name='category_subscribers')
    slug = models.SlugField(max_length=255, verbose_name='URL категории', blank=True)
    description = models.TextField(verbose_name='Описание категории', max_length=300)
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_index=True,
        related_name='children',
        verbose_name='Родительская категория'
    )

    class MPTTMeta:
        """
        Сортировка по вложенности
        """
        order_insertion_by = ('name',)

    class Meta:
        """
        Название модели в админ панели
        """
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('adverts_by_category', kwargs={'slug': self.slug})


class Advert(models.Model):
    """
    Модель объявлений
    """

    class AdvertManager(models.Manager):
        """
        Кастомный менеджер для модели объявлений
        """

        def all(self):
            """
            Список объявлений (SQL запрос с фильтрацией)
            """
            return self.get_queryset().filter(status='published')

    STATUS_OPTIONS = (
        ('published', 'Опубликовано'),
        ('draft', 'Черновик')
    )

    title = models.CharField(verbose_name='Заголовок', max_length=255)
    slug = models.SlugField(verbose_name='URL объявления', max_length=255, blank=True, unique=True)
    thumbnail = models.ImageField(
        verbose_name='Превью объявления',
        blank=True,
        upload_to='media/images/thumbnails/%Y/%m/%d/',
        validators=[FileExtensionValidator(allowed_extensions=('png', 'jpg', 'webp', 'jpeg', 'gif'))]
    )
    content = CKEditor5Field(verbose_name='Содержание объявления', config_name='extends')
    short_content = CKEditor5Field(max_length=500, verbose_name='Краткое содержание объявления', config_name='extends')
    status = models.CharField(choices=STATUS_OPTIONS, default='published', verbose_name='Статус объявления', max_length=10)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время добавления')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время обновления')
    author = models.ForeignKey(Author, verbose_name='Автор', on_delete=models.CASCADE, related_name='author_adverts')
    category = TreeForeignKey('Category', on_delete=models.PROTECT, related_name='adverts_category', verbose_name='Категория')

    objects = AdvertManager()

    class Meta:
        ordering = ['-time_create']
        indexes = [models.Index(fields=['-time_create', 'status'])]
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('adverts_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        """
        Сохранение полей модели при их отсутствии заполнения
        """
        if not self.slug:
            self.slug = unique_slugify(self, self.title)
        super().save(*args, **kwargs)


class Response(models.Model):
    time_create = models.DateTimeField(auto_now_add=True)
    response_text = models.TextField(default="There is no response yet.")
    advert = models.ForeignKey(Advert, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='advert_response')

    class Meta:
        """
        Название модели в админ панели
        """
        verbose_name = 'Отклик'
        verbose_name_plural = 'Отклики'

    def __str__(self):
        return f'{self.user.username}: {self.response_text}'


# Create your models here.

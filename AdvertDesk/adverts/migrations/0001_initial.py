# Generated by Django 5.1 on 2024-08-26 13:19

import django.core.validators
import django.db.models.deletion
import django_ckeditor_5.fields
import mptt.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Автор',
                'verbose_name_plural': 'Авторы',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Название категории')),
                ('slug', models.SlugField(blank=True, max_length=255, verbose_name='URL категории')),
                ('description', models.TextField(max_length=300, verbose_name='Описание категории')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='adverts.category', verbose_name='Родительская категория')),
                ('subscribers', models.ManyToManyField(related_name='category_subscribers', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Advert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок')),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True, verbose_name='URL объявления')),
                ('thumbnail', models.ImageField(blank=True, upload_to='media/images/thumbnails/%Y/%m/%d/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=('png', 'jpg', 'webp', 'jpeg', 'gif'))], verbose_name='Превью объявления')),
                ('content', django_ckeditor_5.fields.CKEditor5Field(verbose_name='Содержание объявления')),
                ('short_content', django_ckeditor_5.fields.CKEditor5Field(max_length=500, verbose_name='Краткое содержание объявления')),
                ('status', models.CharField(choices=[('published', 'Опубликовано'), ('draft', 'Черновик')], default='published', max_length=10, verbose_name='Статус объявления')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Время добавления')),
                ('time_update', models.DateTimeField(auto_now=True, verbose_name='Время обновления')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_adverts', to='adverts.author', verbose_name='Автор')),
                ('category', mptt.fields.TreeForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='adverts_category', to='adverts.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Объявление',
                'verbose_name_plural': 'Объявления',
                'ordering': ['-time_create'],
            },
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_create', models.DateTimeField(auto_now_add=True)),
                ('response_text', models.TextField(default='There is no response yet.')),
                ('advert', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adverts.advert')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='advert_response', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Отклик',
                'verbose_name_plural': 'Отклики',
            },
        ),
        migrations.AddIndex(
            model_name='advert',
            index=models.Index(fields=['-time_create', 'status'], name='adverts_adv_time_cr_eeaadc_idx'),
        ),
    ]

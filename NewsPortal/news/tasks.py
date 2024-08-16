from django.utils import timezone
from celery import shared_task

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from django.conf import settings
from .models import *


@shared_task()
def notify_about_new_post(oid):
    post = Post.objects.get(pk=oid)
    categories = set(Post.objects.filter(pk=oid).values_list('categories__name', flat=True))
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers__email',
                                                                               'subscribers__username'))
    for subscriber in subscribers:
        html_content = render_to_string(
            'post_created_email.html',
            {
                'username': subscriber[1],
                'text': post.preview(),
                'link': f'{settings.SITE_URL}/news/{post.id}',
            }
        )

        msg = EmailMultiAlternatives(
            subject=post.title,
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[subscriber[0]],

        )

        msg.attach_alternative(html_content, 'text/html')
        msg.send()


@shared_task()
def posts_weekly_notification():
    today = timezone.now()
    last_week = today - timezone.timedelta(days=7)
    posts = Post.objects.filter(post_time_in__gte=last_week)
    categories = set(posts.values_list('categories__name', flat=True))
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))

    html_content = render_to_string('cat_weekly_posts.html', {
        'link': settings.SITE_URL,
        'posts': posts, }
    )

    msg = EmailMultiAlternatives(
        subject='Статьи в любимой категории за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

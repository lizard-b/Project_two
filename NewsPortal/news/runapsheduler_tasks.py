from django.utils import timezone
from NewsPortal.news.models import Post, Category
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMultiAlternatives


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

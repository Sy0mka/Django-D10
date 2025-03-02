from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import Post
from datetime import timedelta
from django.utils import timezone

@shared_task
def send_notification(post_id):
    post = Post.objects.get(id=post_id)
    for category in post.categories.all():
        for subscriber in category.subscribers.all():
            html_content = render_to_string('email/new_post.html', {
                'post': post,
                'user': subscriber
            })
            send_mail(
                subject=post.title,
                message='',
                from_email='noreply@newsportal.com',
                recipient_list=[subscriber.email],
                html_message=html_content
            )

@shared_task
def weekly_digest():
    from .models import Category
    for category in Category.objects.all():
        subscribers = category.subscribers.all()
        if subscribers:
            posts = category.post_set.filter(
                created_at__gte=timezone.now() - timedelta(days=7)
            )
            if posts.exists():
                html_content = render_to_string('email/weekly_digest.html', {
                    'category': category,
                    'posts': posts
                })
                send_mail(
                    subject=f'Еженедельная рассылка: {category.name}',
                    message='',
                    from_email='noreply@newsportal.com',
                    recipient_list=[sub.email for sub in subscribers],
                    html_message=html_content
                )
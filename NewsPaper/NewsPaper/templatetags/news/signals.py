from .tasks import send_notification

@receiver(post_save, sender=Post)
def notify_subscribers(sender, instance, created, **kwargs):
    if created and instance.post_type == 'news':
        send_notification.delay(instance.id)
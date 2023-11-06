from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Post
from django.db.models.signals import post_save, m2m_changed

from .tasks import new_post_subscription


#@receiver(post_save, sender=Post)
@receiver(m2m_changed, sender=Post.category.through)
def article_create(instance, sender, **kwargs):
    new_post_subscription(instance)

    #if not created:
    #    return

    '''
    emails = User.objects.filter(
        subscriptions__category=instance.category
    ).values_list('email', flat=True)

    subject = f'New post to category {instance.category}'

    text_content = (
        f'Title: {instance.name}\n'
        #f'Цена: {instance.price}\n\n'
        f'Urls to post: http://127.0.0.1:8000{instance.get_absolute_url()}'
    )
    html_content = (
        f'Title: {instance.name}<br>'
        #f'Цена: {instance.price}<br><br>'
        f'<br><a href="http://127.0.0.1{instance.get_absolute_url()}">'
        f'Urls to post</a>'
    )
    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()'''

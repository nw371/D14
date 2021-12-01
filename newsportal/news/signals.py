from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Post, PostCategory, CategorySub
from .secda import admail #файл с личной инфо исключён из гит



# @receiver(post_save, sender=Post)
# def notify_subscribers_publication(instance, created, **kwargs):
#     if not created:
#         subject = f'Изменена публикация: {instance.name} {instance.date.strftime("%d %m %Y")}'
#         dcat_id = list(PostCategory.objects.filter(post_id=instance.id).values('category_id'))
#         lcat_id = [d['category_id'] for d in dcat_id]
#         for cat_id in lcat_id:
#             filtered_susbscrbrs = list(CategorySub.objects.filter(category_id=cat_id).values('subscriber_id__user__email'))
#             list_of_subscribers = [d['subscriber_id__user__email'] for d in filtered_susbscrbrs if 'subscriber_id__user__email' in d]
#             pub_updates = render_to_string('email/pub_updates.html', {'post': instance, 'instance': instance.id})
#             send_updates(subject, pub_updates, list_of_subscribers)
#
# @receiver(m2m_changed, sender=Post.category.through)
# def notify_subscribers_publication(instance, **kwargs):
#     subject = f'Добавлена публикация: {instance.name} {instance.date.strftime("%d %m %Y")}'
#     dcat_id = list(kwargs.get('pk_set'))
#     for cat_id in dcat_id:
#         filtered_susbscrbrs = list(CategorySub.objects.filter(category_id=cat_id).values('subscriber_id__user__email'))
#         list_of_subscribers = [d['subscriber_id__user__email'] for d in filtered_susbscrbrs if 'subscriber_id__user__email' in d]
#         pub_updates = render_to_string('email/pub_updates.html', {'post': instance, 'instance': instance.id})
#         #send_updates(subject, pub_updates, list_of_subscribers)
#         article_created(subject, pub_updates, list_of_subscribers)


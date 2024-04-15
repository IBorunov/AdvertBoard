from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.core.mail import send_mail
from Advert_Board.settings import DEFAULT_FROM_EMAIL
from .models import Notification

"""Сигналы для отправки уведомлений всем пользователям.
 Легко настроить под конкретные нужды, добавив новые функции
 (напр. notify_admins, managers etc)"""
@receiver(post_save, sender=Notification)
def notify_all_users(sender, instance, created, **kwargs):
    if created:
        recipient_emails = []
        recipients = User.objects.all()
        for recipient in recipients:
            recipient_emails += [recipient.email]
        subject = instance.title
        message = instance.text

        send_mail(subject=subject, message=message, from_email=DEFAULT_FROM_EMAIL, recipient_list=recipient_emails)

post_save.connect(notify_all_users, sender=Notification)
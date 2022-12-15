from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from allauth.account.signals import email_confirmed
from django.shortcuts import get_object_or_404

from .models import Resp, Advert
from .tasks import mail_for_add_response, mail_for_change_status


@receiver(email_confirmed)
def email_confirmed_(request, email_address, **kwargs):
    """По факту подтверждения email делаем пользователя активным
    и выдаем права staff - нужно для загрузки файлов в ckeditor"""
    user = User.objects.get(email=email_address.email)
    user.is_staff = True
    user.is_active = True
    user.save()


@receiver(post_save, sender=Resp)
def add_response(sender, instance, created, *args, **kwargs):
    # Добавляем задание на отправку письма по факту добавления отклика
    if created:
        adv_pk = instance.post_id
        adv = get_object_or_404(Advert, pk=adv_pk)
        mail_for_add_response.apply_async(
            (adv.author.username, adv.author.email, adv.title),
            countdown=30,
        )
    # Добавляем задание на отправку письма по факту принятия отклика
    elif kwargs.get('update_fields'):
        mail_for_change_status.apply_async(
            (instance.author.username, instance.author.email),
            countdown=30,
        )
    return

from datetime import timedelta

from allauth.account.models import EmailAddress
from celery import shared_task

from django.template.loader import render_to_string
from django.utils import timezone

from .utilites import send_mail
from .models import User, Advert


@shared_task
def mail_for_add_response(username, email, title):
    """Отправка письма после добавления отклика"""
    html_content = render_to_string(
        'email/added_response.html',
        {
            'name': username,
            'title': title,
        }
    )
    subject = f'{username}, на объявление "{title}" появился новый отклик'
    send_mail(email, subject, html_content)
    return


@shared_task
def mail_for_change_status(username, email):
    """Отправка письма после принятия отклика"""
    html_content = render_to_string(
        'email/response_accepted.html',
        {
            'name': username,
        }
    )
    subject = f'{username}, ваш отклик принят'
    send_mail(email, subject, html_content)
    return


@shared_task
def periodic_mailing():
    """Ежесуточная рассылка новостей"""

    # Создаем список рассылки из пользователей с подтвержденным email
    mailing_list = []
    users = User.objects.all()
    emails = EmailAddress.objects.filter(verified=True).values_list('user_id', 'email')
    for id, email in emails:
        username = users.get(pk=id).username
        mailing_list.append((username, email))

    # Проверяем наличие объявлений за прошедшие сутки и отправляем письма
    last_day = timezone.now() - timedelta(days=1)
    adv = Advert.objects.filter(create__gte=last_day)
    if adv.exists():
        for recipient in mailing_list:
            html_content = render_to_string(
                'email/daily_mailing.html',
                {
                    'link': 'http://127.0.0.1:8000',
                    'name': recipient[0],
                    'adverts': adv
                }
            )
            subject = f'{recipient[0]}, новые объявления'
            send_mail(recipient[1], subject, html_content)

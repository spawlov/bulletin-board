from django.conf import settings
from django.core import mail

from loguru import logger


def send_mail(email: str, subject: str, html: any) -> None:
    connection = None
    try:
        connection = mail.get_connection()
        connection.open()
        message = mail.EmailMultiAlternatives(
            subject=subject,
            from_email=settings.EMAIL,
            to=[email],
            connection=connection,
        )
        message.attach_alternative(html, 'text/html')
        message.send()
    except Exception as e:
        logger.error(f'Task mailing added response :: {e}')
    finally:
        connection.close()

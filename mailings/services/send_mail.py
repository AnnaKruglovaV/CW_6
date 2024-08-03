import datetime
import smtplib

from django.conf import settings
from django.core.mail import send_mail

from mailings.models import MailingSettings, Log


def send_email(message_settings, message_client):
    try:
        send_mail(
            subject=message_settings.title,
            message=message_settings.text,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[message_client.email],
            fail_silently=False,
        )

        Log.objects.create(
            time=datetime.datetime.now(datetime.timezone.utc),
            status="Успешно",
            mailing_list=message_settings,
            client=message_client,
        )
    except smtplib.SMTPException as e:
        Log.objects.create(
            time=datetime.datetime.now(datetime.timezone.utc),
            status="Ошибка",
            server_response=str(e),
            mailing_list=message_settings,
            client=message_client,
        )


def send_mails():
    datetime_now = datetime.datetime.now(datetime.timezone.utc)
    for mailing_setting in MailingSettings.objects.filter(status=MailingSettings.STARTED):

        if (datetime_now > mailing_setting.start_time) and (datetime_now < mailing_setting.end_time):

            for mailing_client in mailing_setting.client.all():
                mailing_log = Log.objects.filter(
                    client=mailing_client.pk,
                    mailing_list=mailing_setting
                )

                if mailing_log.exists():
                    last_try_date = mailing_log.order_by('-time').first().time

                    if mailing_setting.periodicity == MailingSettings.DAILY:
                        if (datetime_now - last_try_date).days >= 1:
                            send_email(mailing_setting, mailing_client)
                    elif mailing_setting.periodicity == MailingSettings.WEEKLY:
                        if (datetime_now - last_try_date).days >= 7:
                            send_email(mailing_setting, mailing_client)
                    elif mailing_setting.periodicity == MailingSettings.MONTHLY:
                        if (datetime_now - last_try_date).days >= 30:
                            send_email(mailing_setting, mailing_client)
                else:
                    send_email(mailing_setting, mailing_client)

from EducationalPortal.celery import app
from django.core.mail import send_mail

from courses.models import Contact


@app.task
def send_spam_email(email):
    send_mail('Вы подписались на рассылку', 'Наш сайт будет вас уведомлять о новых курсов и фичах сайта',
              'educationalplatform11@gmail.com', [email],
              fail_silently=False)


@app.task
def send_beat_email(email):
    for contact in Contact.objects.all():
        send_mail('Образовательный проект', 'Возвращайся на сайт, тебя ждут новые курсы!',
                  'educationalplatform11@gmail.com', [contact.email],
                  fail_silently=False)

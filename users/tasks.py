from EducationalPortal.celery import app
from django.core.mail import send_mail


@app.task
def send_email_password(message, email):
    send_mail('Сброс пароля', message, 'educationalplatform11@gmail.com', [email], fail_silently=False)

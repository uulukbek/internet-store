
from django.core.mail import send_mail
from main.celery import app


@app.task
def send_confirmation_email(email, code):
    link = f'http://localhost:8000/account/activate/{code}'
    send_mail(
        'Актвационный код',
         link,
        'ulanovulukbek2@gmail.com',
        [email]
    )


@app.task
def send_confirmation_code(email, code):
    send_mail(
        'Password recovery',
        f'Copy this code -> {code}',
        'ulanovulukbek2@gmail.com',
        [email],
    )
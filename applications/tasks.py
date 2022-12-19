from django.core.mail import send_mail
from main.celery import app


@app.task
def send_confirmation_email_celery(email, code):
    full_link = f"http://localhost:8000/shop/activate/{code}"
    send_mail(
        "User activation",
        f"Here is your code: {full_link}",
        "sabyrkulov.nurmuhammed@gmail.com",
        [email]
    )


@app.task
def send_confirmation_code_celery(email, confirm_code):
    send_mail(
        "Password recovery",
        f"Here is your recovery code: {confirm_code}",
        "sabyrkulov.nurmuhammed@gmail.com",
        [email]
    )
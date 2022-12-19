from django.core.mail import send_mail
from main.celery import app


@app.task
def send_order_confirm(email, order_code):
    full_link = f'http://localhost:8000/notebook/buy/{order_code}'
    send_mail(
        'Order confirmation',
        f'Tap this to confirm your order-> {full_link}',
        'ulanovulukbek2@gmail.com',
        [email],
    )
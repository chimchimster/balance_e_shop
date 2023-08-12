from balance.celery import app
from django.core.mail import send_mail
from .models import Order


# @app.task
def order_created(order_id):
    order = Order.objects.get(id=order_id)
    subject = f'Номер заказа {order.id}'
    message = f'Уважаемый {order.first_name}\n' \
              f'Вы успешно создали заказ!\n' \
              f'Номер вашего заказа {order.id}.'

    mail_sent = send_mail(
        subject,
        message,
        'admin@shop.com',
        [order.email],
    )

    return mail_sent
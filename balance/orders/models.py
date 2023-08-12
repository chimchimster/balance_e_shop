from django.db import models
from decimal import Decimal
from shop.models import Product
from django.core.validators import MinValueValidator, MaxValueValidator
from coupons.models import Coupon


class Order(models.Model):
    first_name = models.CharField(
        max_length=50,
        verbose_name='Имя',
    )
    last_name = models.CharField(
        max_length=50,
        verbose_name='Фамилия',
    )
    email = models.EmailField(
        verbose_name='Почта',
    )
    address = models.CharField(
        max_length=250,
        verbose_name='Адрес',
    )
    postal_code = models.CharField(
        max_length=20,
        verbose_name='Почтовый индекс',
    )
    city = models.CharField(
        max_length=100,
        verbose_name='Город',
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата изменения',
    )
    paid = models.BooleanField(
        default=False,
        verbose_name='Оплачено',
    )

    coupon = models.ForeignKey(
        Coupon,
        related_name='orders',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='Купон',
    )

    discount = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name='Скидка',
    )

    class Meta:
        ordering = ('-created',)
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'Заказ {self.pk}'

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())

        return total_cost - total_cost * (self.discount / Decimal('100'))


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE,
        verbose_name='Заказ',
    )
    product = models.ForeignKey(
        Product,
        related_name='order_items',
        on_delete=models.CASCADE,
        verbose_name='Товар',
    )
    price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Цена',
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name='Количество'
    )

    def __str__(self):
        return f'{self.pk}'

    def get_cost(self):
        return self.price * self.quantity
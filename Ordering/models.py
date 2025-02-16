from django.db import models

from Account.models import User
from Rent.models import RentDay, Rent, RentSize
from product.models import Product, Size


# Create your models here.

class Ordering(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    is_paid = models.BooleanField(verbose_name='پرداخت شده/نشده', default=False)
    date = models.DateField(verbose_name='تاریخ پرداخت', null=True, blank=True)

    def __str__(self):
        return str(self.user)

    def calculate_total_price(self):
        total = 0
        item_prices = {}
        for detail in self.orderingitem_set.all():
            if self.is_paid:
                item_price = detail.total_price

            else:
                item_price = detail.product.price * detail.total_quantity
            item_prices[detail.id] = int(item_price)
            total += int(item_price)
        return item_prices, total

    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبدهای خرید'


class OrderingItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    order = models.ForeignKey(Ordering, on_delete=models.CASCADE, verbose_name='سبد خرید')
    total_price = models.IntegerField(verbose_name='قیمت نهایی', null=True, blank=True)
    total_quantity = models.IntegerField(verbose_name='تعداد')
    size = models.ForeignKey(Size, on_delete=models.CASCADE, verbose_name='سایز', null=True, blank=True)

    def __str__(self):
        return str(self.order)

    class Meta:
        verbose_name = 'جزئیات خرید'
        verbose_name_plural = 'جزئیات خریدها'


class OrderingRent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    is_paid = models.BooleanField(verbose_name='پرداخت شده/نشده', default=False)
    date = models.DateField(verbose_name='تاریخ پرداخت', null=True, blank=True)

    def __str__(self):
        return str(self.user)

    def calculate_total_rent_price(self):
        total = 0
        item_prices = {}

        for detail in self.orderingrentitem_set.all():
            if self.is_paid:
                if detail.day.id == 1:
                    item_price = detail.total_price
                elif detail.day.id == 2:
                    item_price = detail.total_price * 5
                elif detail.day.id == 3:
                    item_price = detail.total_price * 18
                else:
                    item_price = detail.total_price * 25
            else:
                if detail.day.id == 1:
                    item_price = detail.product.price * detail.total_quantity
                elif detail.day.id == 2:
                    item_price = detail.product.price * detail.total_quantity * 5
                elif detail.day.id == 3:
                    item_price = detail.product.price * detail.total_quantity * 18
                else:
                    item_price = detail.product.price * detail.total_quantity * 25

            item_prices[detail.id] = int(item_price)
            total += int(item_price)
        return item_prices, total

    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبدهای خرید'


class OrderingRentItem(models.Model):
    product = models.ForeignKey(Rent, on_delete=models.CASCADE, verbose_name='محصول')
    order = models.ForeignKey(OrderingRent, on_delete=models.CASCADE, verbose_name='سبد خرید')
    total_price = models.IntegerField(verbose_name='قیمت نهایی', null=True, blank=True)
    total_quantity = models.IntegerField(verbose_name='تعداد')
    day = models.ForeignKey(RentDay, on_delete=models.CASCADE, verbose_name='روز', null=True, blank=True)
    size = models.ForeignKey(RentSize, on_delete=models.CASCADE, verbose_name='سایز', null=True, blank=True)

    def __str__(self):
        return str(self.order)

    class Meta:
        verbose_name = 'جزئیات خرید'
        verbose_name_plural = 'جزئیات خریدها'

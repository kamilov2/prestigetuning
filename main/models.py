import uuid
import requests
from decimal import Decimal
from django.db import models
from django.utils.translation import gettext_lazy as _

def get_usd_to_uzs_rate():
    try:
        url = "https://cbu.uz/uz/arkhiv-kursov-valyut/json/"
        response = requests.get(url)
        response.raise_for_status()  # Проверка на ошибки HTTP
        data = response.json()
        for currency in data:
            if currency['Ccy'] == 'USD':
                return Decimal(currency['Rate'])
    except (requests.RequestException, ValueError, KeyError, Decimal.InvalidOperation) as e:
        print(f"Ошибка при получении или обработке курса USD: {e}")
    return Decimal('0.00')  

def generate_unique_category_id():
    return str(uuid.uuid4()).replace('-', '')

class Banner(models.Model):
    name = models.CharField(max_length=200, db_index=True, verbose_name=_('Название'))
    description = models.TextField(blank=True, verbose_name=_('Описание'))
    ceiling = models.PositiveIntegerField(verbose_name=_('Потолок'))
    image = models.ImageField(upload_to='banners/%Y/%m/%d', blank=True, verbose_name=_('Изображение'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создания'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Дата обновления'))

    class Meta:
        ordering = ('name',)
        verbose_name = _('Баннер')
        verbose_name_plural = _('Баннеры')

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True, verbose_name=_('Название'))
    category_id = models.CharField(max_length=300, unique=True, default=generate_unique_category_id, editable=False, verbose_name=_('ID категории'))
    category_image = models.ImageField(upload_to='categories/%Y/%m/%d', blank=True, verbose_name=_('Изображение категории'))

    class Meta:
        ordering = ('name',)
        verbose_name = _('Категория')
        verbose_name_plural = _('Категории')

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=200, db_index=True, verbose_name=_('Название'))

    class Meta:
        ordering = ('name',)
        verbose_name = _('Бренд')
        verbose_name_plural = _('Бренды')

    def __str__(self):
        return self.name

class CarModel(models.Model):
    name = models.CharField(max_length=200, db_index=True, verbose_name=_('Название'))

    class Meta:
        ordering = ('name',)
        verbose_name = _('Марка автомобиля')
        verbose_name_plural = _('Марки автомобилей')

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey('Category', related_name='products', on_delete=models.CASCADE, verbose_name=_('Категория'))
    brand = models.ForeignKey('Brand', related_name='products', on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('Бренд'))
    car_model = models.ForeignKey('CarModel', related_name='products', on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('Марка автомобиля'))
    name = models.CharField(max_length=200, db_index=True, verbose_name=_('Название'))
    description = models.TextField(blank=True, verbose_name=_('Описание'))
    usd_price = models.DecimalField(verbose_name=_('Цена в USD'), max_digits=15, decimal_places=2, blank=True, null=True)
    uzs_price = models.DecimalField(verbose_name=_('Цена в UZS'), max_digits=15, decimal_places=2, blank=True, null=True)
    ceiling_price = models.DecimalField(verbose_name=_('Цена до скидки'), max_digits=15, decimal_places=2, blank=True, null=True, default=0)
    image_1 = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, verbose_name=_('Изображение 1'))
    image_2 = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, verbose_name=_('Изображение 2'))
    image_3 = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, verbose_name=_('Изображение 3'))
    image_4 = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, verbose_name=_('Изображение 4'))
    sell_count = models.PositiveIntegerField(default=0, verbose_name=_('Количество продаж'))
    count_in_stock = models.PositiveIntegerField(default=0, verbose_name=_('Количество в наличии'), editable=False)
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создания'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Дата обновления'))

    def save(self, *args, **kwargs):
        try:
            if self.usd_price and not self.uzs_price:
                usd_to_uzs_rate = get_usd_to_uzs_rate()
                if usd_to_uzs_rate:
                    self.uzs_price = self.usd_price * usd_to_uzs_rate
            elif self.uzs_price and not self.usd_price:
                usd_to_uzs_rate = get_usd_to_uzs_rate()
                if usd_to_uzs_rate:
                    self.usd_price = self.uzs_price / usd_to_uzs_rate
        except Decimal.InvalidOperation as e:
            print(f"Ошибка в методе save: {e}")
        super().save(*args, **kwargs)



    class Meta:
        ordering = ('name',)
        verbose_name = _('Товар')
        verbose_name_plural = _('Товары')
        index_together = (('id', 'name'),)

    def __str__(self):
        return self.name
    
class Order(models.Model):
    full_name = models.CharField(max_length=150, verbose_name=_('ФИО'))
    phone_number = models.CharField(max_length=20, verbose_name=_('Номер телефона'))
    address = models.CharField(max_length=250, blank=True, verbose_name=_('Адрес'))
    city = models.CharField(max_length=200, blank=True, verbose_name=_('Город'))
    village = models.CharField(max_length=100, blank=True, verbose_name=_('Посёлок'))
    street = models.CharField(max_length=100, blank=True, verbose_name=_('Улица'))
    home_number = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Дом'))
    delivery_status = models.BooleanField(default=False, verbose_name=_('Статус доставки'))
    message_for_delivery = models.TextField(blank=True, verbose_name=_('Сообщение для доставки'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создания'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Дата обновления'))

    class Meta:
        ordering = ('-created',)
        verbose_name = _('Заказ')
        verbose_name_plural = _('Заказы')

    def __str__(self):
        return f'Заказ {self.id}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name=_('Заказ'))
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE, verbose_name=_('Товар'))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Цена'))
    quantity = models.PositiveIntegerField(default=1, verbose_name=_('Количество'))

    class Meta:
        verbose_name = _('Позиция заказа')
        verbose_name_plural = _('Позиции заказа')

    def __str__(self):
        return f'Позиция заказа {self.id}'

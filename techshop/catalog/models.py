from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg
from django.core.validators import MinValueValidator, MaxValueValidator


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    address = models.CharField(max_length=256,  verbose_name='Адрес')

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.user

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Product(models.Model):
    name = models.CharField(max_length=256, db_index=True, verbose_name='Товар')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    image = models.ImageField(upload_to='images/products', blank=True, null=True, default='images/products/placeholder.jpg')
    state_price = models.IntegerField(default=0, verbose_name='Базовая цена')
    price = models.IntegerField(default=0, verbose_name='Цена')
    rating = models.DecimalField(max_digits=5, decimal_places=1, default=0.0, verbose_name='Рейтинг')
    numReviews = models.IntegerField(default=0, verbose_name='Кол-во оценок')
    discount = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name='Скидка')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='product', verbose_name='Категория')
    producer = models.ForeignKey('Producer', on_delete=models.CASCADE, verbose_name='Производитель',
                                 related_name='product')
    inStock = models.BooleanField(default=False, verbose_name='В наличии')
    subscribers = models.ManyToManyField(User, through='UserProduct', related_name='product_subscribers')

    def get_absolute_url(self):
        return f'/{self.id}'

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class UserProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)


class Filial(models.Model):
    name = models.CharField(max_length=128, verbose_name='Наименование филиала')
    address = models.CharField(max_length=256, verbose_name='Адрес')
    products = models.ManyToManyField(Product, through='ProductFilial', verbose_name='Товар', related_name='filial')

    class Meta:
        verbose_name = 'Филиал'
        verbose_name_plural = 'Филиалы'

    def __str__(self):
        return self.name


class ProductFilial(models.Model):
    amount = models.IntegerField(default=0, verbose_name='Количество товара на складе')
    filial = models.ForeignKey(Filial, on_delete=models.CASCADE, verbose_name='Филиал', related_name='product_filials')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар', related_name='product_filials')

    class Meta:
        verbose_name = 'Филиал товара'
        verbose_name_plural = 'Филиалы товара'

    def __str__(self):
        return f'{self.product.name}'


class Category(models.Model):
    name = models.CharField(max_length=128, verbose_name='Название категории')
    image = models.ImageField(upload_to='images/category', blank=True, null=True, default='images/products/placeholder.jpg')
    subscribers = models.ManyToManyField(User, through='UserCategory', related_name='subscribers')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/category/{self.id}'


class UserCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)


class Producer(models.Model):
    name = models.CharField(max_length=128, verbose_name='Производитель')
    description = models.CharField(max_length=512, null=True, blank=True, verbose_name='Описание производителя')
    logo = models.ImageField(upload_to='images/producer', blank=True, null=True, default='images/producer/placeholder.jpg')

    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'

    def __str__(self):
        return self.name


class Order(models.Model):
    CHOICES = (
        ('самовывоз', 'Самовывоз'), ('курьер', 'Курьер'), ('почта', 'Почта'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    first_name = models.CharField(max_length=50, default='name', verbose_name='Имя')
    last_name = models.CharField(max_length=50, default='lastname', verbose_name='Фамилия')
    address = models.CharField(max_length=200, default='lastname', verbose_name='Адрес')
    paymentMethod = models.CharField(max_length=200, null=True, blank=True, verbose_name='Способ оплаты')
    order_data = models.DateField(auto_now_add=True, verbose_name='Дата заказа')
    status = models.BooleanField(default=False, verbose_name='Статус заказа')
    quantity = models.IntegerField(default=0, verbose_name='Количество')
    delivery = models.CharField(max_length=128, choices=CHOICES, default='Самовывоз', verbose_name='Доставка')
    comment = models.CharField(max_length=512, null=True, blank=True, verbose_name='Комментарий')
    products = models.ManyToManyField(Product, through='ProductOrder', related_name='order')

    class Meta:
        ordering = ('-order_data',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def get_absolute_url(self):
        return f'/order/{self.id}'

    def __str__(self):
        return 'Заказ {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class ProductOrder(models.Model):
    amount = models.IntegerField(default=1, verbose_name='Количество товара')
    price = models.FloatField(default=0.0, verbose_name='Стоимость')
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='items', verbose_name='Заказ')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='order_items', verbose_name='Товар')

    def get_cost(self):
        return self.price * self.amount

    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказа'

    def __str__(self):
        return f'{self.order.id} \
                 {self.product.name}\
                 {self.amount} \
                 {self.price}'


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='user_comments')
    rating = models.IntegerField(null=True, blank=True, default=0, verbose_name='Рейтинг')
    com_text = models.TextField(verbose_name='Текст комментария')
    com_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата комментария')

    def get_absolute_url(self):
        return f'/comment/{self.id}'

    def __str__(self):
        return 'Комментарий {} и оценка {}'.format(self.user, self.rating)

    class Meta:
        ordering = ["-com_date"]
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'







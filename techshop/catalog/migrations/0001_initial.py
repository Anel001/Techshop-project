# Generated by Django 4.2 on 2023-05-12 20:14

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Название категории')),
                ('image', models.ImageField(blank=True, default='images/products/placeholder.jpg', null=True, upload_to='images/category')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Filial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Наименование филиала')),
                ('address', models.CharField(max_length=200, verbose_name='Адрес')),
            ],
            options={
                'verbose_name': 'Филиал',
                'verbose_name_plural': 'Филиалы',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(default='name', max_length=50, verbose_name='Имя')),
                ('last_name', models.CharField(default='lastname', max_length=50, verbose_name='Фамилия')),
                ('address', models.CharField(default='lastname', max_length=200, verbose_name='Адрес')),
                ('paymentMethod', models.CharField(blank=True, max_length=200, null=True, verbose_name='Способ оплаты')),
                ('order_data', models.DateField(auto_now_add=True, verbose_name='Дата заказа')),
                ('status', models.BooleanField(default=False, verbose_name='Статус заказа')),
                ('quantity', models.IntegerField(default=0, verbose_name='Количество')),
                ('delivery', models.CharField(choices=[('самовывоз', 'Самовывоз'), ('курьер', 'Курьер'), ('почта', 'Почта')], default='Самовывоз', max_length=128, verbose_name='Доставка')),
                ('comment', models.CharField(blank=True, max_length=512, null=True, verbose_name='Комментарий')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
                'ordering': ('-order_data',),
            },
        ),
        migrations.CreateModel(
            name='Producer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Производитель')),
                ('description', models.CharField(blank=True, max_length=256, null=True, verbose_name='Описание производителя')),
                ('logo', models.ImageField(blank=True, default='images/producers/placeholder.jpg', null=True, upload_to='images/producers')),
            ],
            options={
                'verbose_name': 'Производитель',
                'verbose_name_plural': 'Производители',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=256, verbose_name='Товар')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('image', models.ImageField(blank=True, default='images/products/placeholder.jpg', null=True, upload_to='images/products')),
                ('state_price', models.IntegerField(default=0, verbose_name='Базовая цена')),
                ('price', models.IntegerField(default=0, verbose_name='Цена')),
                ('rating', models.DecimalField(decimal_places=1, default=0.0, max_digits=5, verbose_name='Рейтинг')),
                ('numReviews', models.IntegerField(default=0, verbose_name='Кол-во оценок')),
                ('discount', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Скидка')),
                ('inStock', models.BooleanField(default=False, verbose_name='В наличии')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product', to='catalog.category', verbose_name='Категория')),
                ('producer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product', to='catalog.producer', verbose_name='Производитель')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=126, verbose_name='Адрес')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Профиль',
                'verbose_name_plural': 'Профили',
            },
        ),
        migrations.CreateModel(
            name='UserProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.product')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.category')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProductOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=1, verbose_name='Количество товара')),
                ('price', models.FloatField(default=0.0, verbose_name='Стоимость')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='catalog.order', verbose_name='Заказ')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='catalog.product', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Элемент заказа',
                'verbose_name_plural': 'Элементы заказа',
            },
        ),
        migrations.CreateModel(
            name='ProductFilial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=0, verbose_name='Количество товара на складе')),
                ('filial', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_filials', to='catalog.filial', verbose_name='Филиал')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_filials', to='catalog.product', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Филиал товара',
                'verbose_name_plural': 'Филиалы товара',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='subscribers',
            field=models.ManyToManyField(related_name='product_subscribers', through='catalog.UserProduct', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(related_name='order', through='catalog.ProductOrder', to='catalog.product'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='filial',
            name='products',
            field=models.ManyToManyField(related_name='filial', through='catalog.ProductFilial', to='catalog.product', verbose_name='Товар'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(blank=True, default=0, null=True, verbose_name='Рейтинг')),
                ('com_text', models.TextField(verbose_name='Текст комментария')),
                ('com_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата комментария')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='catalog.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_comments', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
                'ordering': ['-com_date'],
            },
        ),
        migrations.AddField(
            model_name='category',
            name='subscribers',
            field=models.ManyToManyField(related_name='subscribers', through='catalog.UserCategory', to=settings.AUTH_USER_MODEL),
        ),
    ]
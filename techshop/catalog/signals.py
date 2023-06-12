from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Comment, ProductFilial, ProductOrder, Product, UserCategory, UserProduct
from django.db.models import Avg
from django.core.mail import send_mail


@receiver(post_save, sender=Comment)
def my_callback(sender, instance, *args, **kwargs):
    product = instance.product
    rat = sender.objects.filter(product=instance.product).aggregate(Avg('rating'))
    rating = rat['rating__avg']
    product.rating = round(rating, 1)
    product.numReviews = sender.objects.filter(product=instance.product).count()
    product.save()


@receiver(post_delete, sender=Comment)
def my_delete(sender, instance, *args, **kwargs):
    product = instance.product
    if Comment.objects.all().count() == 0:
        rat = {'rating__avg': 0}
    else:
        rat = Comment.objects.filter(product=product).aggregate(Avg('rating'))
    print(rat)
    rating = rat['rating__avg']
    product.rating = round(rating, 1)
    product.numReviews = sender.objects.filter(product=instance.product).count()
    product.save()


@receiver(post_save, sender=ProductOrder)
def my_callback(sender, instance, *args, **kwargs):
    product = instance.product
    amount = instance.amount
    filials = ProductFilial.objects.filter(product=product)
    for f in filials:
        if f.amount < amount:
            amount = amount - f.amount
            f.amount = 0
            f.save()
        else:
            f.amount = f.amount - amount
            f.save()
            break


@receiver(post_save, sender=ProductFilial)
def my_callback(sender, instance, *args, **kwargs):
    product = instance.product
    filials = ProductFilial.objects.filter(product=product)
    t = 0
    for f in filials:
        t = t + f.amount
    if t > 0:
        if not product.inStock:
            product_id = instance.product.id
            users = UserProduct.objects.filter(product_id=product_id)
            for i in users:
                send_mail(
                    subject=f"Товар в наличии!",
                    message=f"Здравствуй, {i.user.username}."
                            f" Пополнение выбранного вами товара: {instance.product.name} \n"
                            f" Смотреть товар:  http://127.0.0.1:8000/{instance.product.id}",
                    from_email='anel031@yandex.ru',
                    recipient_list=[i.user.email]
                )
        product.inStock = True
        product.save()
    else:
        product.inStock = False
        product.save()


@receiver(post_save, sender=Product)
def product_saved(sender, instance, created, **kwargs):
    new_price = instance.state_price - ((instance.state_price * instance.discount) / 100)
    sender.objects.filter(pk=instance.pk).update(price=new_price)
    if created:
        cat_id = instance.category.id
        users = UserCategory.objects.filter(category_id=cat_id)
        for i in users:
            send_mail(
                subject=f"Внимание, новинка!",
                message=f"Здравствуй, {i.user.username}."
                        f" Добавлен новый товар в выбранной вами категории! \n Новинка: {instance.name} \n"
                        f" Смотреть товар:  http://127.0.0.1:8000/{instance.id}",
                from_email='anel031@yandex.ru',
                recipient_list=[i.user.email]
            )

# Generated by Django 4.2 on 2023-05-12 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producer',
            name='logo',
            field=models.ImageField(blank=True, default='images/producer/placeholder.jpg', null=True, upload_to='images/producer'),
        ),
    ]
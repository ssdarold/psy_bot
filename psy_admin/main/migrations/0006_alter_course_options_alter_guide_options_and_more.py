# Generated by Django 4.2.11 on 2024-03-18 09:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_product_alter_order_item'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='course',
            options={'verbose_name': 'Курс', 'verbose_name_plural': 'Курсы'},
        ),
        migrations.AlterModelOptions(
            name='guide',
            options={'verbose_name': 'Гайд', 'verbose_name_plural': 'Гайды'},
        ),
        migrations.RemoveField(
            model_name='guide',
            name='relation',
        ),
    ]
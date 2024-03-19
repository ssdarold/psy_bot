# Generated by Django 4.2.11 on 2024-03-08 09:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_message', models.TextField(verbose_name='Приветственное сообщение для команды /start')),
                ('help_message', models.TextField(verbose_name='Сообщение для команды /help')),
                ('promocode', models.CharField(max_length=255, verbose_name='Бонусный промокод')),
                ('guide_cost', models.PositiveIntegerField(verbose_name='Стоимость покупки гайда (руб.)')),
            ],
            options={
                'verbose_name': 'Настройки',
                'verbose_name_plural': 'Настройки',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tg_id', models.IntegerField(verbose_name='ID пользователя в телеграм')),
                ('user_name', models.CharField(max_length=255, null=True, verbose_name='Имя пользователя')),
                ('signup_date', models.DateTimeField(auto_now=True, verbose_name='Дата регистрации пользователя')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField(null=True, verbose_name='Сумма заказа')),
                ('creation_date', models.DateTimeField(auto_now=True, verbose_name='Дата создания заказа')),
                ('status', models.CharField(choices=[('completed', 'Завершен'), ('pending', 'В процессе'), ('decline', 'Отклонен')], max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_order', to='main.user', verbose_name='Связанный пользователь')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
        migrations.CreateModel(
            name='Guide',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guide_video_name', models.TextField(verbose_name='Описние видеофайла')),
                ('guide_video_file', models.FileField(blank=True, upload_to='videos', verbose_name='Видео гайда')),
                ('relation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='settings_relation', to='main.settings')),
            ],
            options={
                'verbose_name': 'Видео гайд',
                'verbose_name_plural': 'Видео гайды',
            },
        ),
    ]
from django.db import models


# Модель пользователей
class User(models.Model):
    tg_id = models.IntegerField(verbose_name = "ID пользователя в телеграм")
    user_name = models.CharField(max_length=255, verbose_name = "Имя пользователя", null=True)
    signup_date = models.DateTimeField(auto_now=True, verbose_name = "Дата регистрации пользователя")
    funnel_step = models.IntegerField(verbose_name = "Текущий этап в воронке", null=True)

    def __str__(self):
        return f"Пользователь {self.user_name}"

    class Meta:
         verbose_name = "Пользователь"
         verbose_name_plural = "Пользователи"



# Модель заказов
class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name = "Название товара")
    description = models.TextField(verbose_name = "Описание товара")
    price = models.PositiveIntegerField(verbose_name = "Цена 1 единицы товара (руб.)", null=True)

    def __str__(self):
        return self.name

    class Meta:
         verbose_name = "Товар"
         verbose_name_plural = "Товары"

# Модель заказов
class Order(models.Model):
    user = models.ForeignKey(User, verbose_name = "Связанный пользователь", on_delete=models.CASCADE, related_name = "user_order")
    item = models.ForeignKey(Product, verbose_name = "Товар в заказе", on_delete=models.CASCADE, related_name = "product_order", null=True)
    amount = models.PositiveIntegerField(verbose_name = "Сумма заказа", null=True)
    system_id = models.PositiveIntegerField(verbose_name = "Внутренний ID заказа", null=True)
    creation_date = models.DateTimeField(auto_now=True, verbose_name = "Дата создания заказа")
    status = models.CharField(max_length=255, choices=[('completed', 'Завершен'), ('pending', 'В процессе'), ('decline', 'Отклонен')])

    def __str__(self):
        return f"Заказ {self.id}"

    class Meta:
         verbose_name = "Заказ"
         verbose_name_plural = "Заказы"




# Модель настроек
class Settings(models.Model):
    start_message = models.TextField(verbose_name = "Приветственное сообщение для команды /start")
    start_audio_file = models.FileField(blank=True, upload_to='static/data/audios', verbose_name = "Приветственное аудио")
    help_message = models.TextField(verbose_name = "Сообщение для команды /help")
    promocode = models.CharField(max_length=255, verbose_name = "Бонусный промокод")
    guide_cost = models.PositiveIntegerField(verbose_name = "Стоимость покупки гайда (руб.)")
    course_cost = models.PositiveIntegerField(verbose_name = "Стоимость покупки курса (руб.)", null=True)

    def __str__(self):
        return f"Настройки сайта"    


    class Meta:
         verbose_name = "Настройки"
         verbose_name_plural = "Настройки"


# Модель Видео-курсов
class Course(models.Model):
    product = models.ForeignKey(Product, verbose_name = "Товар", on_delete=models.CASCADE, related_name = "course_product", null=True)
    course_video_name = models.CharField(max_length=255, verbose_name="Название курса")
    course_link = models.CharField(max_length=255, verbose_name="Ссылка", null=True)

    def __str__(self):
        return f"Курс {self.id}"
    
    class Meta:
         verbose_name = "Курс"
         verbose_name_plural = "Курсы"


# Модель Видео-курсов
class Meditation(models.Model):
    meditation_name = models.CharField(max_length=255, verbose_name="Название медитации")
    meditation_description = models.TextField(verbose_name="Описние медитации", null=True)
    meditation_file = models.FileField(blank=True, upload_to='static/data/audios/meditations', verbose_name = "Аудио медитации")

    def __str__(self):
        return f"Медитация {self.id}"
    
    class Meta:
         verbose_name = "Медитация"
         verbose_name_plural = "Медитации"



# Модель гайдов
class Guide(models.Model):
    guide_name = models.CharField(max_length=255, verbose_name="Название гайда", blank=True, null=True)
    guide_description = models.TextField(verbose_name="Описание гайда", blank=True, null=True)
    guide_file = models.FileField(blank=True, upload_to='static/data/videos/guide', verbose_name = "Файл гайда", null=True)

    def __str__(self):
        return self.guide_name
    
    class Meta:
         verbose_name = "Гайд"
         verbose_name_plural = "Гайды"
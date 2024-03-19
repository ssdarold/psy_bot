from django.contrib import admin
from main.models import User, Order, Guide, Course, Settings, Product, Meditation

class CourseInline(admin.StackedInline):
    model = Course

    extra = 1

class ProductAdmin(admin.ModelAdmin):
    def get_inline_instances(self, request, obj=None):
        # Если редактируемый объект имеет id=2 и это экземпляр модели Product,
        # добавляем инлайн CourseInline, иначе возвращаем пустой список
        if obj and obj.id == 2 and isinstance(obj, Product):
            return [CourseInline(self.model, self.admin_site)]
        return []


admin.site.register(Settings)
admin.site.register(Product, ProductAdmin)
admin.site.register(Meditation)

admin.site.site_header = "Административная панель"

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import *


class UserInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Доп. информация'


class UserAdm(UserAdmin):
    inlines = (UserInline, )


admin.site.unregister(User)
admin.site.register(User, UserAdm)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Producer)
admin.site.register(Order)
admin.site.register(Filial)
admin.site.register(ProductFilial)
admin.site.register(ProductOrder)
admin.site.register(Comment)

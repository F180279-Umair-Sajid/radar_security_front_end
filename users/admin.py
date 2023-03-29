from django.contrib import admin
from django.apps import apps

CustomUser = apps.get_model('users', 'CustomUser')

# Register your models here
admin.site.register(CustomUser)

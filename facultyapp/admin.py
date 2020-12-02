from django.contrib import admin
from .models import *
from django.contrib.admin.options import ModelAdmin

# Register your models here.
# admin.site.register(student)
admin.site.register(Bookdts)
admin.site.register(issbktb)
class registerAdmin(ModelAdmin):
    list_display = ["user","cnt","age","city","gender","enrollment","branch"]
admin.site.register(register, registerAdmin)

admin.site.register(contact_us)
from django.contrib import admin
from .models import *

@admin.register(Partner)

class ApiAdmin(admin.ModelAdmin):
    pass
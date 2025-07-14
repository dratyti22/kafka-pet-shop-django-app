from django.contrib import admin
from unfold.admin import ModelAdmin

from src.user.models import User


@admin.register(User)
class UserAdmin(ModelAdmin):
    pass

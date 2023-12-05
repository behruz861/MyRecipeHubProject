from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Recipe, Profile, CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm

admin.site.register(Recipe)
admin.site.register(Profile)
admin.site.register(CustomUser)
# admin.site.register(CustomUser)
#
#
# class CustomUserAdmin(UserAdmin):
#     add_form = CustomUserCreationForm
#     form = CustomUserChangeForm
#     model = CustomUser
#     list_display = ['email', 'username', ]
#
#
# admin.site.register(CustomUserAdmin)

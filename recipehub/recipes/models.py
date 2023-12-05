from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, AbstractUser
from django.urls import reverse
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth import get_user_model


class Recipe(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey('recipes.CustomUser', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='recipes/images/')
    ingredients = models.TextField()
    instructions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('recipes:recipe_detail', args=[str(self.pk)])


class CustomUser(AbstractUser):
    # name = models.CharField(max_length=255)
    # surname = models.CharField(max_length=255)
    # email = models.EmailField(unique=True)
    # password = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='recipes/profile_photo/', blank=True, null=True)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')], blank=True, null=True)
    is_moderator = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('user_profile', args=[str(self.pk)])

    def is_moderator(self):
        return self.groups.filter(name='Moderator').exists()

    def is_admin(self):
        return self.groups.filter(name='Admin').exists()


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    image = models.ImageField(upload_to='recipes/profile_photo/', blank=True, null=True)
    phone_number = models.CharField(max_length=12, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)

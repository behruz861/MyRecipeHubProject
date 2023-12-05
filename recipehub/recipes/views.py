from django.db import migrations
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Recipe, CustomUser
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm, CustomAuthenticationForm, ProfileForm, CustomUserSingUpForm
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model


# def signup(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             user.set_password(form.cleaned_data.get('password1'))
#             user.save()
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(username=user.username, password=raw_password)
#             login(request, user)
#             return redirect('home')
#     else:
#         form = CustomUserCreationForm()
#     return render(request, 'registration/signup.html', {'form': form})


class SignUpView(CreateView):
    model = CustomUser
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('user_login')
    form_class = CustomUserSingUpForm


class CustomUserLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'registration/login.html'
    next_page = reverse_lazy('my_home')


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def update_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'recipes/update_profile.html', {'form': form})


def home(request):
    return render(request, 'recipes/home.html')


class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipes/recipe_list.html'
    context_object_name = 'recipes'
    paginate_by = 10


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipes/recipe_detail.html'
    context_object_name = 'recipe'


class RecipeCreateView(CreateView):
    model = Recipe
    fields = ['title', 'author', 'image', 'ingredients', 'instructions']
    template_name = 'recipes/recipe_form.html'
    success_url = ''


class RecipeUpdateView(UpdateView):
    model = Recipe
    fields = ['title', 'author', 'image', 'ingredients', 'instructions']
    template_name = 'recipes/recipe_form.html'
    success_url = '/recipe_list/'


class RecipeDeleteView(DeleteView):
    model = Recipe
    success_url = reverse_lazy('recipes:recipe_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({'success': True, 'redirect_url': self.get_success_url()})


def create_moderators_group(apps, schema_editor):
    Group.objects.get_or_create(name='moderators')


class Migration(migrations.Migration):
    dependencies = [
        ('recipes', '001_initial'),
    ]
    operations = [
        migrations.RunPython(create_moderators_group, )
    ]


def add_user_to_moderator(user):
    group = Group.objects.get(name='moderators')
    user.groups.remove(group)


def is_moderator(user):
    return user.groups.filter(name='moderators')


class User:
    def __init__(self, username, role):
        self.username = username
        self.role = role

    def is_admin(self):
        return self.role == 'admin'


def is_admin(user):
    return user.is_admin()


def make_user_moderator(request, username):
    User = get_user_model()
    user = User.objects.get(username=username)
    user.is_moderator = True
    user.save()
    return render(request, 'directoryy/user_moderator.html', {'username': username})

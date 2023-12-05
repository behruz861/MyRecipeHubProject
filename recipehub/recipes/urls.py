from django.urls import path
from .views import home, RecipeListView, RecipeDetailView, RecipeCreateView, RecipeUpdateView, RecipeDeleteView, \
    logout, CustomUserLoginView, update_profile, SignUpView
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'recipes'

urlpatterns = [
                  path('home/', home, name='my_home'),
                  path('signup/', SignUpView.as_view(), name='signup'),
                  path('login/', CustomUserLoginView.as_view(), name='user_login'),
                  path('logout/', logout, name='logout'),
                  path('update_profile', update_profile, name='update_profile'),
                  path('recipe_list/', RecipeListView.as_view(), name='recipe_list'),
                  path('<int:pk>/', RecipeDetailView.as_view(), name='recipe_detail'),
                  path('recipes/add/', RecipeCreateView.as_view(), name='recipe_add'),
                  path('recipes/<int:pk>/update/', RecipeUpdateView.as_view(), name='recipe_update'),
                  path('recipes/<int:pk>/delete/', RecipeDeleteView.as_view(), name='recipe_delete'),
                  path('make_moderator/<str:username>/', views.make_user_moderator, name='make_moderator'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

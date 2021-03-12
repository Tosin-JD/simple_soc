from django.urls import path
from django.contrib.auth import views as auth_views
from accounts import views

app_name = 'accounts'
urlpatterns = [
    path('sign-up/', views.SignUp.as_view(), name='sign_up'),
    path('profile/', views.ProfileView.as_view(), name='user_profile'),
    path('login/',
         auth_views.LoginView.as_view(template_name='accounts/login.html'),
         name='login'),
    path('logout/',
         auth_views.LogoutView.as_view(), name='logout'),
]

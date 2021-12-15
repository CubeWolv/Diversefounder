"""diversefounders URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from accounts import views as ac


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('accounts/signup/',ac.signup, name='signup'),
    path('accounts/login/', ac.login, name='login'),
    path('accounts/', include('allauth.urls')),
    path('dashboard/logoutuser',ac.logoutUser ,name='logoutuser'),
    

    #Password reset
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='forms/password_reset.html'),
    name='password_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='forms/password_reset_done.html'),
    name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='forms/password_reset_confirm.html'),
    name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='forms/password_reset_complete.html'),
    name='password_reset_complete'),


    #path('authorize/', StripeAuthorizeView.as_view(), name='authorize'),
    
    #path('users/oauth/callback/', StripeAuthorizeCallbackView.as_view(), name='authorize_callback'),
]

handler404= 'main.views.error_404'
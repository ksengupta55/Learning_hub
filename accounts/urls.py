"""Defines URL patterns for accounts."""
from django.urls import path, include
from .import views
from django.contrib.auth import views as auth_views
from accounts.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns = [
    # Include default auth urls. 
    path('', include('django.contrib.auth.urls')),
    # Registration page.
    path('register/', views.register, name='register'), 
    
        # Password reset links (ref: https://github.com/django/django/blob/master/django/contrib/auth/views.py)
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'), name='password_change'),

    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),    

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]


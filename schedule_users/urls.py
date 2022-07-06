from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('', views.taxinet_home, name="home"),
    path('driver-profile/', views.driver_profile),
    path('get_user/', views.get_user),
    path('get_passenger_profile/<int:id>/', views.get_passenger_profile),
    path('get_drivers_profile/<int:id>/', views.get_drivers_profile),
    path('get_passenger_details/<int:id>/', views.get_passenger_details),
    path('get_drivers_details/<int:id>/', views.get_drivers_details),
    path('all_passengers/', views.get_all_passengers),
    path('all_drivers/', views.get_all_drivers),
    path('passenger-profile/', views.passenger_profile),
    path('update_driver_profile/', views.update_driver_profile),
    path('update_passenger_profile/', views.update_passenger_profile),
    path('update_username/', views.update_username),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='schedule_users/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='schedule_users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='schedule_users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='schedule_users/password_reset_complete.html'), name='password_reset_complete'),
]

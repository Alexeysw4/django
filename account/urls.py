from django.urls import path
from django.contrib.auth import views as auth_views

from account import views
from account.views import CustomPasswordResetDoneView, CustomPasswordResetView, CustomPasswordResetCompleteView, \
    CustomPasswordResetConfirmView

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change/',
         auth_views.PasswordChangeView.as_view(),
         name='password_change'),
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(),
         name='password_change_done'),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('users/', views.user_list, name='user_list'),
    path('users/follow/', views.user_follow, name='user_follow'),
    path('users/<username>/', views.user_detail, name='user_detail'),
    path('followers/', views.followers_list, name='followers_list'),
    path('following/', views.following_list, name='following_list'),
    path('password/reset/done/', CustomPasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('password/reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password/confirm/complete/', CustomPasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    path('password/confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('', views.dashboard, name='dashboard')
]

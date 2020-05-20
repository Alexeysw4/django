from django.urls import path
from tweets import views

app_name = 'tweets'

urlpatterns = [
    path('create/', views.tweet_create, name='create'),
    path('detail/<int:id>/', views.tweet_detail, name='detail'),
    path('', views.tweet_list, name='list'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('reply/<int:id>/', views.add_reply, name='reply'),
    path('like/<int:pk>/', views.like, name='like'),
    path('dislike/<int:pk>/', views.dislike, name='dislike'),
]
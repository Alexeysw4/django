"""twitter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings
from rest_framework.routers import DefaultRouter
from .yasg import urlpatterns as doc_urls
from music.api import *
from account import views

router = DefaultRouter()
router.register('songs', APISongViewSet)
router.register('albums', APIAlbumViewSet)
router.register('singers', APISingerViewSet)
router.register('genres', APIGenreViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('tweets/', include('tweets.urls', namespace='tweets')),
    path('music/', include('music.urls', namespace='music')),
    path('api/v1/', include(router.urls)),
    path('', views.main),
]

urlpatterns += doc_urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

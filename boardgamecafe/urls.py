from django.urls import path
from .import views

app_name = 'boardgamecafe'
urlpatterns = [
    path('', views.index, name='index'),
    path('tempband', views.tempband, name='tempband'),
]
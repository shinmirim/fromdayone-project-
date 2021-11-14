#search_app/urls.py
from django.urls import path
from . import views

#from .views import HomePageView, SearchResultsView

urlpatterns = [
    path('', views.index, name='index'),
    path('ver1', views.ver1,name='ver1'),
    path('ver2', views.ver2,name='ver2'),
]
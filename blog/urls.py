from django.urls import path
from . import views

urlpatterns = [
    path('', views.article_list, name='article_list'),
    path('register/', views.register, name='register'),
    path('my-articles/', views.my_articles, name='my_articles'),
    path('article/create/', views.article_create, name='article_create'),
    path('article/<int:pk>/', views.article_detail, name='article_detail'),
    path('article/<int:pk>/edit/', views.article_update, name='article_update'),
    path('article/<int:pk>/delete/', views.article_delete, name='article_delete'),
]

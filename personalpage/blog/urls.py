from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:blog_id>/', views.detail, name='detail'),
    path('new/', views.new, name='new'),
    path('create/', views.create, name='create'),
    path('create_author/', views.create_author, name='create_author'),
    path('author/<int:author_id>', views.author_detail, name='author_detail'),
    path('author/new', views.new_author, name='new_author'),
]

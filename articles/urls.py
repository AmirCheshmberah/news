from django.urls import path
from . import views

urlpatterns = [
    path('', views.article_list_view, name='article_list'),
    path('<int:pk>/detail/', views.article_detail_view, name='article_detail'),
    path('<int:pk>/edit/', views.article_update_view, name='article_edit'),
    path('<int:pk>/delete/', views.article_delete_view, name='article_delete'),
    
]
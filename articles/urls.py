from django.urls import path
from . import views

urlpatterns = [
    path('', views.article_list_view, name='article_list'),
    path('new/', views.ArticleCreateView.as_view(), name='article_new'),
    path('<int:pk>/detail/', views.ArticleDetailView.as_view(), name='article_detail'),
    path('<int:pk>/edit/', views.ArticleUpdateView.as_view(), name='article_edit'),
    path('<int:pk>/delete/', views.ArticleDeleteView.as_view(), name='article_delete'),
]
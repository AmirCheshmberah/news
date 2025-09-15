from django.urls import path
from . import views
urlpatterns = [
    path('', views.new_user_view, name='new_user_form')
]
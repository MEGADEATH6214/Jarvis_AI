from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('set_chat_id/', views.set_chat_id)
]
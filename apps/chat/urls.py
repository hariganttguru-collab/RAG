from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.chat_list, name='chat_list'),
    path('<int:stakeholder_id>/', views.chat_room, name='chat_room'),
    path('<int:stakeholder_id>/send/', views.send_message, name='send_message'),
]


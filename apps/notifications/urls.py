from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.get_notifications, name='get_notifications'),
    path('<int:notification_id>/read/', views.mark_read, name='mark_read'),
]


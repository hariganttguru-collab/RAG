from django.urls import path
from . import views

app_name = 'documents'

urlpatterns = [
    path('<int:document_id>/', views.document_view, name='document_view'),
]


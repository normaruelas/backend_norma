from django.urls import path
from .views import menu_export

urlpatterns = [
    path('menu_export/', menu_export, name='menu_export'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='dashboards'),
    path('action/', views.action, name='action'),
]
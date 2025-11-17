from django.urls import path
from . import views

urlpatterns = [
    path('', views.client_list, name='client_list'),
    path('client/<int:pk>/', views.client_detail, name='client_detail'),
    path('client/new/', views.client_create, name='client_create'),
    path('client/<int:pk>/edit/', views.client_update, name='client_update'),
    path('client/<int:pk>/delete/', views.client_delete, name='client_delete'),
]

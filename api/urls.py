from django.urls import path
from . import views

urlpatterns = [
    path('healthcheck', views.healthcheck, name='healthcheck'),
    path('clients/orders', views.orders.clients_orders, name='clients_orders'),
    path('clients/menu', views.menu.clients_menu, name='clients_menu'),
]
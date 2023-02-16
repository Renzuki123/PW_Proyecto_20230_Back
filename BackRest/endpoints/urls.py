from django.urls import path
from . import views



urlpatterns = [


    path("loginRestaurante", views.LoginRest), ### Login del restaurante

    path("categorias", views.CategPedidos),   ###categorias de los pedidos

    path("cambiarEstado",views.cambiarEstado_Pedido) ## Cambiar estado del pedido

]
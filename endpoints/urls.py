from django.urls import path

# Se pone "." porque este archivo y views están en el mismo nivel de directorio
from . import views

urlpatterns = [
    path("login", views.login), #Req1: Validación Login
    path("restaurante/listar", views.obtenerRestaurante), #Req3: Restaurantes Por Categoria
    path("plato/listar", views.obtenerPlato), #Req4: Platos Por Categoría

    # Paths de Renzo Saucedo
    path("recomendaciones", views.ObtenerRecomendaciones),
    path("verestado", views.verEstado),
    path("registrarentrega", views.registrarentrega),
    path("platosgenericos", views.ObtenerPlatosGenericos),
    path("registrar_pedido", views.registrar_pedido),
    path('pedidos', views.pedidos),
    path('buscar_pedido_por_codigo', views.buscar_pedido_por_codigo),
    path('cambiarEstado', views.cambiarEstado_Pedido),
    path("loginRestaurante", views.LoginRest), ### Login del restaurante

    #path("categorias", views.CategPedidos),   ###categorias de los pedidos
    path("categorias", views.ObtenerCategoria),   

    path("cambiarEstado",views.cambiarEstado_Pedido) ## Cambiar estado del pedido
]

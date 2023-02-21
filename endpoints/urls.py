from django.urls import path

# Se pone "." porque este archivo y views están en el mismo nivel de directorio
from . import views

urlpatterns = [
    path("login", views.login), #Req1: Validación Login
    path("restaurante/listar", views.obtenerRestaurante), #Req3: Restaurantes Por Categoria
    path("platos/listar", views.obtenerPlatos), #Req4: Platos Por Categoría

    # Paths de Renzo Saucedo
    path("recomendaciones", views.ObtenerRecomendaciones),
    path("verestado", views.verEstado),
    path("registrarentrega", views.registrarentrega),
    path("platosgenericos", views.ObtenerPlatosGenericos)
]

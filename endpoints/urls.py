from django.urls import path

# Se pone "." porque este archivo y views están en el mismo nivel de directorio
from . import views

urlpatterns = [
    path("login", views.login), #Req1: Validación Login
    path("listarRestaurantes", views.obtenerRestaurantes), #Req3: Restaurantes Por Categoria
    path("listarPlatos", views.obtenerPlatos), #Req4: Platos Por Categoría

    
    path("recomendaciones", views.ObtenerRecomendaciones),
    path("verestado", views.verEstado),
    path("registrarentrega", views.registrarentrega)
]

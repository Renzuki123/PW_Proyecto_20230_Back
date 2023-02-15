from django.urls import path

from . import views # Se pone "." porque este archivo y views están en el mismo nivel de directorio

urlpatterns = [
    path("hola", views.holaEndpoint),
    path("adios", views.endpoint2),
    path("html", views.htmlEndpoint),
    path("recomendaciones", views.ObtenerRecomendaciones),
]
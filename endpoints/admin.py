from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.User) #Renzo Cavero
admin.site.register(models.CategoriaPlato) #Renzo Cavero
admin.site.register(models.Plato) #Renzo Cavero
admin.site.register(models.CategoriaRestaurante) #Renzo Cavero
admin.site.register(models.Restaurante) #Renzo Cavero
admin.site.register(models.Pedido) # Renzo Saucedo
admin.site.register(models.PedidoXPlato)# Renzo Saucedo

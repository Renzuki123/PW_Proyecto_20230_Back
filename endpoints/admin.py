from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.User)
admin.site.register(models.Categoria)
admin.site.register(models.Platos)
admin.site.register(models.Restaurantes)

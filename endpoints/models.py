from django.db import models

# Create your models here.
# Modelos creados por Renzo Cavero:
class User(models.Model):
    usuario = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.usuario + " " + self.password

    @staticmethod
    def authenticate(usuario, password):
        try:
            user = User.objects.get(usuario=usuario, password=password)
            return user
        except User.DoesNotExist:
            return None

class Plato(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    img = models.URLField()
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    def __str__(self):
        return self.nombre

class Restaurante(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    description = models.TextField()
    date = models.CharField(max_length=50)

    def __str__(self):
        return self.title

# Modelos creados por Renzo Saucedo
class Pedido(models.Model):
    id = models.AutoField(primary_key=True)
    PEDIDO_ESTADOS = (
        ("S", "SOLICITADO"),
        ("EP", "EN PREPARACION"),
        ("EC", "EN CAMINO"),
        ("E", "ENTREGADO")
    )
    nombre = models.CharField(max_length=50, default="")
    direccion = models.CharField(max_length=100, default="")
    referencias = models.CharField(max_length=100, default="")
    detalles = models.CharField(max_length=100, default="")
    #codigo = models.CharField(max_length=6)
    codigo = models.CharField(max_length=6, default ="ABC123")
    metodo = models.CharField(max_length=15, default="")
    total = models.DecimalField(default=0.0, decimal_places=2, max_digits=7) 
    
    #def __str__(self):
    #    return f"{self.nombre} - {self.direccion} - {self.codigo}"

class PedidoXPlato(models.Model):
    id = models.AutoField(primary_key=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    plato = models.ForeignKey(Plato, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=6, decimal_places=2, default= 0)
    

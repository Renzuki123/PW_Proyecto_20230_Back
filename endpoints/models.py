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

class Categoria(models.Model):
    nombre = models.CharField(max_length=50)
    def __str__(self):
        return self.nombre

class Platos(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    img = models.ImageField(upload_to='platos/')
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.nombre

class Restaurantes(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    img = models.ImageField(upload_to='platos/')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.nombre

class Pedido(models.Model):
    PEDIDO_ESTADOS = (
        ("S", "SOLICITADO"),
        ("EP", "EN PREPARACION"),
        ("EC", "EN CAMINO"),
        ("E", "ENTREGADO")
    )

class PedidoXPlato(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    plato = models.ForeignKey(Platos, on_delete=models.CASCADE)
    precio = models.DecimalField(default=0.0, decimal_places=2, max_digits=7)

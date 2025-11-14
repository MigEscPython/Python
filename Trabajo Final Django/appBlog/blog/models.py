from django.db import models
from django.conf import settings
from django.utils import timezone

class Post(models.Model):
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=500)
    texto = models.TextField()
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_publicacion = models.DateTimeField(blank=True, null=True)

    def get_fecha_publicacion(self):
        self.fecha_publicacion = timezone.now()
        self.save()

    def __str__(self):
        return self.titulo
    

# -------------------------------------------------------
# 1. Proveedores
# -------------------------------------------------------
class Proveedor(models.Model):
    nombre = models.CharField(max_length=200)
    ruc = models.CharField(max_length=20, unique=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.nombre} - RUC: {self.ruc}"


# -------------------------------------------------------
# 2. Clientes
# -------------------------------------------------------
class Cliente(models.Model):
    nombre = models.CharField(max_length=200)
    ruc = models.CharField(max_length=20, unique=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} - RUC: {self.ruc}"


# -------------------------------------------------------
# 3. Categorías de productos
# -------------------------------------------------------
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre


# -------------------------------------------------------
# 4. Productos
# -------------------------------------------------------
class Producto(models.Model):
    IVA_CHOICES = [
        (0, 'Exento'),
        (5, '5%'),
        (10, '10%'),
    ]

    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=200)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    descripcion = models.TextField(blank=True, null=True)
    precio_compra = models.DecimalField(max_digits=12, decimal_places=2)
    precio_venta = models.DecimalField(max_digits=12, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    iva = models.IntegerField(choices=IVA_CHOICES, default=10)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} ({self.codigo})"

    def total_con_iva(self):
        return self.precio_venta * (1 + self.iva / 100)


# -------------------------------------------------------
# 5. Compras (Ingreso de stock)
# -------------------------------------------------------
class Compra(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    fecha = models.DateField(default=timezone.now)
    timbrado = models.CharField(max_length=15, help_text="Número de timbrado fiscal", blank=True, null=True)
    nro_factura = models.CharField(max_length=20)
    total = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    def __str__(self):
        return f"Compra {self.nro_factura} - {self.proveedor.nombre}"

    def calcular_total(self):
        total = sum(item.subtotal() for item in self.detallecompra_set.all())
        self.total = total
        self.save()


class DetalleCompra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)

    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Aumentar stock automáticamente
        self.producto.stock += self.cantidad
        self.producto.save()


# -------------------------------------------------------
# 6. Ventas
# -------------------------------------------------------
class Venta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateField(default=timezone.now)
    timbrado = models.CharField(max_length=15, blank=True, null=True)
    nro_factura = models.CharField(max_length=20)
    total = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    def __str__(self):
        return f"Venta {self.nro_factura} - {self.cliente.nombre}"

    def calcular_total(self):
        total = sum(item.subtotal_con_iva() for item in self.detalleventa_set.all())
        self.total = total
        self.save()


class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    iva = models.IntegerField(choices=Producto.IVA_CHOICES)

    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def subtotal_con_iva(self):
        return self.subtotal() * (1 + self.iva / 100)

    def save(self, *args, **kwargs):
        # Reducir stock automáticamente
        super().save(*args, **kwargs)
        self.producto.stock -= self.cantidad
        self.producto.save()

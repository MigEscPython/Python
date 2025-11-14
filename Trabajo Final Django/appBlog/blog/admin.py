from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *

admin.site.register(Post)
admin.site.register(Proveedor)
admin.site.register(Cliente)
admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Compra)
admin.site.register(DetalleCompra)
admin.site.register(Venta)
admin.site.register(DetalleVenta)
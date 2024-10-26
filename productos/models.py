from django.db import models

class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)  # Refleja el nombre correcto en la BD
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'categorias'  # Nombre de la tabla existente en MySQL

class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)  # Refleja el nombre correcto en la BD
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'clientes'

class Despacho(models.Model):
    id_despacho = models.AutoField(primary_key=True)  # Refleja el nombre correcto en la BD
    direccion_entrega = models.CharField(max_length=200)
    fecha_despacho = models.DateField()
    estado = models.CharField(max_length=50)
    orden = models.ForeignKey('Orden', on_delete=models.CASCADE, db_column='id_orden')  # Clave foránea correcta

    class Meta:
        db_table = 'despachos'

class DetalleOrden(models.Model):
    id_detalle = models.AutoField(primary_key=True)  # Refleja el nombre correcto en la BD
    orden = models.ForeignKey('Orden', on_delete=models.CASCADE, db_column='id_orden')  # Clave foránea correcta
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE, db_column='id_producto')  # Clave foránea correcta
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'detalles_orden'

class Orden(models.Model):
    id_orden = models.AutoField(primary_key=True)  # Refleja el nombre correcto en la BD
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE, db_column='id_cliente')  # Clave foránea correcta
    fecha = models.DateField()
    total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'ordenes'

class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)  # Refleja el nombre correcto en la BD
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, db_column='id_categoria')  # Clave foránea correcta
    proveedor = models.ForeignKey('Proveedor', on_delete=models.SET_NULL, null=True, db_column='id_proveedor')  # Clave foránea correcta

    class Meta:
        db_table = 'productos'

class Proveedor(models.Model):
    id_proveedor = models.AutoField(primary_key=True)  # Refleja el nombre correcto en la BD
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    correo = models.EmailField()

    class Meta:
        db_table = 'proveedores'

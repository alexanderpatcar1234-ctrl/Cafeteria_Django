# Importamos la configuración general de Django.
# Nos permitirá relacionar los pedidos con los usuarios.
from django.conf import settings

# Importamos el sistema de modelos de Django.
from django.db import models


# =========================================================
# MODELO CATEGORIA
# =========================================================

class Categoria(models.Model):

    # Nombre de la categoría.
    nombre = models.CharField(max_length=100)

    # Descripción opcional.
    descripcion = models.TextField(blank=True)

    # Permite activar o desactivar categorías.
    activo = models.BooleanField(default=True)

    def __str__(self):
        # Texto que se mostrará en el administrador.
        return self.nombre

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ["nombre"]


# =========================================================
# MODELO PRODUCTO
# =========================================================

class Producto(models.Model):

    # Nombre comercial del producto.
    nombre = models.CharField(max_length=100)

    # Descripción del producto.
    descripcion = models.TextField(blank=True)

    # Cada producto pertenece a una categoría.
    # Si la categoría se elimina, el producto permanecerá.
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="productos",
    )

    # Precio del producto con dos decimales.
    precio = models.DecimalField(
        max_digits=8,
        decimal_places=2,
    )

    # Cantidad disponible.
    stock = models.PositiveIntegerField(default=0)

    # Imagen del producto.
    # Las imágenes se guardarán en:
    # media/productos/
    imagen = models.ImageField(
        upload_to="productos/",
        blank=True,
    )

    # Permite ocultar un producto sin eliminarlo.
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ["nombre"]


# =========================================================
# MODELO PEDIDO
# =========================================================

class Pedido(models.Model):

    # Estados posibles de un pedido.
    class Estado(models.TextChoices):
        PENDIENTE = "PENDIENTE", "Pendiente"
        PREPARACION = "PREPARACION", "En preparación"
        ATENDIDO = "ATENDIDO", "Atendido"
        CANCELADO = "CANCELADO", "Cancelado"

    # Usuario que realizó el pedido.
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="pedidos",
    )

    # Fecha automática de creación.
    fecha = models.DateTimeField(auto_now_add=True)

    # Total monetario del pedido.
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    # Estado actual del pedido.
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.PENDIENTE,
    )

    def __str__(self):
        return f"Pedido {self.id} - {self.usuario.username}"

    class Meta:
        ordering = ["-fecha"]


# =========================================================
# MODELO DETALLE PEDIDO
# =========================================================

class DetallePedido(models.Model):

    # Pedido al que pertenece este producto.
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name="detalles",
    )

    # Producto seleccionado.
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name="detalles_pedido",
    )

    # Cantidad comprada.
    cantidad = models.PositiveIntegerField(
        default=1
    )

    # Precio que tenía el producto
    # cuando se confirmó el pedido.
    #
    # Este valor se guarda para evitar que
    # un cambio posterior en Producto.precio
    # modifique pedidos antiguos.
    precio_unitario = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
    )

    # Calculamos el subtotal de esta línea.
    @property
    def subtotal(self):

        return self.precio_unitario * self.cantidad

    def __str__(self):

        return (
            f"{self.producto.nombre} "
            f"x{self.cantidad}"
        )

    class Meta:

        verbose_name = "Detalle de pedido"

        verbose_name_plural = "Detalles de pedido"

# Importamos el administrador de Django.
from django.contrib import admin

# Importamos nuestros modelos.
from .models import (
    Categoria,
    Producto,
    Pedido,
    DetallePedido,
)


# =========================================================
# ADMINISTRACIÓN DE CATEGORÍAS
# =========================================================

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):

    # Columnas visibles en la lista.
    list_display = (
        "nombre",
        "activo",
    )

    # Campo utilizado por el buscador.
    search_fields = (
        "nombre",
    )

    # Filtros laterales.
    list_filter = (
        "activo",
    )


# =========================================================
# ADMINISTRACIÓN DE PRODUCTOS
# =========================================================

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):

    # Columnas visibles.
    list_display = (
        "nombre",
        "categoria",
        "precio",
        "stock",
        "activo",
    )

    # Permite editar algunos campos directamente
    # desde la lista de productos.
    list_editable = (
        "precio",
        "stock",
        "activo",
    )

    # Buscador.
    search_fields = (
        "nombre",
        "descripcion",
    )

    # Filtros.
    list_filter = (
        "categoria",
        "activo",
    )

    # Orden alfabético.
    ordering = (
        "nombre",
    )


# =========================================================
# DETALLE DEL PEDIDO DENTRO DEL PEDIDO
# =========================================================

class DetallePedidoInline(admin.TabularInline):

    # Modelo que aparecerá dentro del pedido.
    model = DetallePedido

    # No mostrar filas vacías adicionales.
    extra = 0


# =========================================================
# ADMINISTRACIÓN DE PEDIDOS
# =========================================================

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "usuario",
        "fecha",
        "total",
        "estado",
    )

    search_fields = (
        "usuario__username",
    )

    list_filter = (
        "estado",
        "fecha",
    )

    # Los detalles se mostrarán dentro del pedido.
    inlines = [
        DetallePedidoInline,
    ]


# =========================================================
# ADMINISTRACIÓN DE DETALLES
# =========================================================

@admin.register(DetallePedido)
class DetallePedidoAdmin(admin.ModelAdmin):

    list_display = (
        "pedido",
        "producto",
        "cantidad",
    )

    search_fields = (
        "producto__nombre",
        "pedido__usuario__username",
    )

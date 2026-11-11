# =========================================================
# URL DE LA APLICACIÓN
# =========================================================

from django.urls import path

from . import views


urlpatterns = [

    # -----------------------------------------------------
    # INICIO
    # -----------------------------------------------------

    path(
        "inicio/",
        views.inicio,
        name="inicio",
    ),


    # -----------------------------------------------------
    # TIENDA
    # -----------------------------------------------------

    path(
        "tienda/",
        views.tienda,
        name="tienda",
    ),


    # -----------------------------------------------------
    # CARRITO
    # -----------------------------------------------------

    # Mostrar carrito.
    path(
        "carrito/",
        views.ver_carrito,
        name="ver_carrito",
    ),

    # Agregar producto.
    path(
        "carrito/agregar/<int:producto_id>/",
        views.agregar_producto,
        name="agregar_producto",
    ),

    # Restar una unidad.
    path(
        "carrito/restar/<int:producto_id>/",
        views.restar_producto,
        name="restar_producto",
    ),

    # Eliminar completamente un producto.
    path(
        "carrito/eliminar/<int:producto_id>/",
        views.eliminar_producto,
        name="eliminar_producto",
    ),

    # Vaciar carrito.
    path(
        "carrito/vaciar/",
        views.vaciar_carrito,
        name="vaciar_carrito",
    ),


    # -----------------------------------------------------
    # CONFIRMAR PEDIDO
    # -----------------------------------------------------

    path(
        "pedido/confirmar/",
        views.confirmar_pedido,
        name="confirmar_pedido",
    ),


    # -----------------------------------------------------
    # PEDIDOS DEL USUARIO
    # -----------------------------------------------------

    path(
        "mis-pedidos/",
        views.mis_pedidos,
        name="mis_pedidos",
    ),


    # -----------------------------------------------------
    # DETALLE
    # -----------------------------------------------------

    path(
        "pedido/<int:pedido_id>/",
        views.detalle_pedido,
        name="detalle_pedido",
    ),


    # -----------------------------------------------------
    # REPORTES
    # -----------------------------------------------------

    path(
        "reportes/",
        views.reportes,
        name="reportes",
    ),

]

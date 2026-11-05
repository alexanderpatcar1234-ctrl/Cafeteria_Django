# Importamos path para poder definir las rutas
# disponibles dentro de la aplicación.
from django.urls import path

# Importamos las vistas creadas en views.py.
from . import views


# =========================================================
# RUTAS DE LA APLICACIÓN
# =========================================================

urlpatterns = [

    # -----------------------------------------------------
    # MÓDULO PRINCIPAL
    # -----------------------------------------------------

    # Página principal después del inicio de sesión.
    path(
        "inicio/",
        views.inicio,
        name="inicio",
    ),


    # -----------------------------------------------------
    # TIENDA
    # -----------------------------------------------------

    # Muestra todos los productos activos
    # almacenados en la base de datos.
    path(
        "tienda/",
        views.tienda,
        name="tienda",
    ),


    # -----------------------------------------------------
    # PEDIDOS DEL USUARIO
    # -----------------------------------------------------

    # Muestra únicamente los pedidos
    # pertenecientes al usuario autenticado.
    path(
        "mis-pedidos/",
        views.mis_pedidos,
        name="mis_pedidos",
    ),


    # -----------------------------------------------------
    # DETALLE DE PEDIDO
    # -----------------------------------------------------

    # <int:pedido_id> representa el identificador
    # numérico del pedido que queremos consultar.
    #
    # Ejemplo:
    # /pedido/5/
    path(
        "pedido/<int:pedido_id>/",
        views.detalle_pedido,
        name="detalle_pedido",
    ),

]

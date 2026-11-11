# =========================================================
# CARRITO DE COMPRAS
# =========================================================

# Decimal permitirá manejar correctamente
# valores monetarios.
from decimal import Decimal

# Importamos Producto para consultar
# los datos almacenados en la base.
from .models import Producto


class Carrito:

    # Nombre utilizado dentro de la sesión.
    SESSION_KEY = "carrito"

    def __init__(self, request):

        # Guardamos la sesión del usuario.
        self.session = request.session

        # Intentamos recuperar un carrito existente.
        carrito = self.session.get(
            self.SESSION_KEY
        )

        # Si todavía no existe, creamos
        # un diccionario vacío.
        if carrito is None:

            carrito = {}

            self.session[
                self.SESSION_KEY
            ] = carrito

        self.carrito = carrito


    # =====================================================
    # GUARDAR CAMBIOS
    # =====================================================

    def guardar(self):

        # Guardamos nuevamente el carrito
        # dentro de la sesión.
        self.session[
            self.SESSION_KEY
        ] = self.carrito

        # Indicamos a Django que la sesión
        # fue modificada.
        self.session.modified = True


    # =====================================================
    # CANTIDAD ACTUAL
    # =====================================================

    def cantidad_actual(self, producto):

        producto_id = str(producto.id)

        return int(
            self.carrito.get(
                producto_id,
                0,
            )
        )


    # =====================================================
    # AGREGAR PRODUCTO
    # =====================================================

    def agregar(self, producto):

        # No permitimos productos inactivos.
        if not producto.activo:

            return False

        # No permitimos productos sin stock.
        if producto.stock <= 0:

            return False

        producto_id = str(producto.id)

        cantidad = self.cantidad_actual(
            producto
        )

        # Impedimos agregar más unidades
        # que las disponibles.
        if cantidad >= producto.stock:

            return False

        # Incrementamos una unidad.
        self.carrito[producto_id] = (
            cantidad + 1
        )

        self.guardar()

        return True


    # =====================================================
    # RESTAR UNA UNIDAD
    # =====================================================

    def restar(self, producto):

        producto_id = str(producto.id)

        if producto_id in self.carrito:

            cantidad = (
                int(
                    self.carrito[
                        producto_id
                    ]
                )
                - 1
            )

            # Si llega a cero eliminamos
            # el producto completamente.
            if cantidad <= 0:

                del self.carrito[
                    producto_id
                ]

            else:

                self.carrito[
                    producto_id
                ] = cantidad

            self.guardar()


    # =====================================================
    # ELIMINAR PRODUCTO
    # =====================================================

    def eliminar(self, producto):

        producto_id = str(producto.id)

        if producto_id in self.carrito:

            del self.carrito[
                producto_id
            ]

            self.guardar()


    # =====================================================
    # VACIAR CARRITO
    # =====================================================

    def limpiar(self):

        self.session[
            self.SESSION_KEY
        ] = {}

        self.carrito = {}

        self.session.modified = True


    # =====================================================
    # OBTENER PRODUCTOS Y TOTAL
    # =====================================================

    def obtener_items(self):

        # Recuperamos todos los identificadores
        # almacenados en la sesión.
        ids = list(
            self.carrito.keys()
        )

        # Buscamos los productos existentes
        # en la base de datos.
        productos = (
            Producto.objects
            .filter(id__in=ids)
            .select_related("categoria")
            .order_by("nombre")
        )

        items = []

        total = Decimal("0.00")

        for producto in productos:

            cantidad = int(
                self.carrito.get(
                    str(producto.id),
                    0,
                )
            )

            # Calculamos el subtotal.
            subtotal = (
                producto.precio
                * cantidad
            )

            total += subtotal

            items.append(
                {
                    "producto": producto,
                    "cantidad": cantidad,
                    "subtotal": subtotal,
                }
            )

        return items, total

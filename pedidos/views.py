# =========================================================
# IMPORTACIONES
# =========================================================

# Decimal permite manejar valores monetarios.
from decimal import Decimal

# Sistema de mensajes de Django.
from django.contrib import messages

# Protección de vistas.
from django.contrib.auth.decorators import (
    login_required,
)

# Excepción utilizada cuando un usuario
# autenticado no tiene autorización.
from django.core.exceptions import (
    PermissionDenied,
)

# transaction.atomic permitirá que todas
# las operaciones de confirmación se realicen
# como una sola transacción.
from django.db import transaction

# Sum permite generar reportes agrupados.
from django.db.models import Sum

# Funciones auxiliares.
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)

# Permite aceptar solamente solicitudes POST
# en operaciones que modifican información.
from django.views.decorators.http import (
    require_POST,
)

# Carrito.
from .carrito import Carrito

# Formulario del reporte.
from .forms import ReporteFiltroForm

# Modelos.
from .models import (
    DetallePedido,
    Pedido,
    Producto,
)


# =========================================================
# INICIO
# =========================================================

@login_required
def inicio(request):

    return render(
        request,
        "inicio.html",
    )


# =========================================================
# TIENDA
# =========================================================

@login_required
def tienda(request):

    # Solo mostramos productos activos.
    productos = (
        Producto.objects
        .filter(activo=True)
        .select_related("categoria")
        .order_by("nombre")
    )

    return render(
        request,
        "tienda/lista.html",
        {
            "productos": productos,
        },
    )


# =========================================================
# MOSTRAR CARRITO
# =========================================================

@login_required
def ver_carrito(request):

    carrito = Carrito(request)

    items, total = (
        carrito.obtener_items()
    )

    return render(
        request,
        "carrito/ver.html",
        {
            "items": items,
            "total": total,
        },
    )


# =========================================================
# AGREGAR PRODUCTO
# =========================================================

@login_required
@require_POST
def agregar_producto(
    request,
    producto_id,
):

    # Solo pueden agregarse productos activos.
    producto = get_object_or_404(
        Producto,
        id=producto_id,
        activo=True,
    )

    carrito = Carrito(request)

    agregado = carrito.agregar(
        producto
    )

    if agregado:

        messages.success(
            request,
            f"{producto.nombre} "
            "fue agregado al carrito.",
        )

    else:

        messages.error(
            request,
            f"No es posible agregar más "
            f"unidades de {producto.nombre}.",
        )

    # La misma operación puede ejecutarse
    # desde Tienda o desde Carrito.
    origen = request.POST.get(
        "origen"
    )

    if origen == "carrito":

        return redirect(
            "ver_carrito"
        )

    return redirect(
        "tienda"
    )


# =========================================================
# RESTAR PRODUCTO
# =========================================================

@login_required
@require_POST
def restar_producto(
    request,
    producto_id,
):

    producto = get_object_or_404(
        Producto,
        id=producto_id,
    )

    carrito = Carrito(request)

    carrito.restar(
        producto
    )

    return redirect(
        "ver_carrito"
    )


# =========================================================
# ELIMINAR PRODUCTO
# =========================================================

@login_required
@require_POST
def eliminar_producto(
    request,
    producto_id,
):

    producto = get_object_or_404(
        Producto,
        id=producto_id,
    )

    carrito = Carrito(request)

    carrito.eliminar(
        producto
    )

    messages.success(
        request,
        f"{producto.nombre} "
        "fue eliminado del carrito.",
    )

    return redirect(
        "ver_carrito"
    )


# =========================================================
# VACIAR CARRITO
# =========================================================

@login_required
@require_POST
def vaciar_carrito(request):

    carrito = Carrito(request)

    carrito.limpiar()

    messages.success(
        request,
        "El carrito fue vaciado.",
    )

    return redirect(
        "ver_carrito"
    )


# =========================================================
# CONFIRMAR PEDIDO
# =========================================================

@login_required
@require_POST
def confirmar_pedido(request):

    carrito = Carrito(request)

    items, _ = (
        carrito.obtener_items()
    )

    # ---------------------------------------------
    # VALIDAR CARRITO VACÍO
    # ---------------------------------------------

    if not items:

        messages.warning(
            request,
            "No existen productos "
            "en el carrito.",
        )

        return redirect(
            "tienda"
        )


    # =====================================================
    # TRANSACCIÓN
    # =====================================================

    # Todas las operaciones siguientes deben
    # completarse correctamente.
    #
    # Si ocurre un error, Django puede revertir
    # los cambios realizados dentro del bloque.
    with transaction.atomic():

        # Primero validamos TODOS los productos
        # antes de crear el pedido.
        productos_confirmados = {}


        for item in items:

            producto_original = (
                item["producto"]
            )

            # Volvemos a consultar el producto
            # directamente desde la base.
            producto = get_object_or_404(
                Producto,
                id=producto_original.id,
                activo=True,
            )

            cantidad = (
                item["cantidad"]
            )

            # -----------------------------------------
            # VALIDAR STOCK
            # -----------------------------------------

            if producto.stock < cantidad:

                messages.error(
                    request,
                    f"No existe suficiente stock "
                    f"para {producto.nombre}. "
                    f"Disponible: {producto.stock}.",
                )

                return redirect(
                    "ver_carrito"
                )

            productos_confirmados[
                producto.id
            ] = producto


        # ---------------------------------------------
        # CREAR PEDIDO
        # ---------------------------------------------

        pedido = Pedido.objects.create(

            usuario=request.user,

            total=Decimal("0.00"),

            estado=Pedido.Estado.PENDIENTE,

        )


        total_pedido = Decimal(
            "0.00"
        )


        # ---------------------------------------------
        # CREAR DETALLES
        # ---------------------------------------------

        for item in items:

            producto = (
                productos_confirmados[
                    item["producto"].id
                ]
            )

            cantidad = (
                item["cantidad"]
            )

            # Precio actual.
            precio = (
                producto.precio
            )

            # Subtotal.
            subtotal = (
                precio * cantidad
            )


            # Crear detalle del pedido.
            DetallePedido.objects.create(

                pedido=pedido,

                producto=producto,

                cantidad=cantidad,

                precio_unitario=precio,

            )


            # -----------------------------------------
            # REDUCIR STOCK
            # -----------------------------------------

            producto.stock -= cantidad

            producto.save(
                update_fields=[
                    "stock"
                ]
            )


            # Acumular total.
            total_pedido += subtotal


        # ---------------------------------------------
        # GUARDAR TOTAL
        # ---------------------------------------------

        pedido.total = total_pedido

        pedido.save(
            update_fields=[
                "total"
            ]
        )


    # =====================================================
    # VACIAR CARRITO
    # =====================================================

    carrito.limpiar()


    # =====================================================
    # MENSAJE DE ÉXITO
    # =====================================================

    messages.success(
        request,
        f"Pedido #{pedido.id} "
        "registrado correctamente.",
    )


    # Mostrar inmediatamente
    # el pedido creado.
    return redirect(
        "detalle_pedido",
        pedido_id=pedido.id,
    )


# =========================================================
# MIS PEDIDOS
# =========================================================

@login_required
def mis_pedidos(request):

    pedidos = (
        Pedido.objects
        .filter(
            usuario=request.user
        )
        .order_by("-fecha")
    )

    return render(
        request,
        "pedidos/mis_pedidos.html",
        {
            "pedidos": pedidos,
        },
    )


# =========================================================
# DETALLE DEL PEDIDO
# =========================================================

@login_required
def detalle_pedido(
    request,
    pedido_id,
):

    # El pedido debe cumplir DOS condiciones:
    #
    # - tener el identificador solicitado;
    # - pertenecer al usuario autenticado.
    pedido = get_object_or_404(

        Pedido,

        id=pedido_id,

        usuario=request.user,

    )

    detalles = (
        pedido.detalles
        .select_related("producto")
        .all()
    )

    return render(
        request,
        "pedidos/detalle.html",
        {
            "pedido": pedido,
            "detalles": detalles,
        },
    )


# =========================================================
# REPORTES
# =========================================================

@login_required
def reportes(request):

    # ---------------------------------------------
    # AUTORIZACIÓN
    # ---------------------------------------------

    # El usuario debe estar autenticado
    # Y además ser administrador/staff.
    if not request.user.is_staff:

        raise PermissionDenied


    # ---------------------------------------------
    # FORMULARIO
    # ---------------------------------------------

    form = ReporteFiltroForm(
        request.GET or None
    )


    # Inicialmente recuperamos todos los pedidos.
    pedidos = Pedido.objects.all()


    # ---------------------------------------------
    # APLICAR FILTROS
    # ---------------------------------------------

    if form.is_valid():

        fecha_desde = (
            form.cleaned_data.get(
                "fecha_desde"
            )
        )

        fecha_hasta = (
            form.cleaned_data.get(
                "fecha_hasta"
            )
        )

        estado = (
            form.cleaned_data.get(
                "estado"
            )
        )


        if fecha_desde:

            pedidos = pedidos.filter(
                fecha__date__gte=fecha_desde
            )


        if fecha_hasta:

            pedidos = pedidos.filter(
                fecha__date__lte=fecha_hasta
            )


        if estado:

            pedidos = pedidos.filter(
                estado=estado
            )


    # =====================================================
    # INDICADORES
    # =====================================================

    cantidad_pedidos = (
        pedidos.count()
    )


    # Para ventas no consideraremos
    # pedidos cancelados.
    pedidos_validos = (
        pedidos.exclude(
            estado=Pedido.Estado.CANCELADO
        )
    )


    # ---------------------------------------------
    # TOTAL DE VENTAS
    # ---------------------------------------------

    resultado_ventas = (
        pedidos_validos.aggregate(
            total_ventas=Sum("total")
        )
    )

    total_ventas = (
        resultado_ventas[
            "total_ventas"
        ]
        or Decimal("0.00")
    )


    # ---------------------------------------------
    # UNIDADES VENDIDAS
    # ---------------------------------------------

    detalles_validos = (
        DetallePedido.objects.filter(
            pedido__in=pedidos_validos
        )
    )

    resultado_unidades = (
        detalles_validos.aggregate(
            total_unidades=Sum(
                "cantidad"
            )
        )
    )

    unidades_vendidas = (
        resultado_unidades[
            "total_unidades"
        ]
        or 0
    )


    # =====================================================
    # PRODUCTOS MÁS SOLICITADOS
    # =====================================================

    productos_grafico = list(

        detalles_validos

        .values(
            "producto__nombre"
        )

        .annotate(
            cantidad_total=Sum(
                "cantidad"
            )
        )

        .order_by(
            "-cantidad_total"
        )[:10]

    )


    # Producto más solicitado.
    if productos_grafico:

        producto_top_nombre = (
            productos_grafico[0][
                "producto__nombre"
            ]
        )

        producto_top_cantidad = (
            productos_grafico[0][
                "cantidad_total"
            ]
        )

    else:

        producto_top_nombre = (
            "Sin información"
        )

        producto_top_cantidad = 0


    # =====================================================
    # DATOS PARA CHART.JS
    # =====================================================

    grafico_labels = [

        producto[
            "producto__nombre"
        ]

        for producto
        in productos_grafico

    ]


    grafico_datos = [

        producto[
            "cantidad_total"
        ]

        for producto
        in productos_grafico

    ]


    # Últimos pedidos filtrados.
    pedidos_tabla = (
        pedidos
        .select_related("usuario")
        .order_by("-fecha")[:50]
    )


    return render(
        request,
        "reportes/reporte.html",
        {
            "form": form,

            "cantidad_pedidos":
                cantidad_pedidos,

            "total_ventas":
                total_ventas,

            "unidades_vendidas":
                unidades_vendidas,

            "producto_top_nombre":
                producto_top_nombre,

            "producto_top_cantidad":
                producto_top_cantidad,

            "grafico_labels":
                grafico_labels,

            "grafico_datos":
                grafico_datos,

            "pedidos_tabla":
                pedidos_tabla,
        },
    )

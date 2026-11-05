# =========================================================
# IMPORTACIONES
# =========================================================

# Decorador que obliga al usuario a iniciar sesión
# antes de poder utilizar una vista.
from django.contrib.auth.decorators import login_required

# get_object_or_404 permite buscar un objeto.
# Si el objeto no existe o no pertenece al usuario,
# Django mostrará un error 404.
from django.shortcuts import get_object_or_404, render

# Importamos los modelos que utilizaremos.
from .models import Pedido, Producto


# =========================================================
# VISTA: INICIO
# =========================================================

# Solo los usuarios autenticados pueden ingresar.
@login_required
def inicio(request):

    # Mostramos la página principal del sistema.
    return render(
        request,
        "inicio.html",
    )


# =========================================================
# VISTA: TIENDA
# =========================================================

@login_required
def tienda(request):

    # Consultamos únicamente productos activos.
    #
    # select_related("categoria") permite obtener
    # también la información de la categoría
    # relacionada con cada producto.
    productos = (
        Producto.objects
        .filter(activo=True)
        .select_related("categoria")
        .order_by("nombre")
    )

    # Enviamos los productos al template.
    return render(
        request,
        "tienda/lista.html",
        {
            "productos": productos,
        },
    )


# =========================================================
# VISTA: MIS PEDIDOS
# =========================================================

@login_required
def mis_pedidos(request):

    # request.user representa al usuario
    # que actualmente inició sesión.
    #
    # Filtramos para mostrar únicamente
    # los pedidos pertenecientes a ese usuario.
    pedidos = (
        Pedido.objects
        .filter(usuario=request.user)
        .order_by("-fecha")
    )

    # Enviamos los pedidos al template.
    return render(
        request,
        "pedidos/mis_pedidos.html",
        {
            "pedidos": pedidos,
        },
    )


# =========================================================
# VISTA: DETALLE DEL PEDIDO
# =========================================================

@login_required
def detalle_pedido(request, pedido_id):

    # Buscamos el pedido utilizando DOS condiciones:
    #
    # 1. Debe tener el identificador solicitado.
    # 2. Debe pertenecer al usuario autenticado.
    #
    # Esto evita que un usuario pueda consultar
    # pedidos pertenecientes a otro usuario
    # modificando manualmente la URL.
    pedido = get_object_or_404(
        Pedido,
        id=pedido_id,
        usuario=request.user,
    )

    # Recuperamos los productos correspondientes
    # al pedido mediante la relación DetallePedido.
    detalles = (
        pedido.detalles
        .select_related("producto")
        .all()
    )

    # Enviamos pedido y detalles al template.
    return render(
        request,
        "pedidos/detalle.html",
        {
            "pedido": pedido,
            "detalles": detalles,
        },
    )

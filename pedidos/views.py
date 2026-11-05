# Decorador utilizado para proteger vistas.
from django.contrib.auth.decorators import login_required

# Función para renderizar templates.
from django.shortcuts import render


# =========================================================
# VISTA PRINCIPAL
# =========================================================

# Esta vista solo puede ser utilizada
# por usuarios autenticados.
@login_required
def inicio(request):

    # Mostramos el template inicio.html.
    return render(
        request,
        "inicio.html",
    )

# Importamos path para definir las rutas.
from django.urls import path

# Importamos las vistas de la aplicación.
from . import views


urlpatterns = [

    # Módulo principal después del inicio de sesión.
    path(
        "inicio/",
        views.inicio,
        name="inicio",
    ),

]

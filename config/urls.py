# Configuración general.
from django.conf import settings

# Permite mostrar archivos MEDIA durante desarrollo.
from django.conf.urls.static import static

# Panel administrativo.
from django.contrib import admin

# Vistas incorporadas de autenticación.
from django.contrib.auth import views as auth_views

# include permite incorporar las URLs de la app pedidos.
from django.urls import include, path

# Permite redireccionar la URL raíz.
from django.views.generic import RedirectView


urlpatterns = [

    # =====================================================
    # URL PRINCIPAL
    # =====================================================

    # Cuando el usuario ingrese a:
    # http://127.0.0.1:8000/
    #
    # será enviado automáticamente al login.
    path(
        "",
        RedirectView.as_view(
            pattern_name="login",
            permanent=False,
        ),
        name="raiz",
    ),


    # =====================================================
    # AUTENTICACIÓN
    # =====================================================

    # Pantalla para iniciar sesión.
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="registration/login.html"
        ),
        name="login",
    ),

    # Cierre de sesión.
    # LogoutView trabaja mediante una solicitud POST
    # desde el formulario que crearemos en base.html.
    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),


    # =====================================================
    # ADMINISTRACIÓN
    # =====================================================

    path(
        "admin/",
        admin.site.urls,
    ),


    # =====================================================
    # APLICACIÓN PEDIDOS
    # =====================================================

    # Incorporamos las URLs declaradas en pedidos/urls.py.
    path(
        "",
        include("pedidos.urls"),
    ),
]


# =========================================================
# ARCHIVOS MEDIA
# =========================================================

# Durante desarrollo permitimos que Django muestre
# las imágenes cargadas desde la carpeta media.
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )

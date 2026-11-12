# =========================================================
# PRUEBAS AUTOMÁTICAS
# =========================================================

# Modelo de usuario configurado por Django.
from django.contrib.auth import (
    get_user_model,
)

# Herramientas de prueba.
from django.test import TestCase

# Permite obtener URLs por su nombre.
from django.urls import reverse

# Modelo Pedido.
from .models import Pedido


# Recuperamos el modelo de usuario.
User = get_user_model()


class SeguridadSistemaTest(
    TestCase
):

    # =====================================================
    # PREPARACIÓN
    # =====================================================

    def setUp(self):

        # Usuario número 1.
        self.usuario1 = (
            User.objects.create_user(
                username="cliente01",
                password="12345678",
            )
        )

        # Usuario número 2.
        self.usuario2 = (
            User.objects.create_user(
                username="cliente02",
                password="12345678",
            )
        )

        # Administrador.
        self.admin = (
            User.objects.create_user(
                username="adminprueba",
                password="12345678",
                is_staff=True,
            )
        )

        # Pedido perteneciente al usuario 2.
        self.pedido_usuario2 = (
            Pedido.objects.create(
                usuario=self.usuario2,
                total=20,
            )
        )


    # =====================================================
    # PRUEBA 1
    # TIENDA PROTEGIDA
    # =====================================================

    def test_tienda_requiere_login(
        self
    ):

        respuesta = self.client.get(
            reverse("tienda")
        )

        # Django debe redirigir.
        self.assertEqual(
            respuesta.status_code,
            302,
        )


    # =====================================================
    # PRUEBA 2
    # NO VER PEDIDO AJENO
    # =====================================================

    def test_usuario_no_ve_pedido_ajeno(
        self
    ):

        # Iniciamos sesión como usuario1.
        self.client.login(
            username="cliente01",
            password="12345678",
        )

        respuesta = self.client.get(
            reverse(
                "detalle_pedido",
                args=[
                    self.pedido_usuario2.id
                ],
            )
        )

        # Debe devolver 404.
        self.assertEqual(
            respuesta.status_code,
            404,
        )


    # =====================================================
    # PRUEBA 3
    # REPORTES SOLO PARA STAFF
    # =====================================================

    def test_usuario_normal_no_ve_reportes(
        self
    ):

        self.client.login(
            username="cliente01",
            password="12345678",
        )

        respuesta = self.client.get(
            reverse("reportes")
        )

        # PermissionDenied devuelve 403.
        self.assertEqual(
            respuesta.status_code,
            403,
        )


    # =====================================================
    # PRUEBA 4
    # ADMINISTRADOR SÍ VE REPORTES
    # =====================================================

    def test_admin_ve_reportes(
        self
    ):

        self.client.login(
            username="adminprueba",
            password="12345678",
        )

        respuesta = self.client.get(
            reverse("reportes")
        )

        self.assertEqual(
            respuesta.status_code,
            200,
        )

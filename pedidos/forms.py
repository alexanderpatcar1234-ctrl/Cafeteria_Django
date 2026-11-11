# =========================================================
# FORMULARIOS DEL SISTEMA
# =========================================================

# Importamos el sistema de formularios de Django.
from django import forms

# Importamos Pedido para obtener
# automáticamente sus estados.
from .models import Pedido


# =========================================================
# FORMULARIO PARA FILTRAR REPORTES
# =========================================================

class ReporteFiltroForm(forms.Form):

    # Fecha inicial.
    #
    # required=False significa que el filtro
    # puede quedar vacío.
    fecha_desde = forms.DateField(
        required=False,
        label="Desde",
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "form-control",
            }
        ),
    )

    # Fecha final.
    fecha_hasta = forms.DateField(
        required=False,
        label="Hasta",
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "form-control",
            }
        ),
    )

    # Estado del pedido.
    #
    # Agregamos primero una opción vacía
    # para representar "Todos".
    estado = forms.ChoiceField(
        required=False,
        label="Estado",
        choices=[
            ("", "Todos"),
            *Pedido.Estado.choices,
        ],
        widget=forms.Select(
            attrs={
                "class": "form-select",
            }
        ),
    )

    # =====================================================
    # VALIDACIÓN DEL FORMULARIO
    # =====================================================

    def clean(self):

        # Ejecutamos primero las validaciones
        # proporcionadas por Django.
        datos = super().clean()

        fecha_desde = datos.get("fecha_desde")

        fecha_hasta = datos.get("fecha_hasta")

        # Comprobamos que la fecha inicial
        # no sea posterior a la fecha final.
        if (
            fecha_desde
            and fecha_hasta
            and fecha_desde > fecha_hasta
        ):

            raise forms.ValidationError(
                "La fecha inicial no puede ser "
                "posterior a la fecha final."
            )

        return datos

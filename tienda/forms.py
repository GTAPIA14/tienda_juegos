from django import forms


class PedidoForm(forms.Form):

    nombre_cliente = forms.CharField(
        max_length=150,
        label="Nombre completo",
        widget=forms.TextInput(attrs={
            'class': 'campo',
            'placeholder': 'Ingresa tu nombre completo'
        })
    )

    correo = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={
            'class': 'campo',
            'placeholder': 'ejemplo@correo.com'
        })
    )

    telefono = forms.CharField(
        max_length=20,
        label="Teléfono",
        widget=forms.TextInput(attrs={
            'class': 'campo',
            'placeholder': 'Ingresa tu teléfono'
        })
    )

    cantidad = forms.IntegerField(
        min_value=1,
        max_value=5,
        label="Cantidad de unidades",
        widget=forms.NumberInput(attrs={
            'class': 'campo',
            'min': 1,
            'max': 5
        })
    )

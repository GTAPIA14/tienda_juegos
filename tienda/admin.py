from django.contrib import admin
from django.utils.html import format_html
from .models import Categoria, Juego, Pedido


# ==========================================
# ADMINISTRACION DE CATEGORIAS
# ==========================================

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):

    list_display = ('id', 'nombre')
    search_fields = ('nombre',)
    ordering = ('nombre',)


# ==========================================
# ADMINISTRACION DE JUEGOS
# ==========================================

@admin.register(Juego)
class JuegoAdmin(admin.ModelAdmin):

    list_display = (
        'nombre',
        'categoria',
        'precio_formateado',
        'stock',
        'disponible',
        'mostrar_imagen'
    )

    list_filter = ('categoria', 'disponible')

    search_fields = ('nombre',)

    list_per_page = 10

    def precio_formateado(self, obj):
        return f"${obj.precio:,.0f}".replace(",", ".")

    precio_formateado.short_description = "Precio (CLP)"

    def mostrar_imagen(self, obj):
        if obj.imagen:
            return format_html(
                '<img src="{}" width="50" height="50" '
                'style="object-fit:contain;" />',
                obj.imagen.url
            )
        return "Sin imagen"

    mostrar_imagen.short_description = "Imagen"


# ==========================================
# ADMINISTRACION DE PEDIDOS
# ==========================================

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):

    list_display = (
        'codigo',
        'juego',
        'nombre_cliente',
        'cantidad',
        'fecha_pedido'
    )

    list_filter = ('juego',)

    search_fields = (
        'nombre_cliente',
        'correo'
    )

    list_per_page = 10

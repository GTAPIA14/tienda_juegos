
from django.shortcuts import render, get_object_or_404, redirect
from django.db import transaction

from .models import Juego, Categoria, Pedido
from .forms import PedidoForm


# ==========================================
# CATALOGO PUBLICO
# ==========================================

def inicio(request):

    juegos = Juego.objects.filter(disponible=True)

    busqueda = request.GET.get('buscar', '')
    categoria_id = request.GET.get('categoria', '')

    if busqueda:
        juegos = juegos.filter(nombre__icontains=busqueda)

    if categoria_id:
        juegos = juegos.filter(categoria_id=categoria_id)

    categorias = Categoria.objects.all()

    contexto = {
        'juegos': juegos,
        'categorias': categorias,
        'busqueda': busqueda,
        'categoria_seleccionada': categoria_id,
    }

    return render(request, 'tienda/inicio.html', contexto)


# ==========================================
# DETALLE Y FORMULARIO DE PEDIDO
# ==========================================

def detalle_juego(request, juego_id):

    juego = get_object_or_404(
        Juego,
        id=juego_id,
        disponible=True
    )

    form = PedidoForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():

        cantidad = form.cleaned_data['cantidad']

        with transaction.atomic():

            # Consultar nuevamente el juego y bloquearlo
            juego_actual = get_object_or_404(
                Juego.objects.select_for_update(),
                id=juego_id,
                disponible=True
            )

            if juego_actual.stock == 0:

                form.add_error(
                    'cantidad',
                    'Este juego se encuentra agotado.'
                )

            elif cantidad > juego_actual.stock:

                form.add_error(
                    'cantidad',
                    f'Solo quedan {juego_actual.stock} unidades disponibles.'
                )

            else:

                # Crear el pedido
                pedido = Pedido.objects.create(
                    juego=juego_actual,
                    nombre_cliente=form.cleaned_data['nombre_cliente'],
                    correo=form.cleaned_data['correo'],
                    telefono=form.cleaned_data['telefono'],
                    cantidad=cantidad,
                    precio_unitario=juego_actual.precio
                )

                # Descontar el stock
                juego_actual.stock -= cantidad

                juego_actual.save(
                    update_fields=['stock']
                )

                # Redirigir al comprobante
                return redirect(
                    'comprobante',
                    codigo=pedido.codigo
                )

        juego.refresh_from_db()

    contexto = {
        'juego': juego,
        'form': form,
    }

    return render(
        request,
        'tienda/detalle.html',
        contexto
    )


# ==========================================
# COMPROBANTE DEL PEDIDO
# ==========================================

def comprobante(request, codigo):

    pedido = get_object_or_404(
        Pedido,
        codigo=codigo
    )

    contexto = {
        'pedido': pedido,
        'total': pedido.total,
    }

    return render(
        request,
        'tienda/comprobante.html',
        contexto
    )

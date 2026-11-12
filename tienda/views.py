from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Juego, Categoria


# ==========================================
# CATALOGO PUBLICO
# ==========================================

def inicio(request):

    juegos = Juego.objects.filter(disponible=True)

    # Busqueda por nombre
    busqueda = request.GET.get('buscar', '')

    if busqueda:
        juegos = juegos.filter(nombre__icontains=busqueda)

    # Filtro por categoria
    categoria_id = request.GET.get('categoria', '')

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
# DETALLE DE JUEGO
# ==========================================

def detalle_juego(request, juego_id):

    juego = get_object_or_404(
        Juego,
        id=juego_id,
        disponible=True
    )

    return render(
        request,
        'tienda/detalle.html',
        {'juego': juego}
    )

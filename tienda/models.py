from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid


# ==========================================
# MODELO: CATEGORIA
# ==========================================

class Categoria(models.Model):

    nombre = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nombre de categoría"
    )

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ["nombre"]


# ==========================================
# MODELO: JUEGO
# ==========================================

class Juego(models.Model):

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        related_name="juegos",
        verbose_name="Categoría"
    )

    nombre = models.CharField(
        max_length=150,
        verbose_name="Nombre del juego"
    )

    descripcion = models.TextField(
        verbose_name="Descripción"
    )

    imagen = models.ImageField(
        upload_to="juegos/",
        verbose_name="Imagen de la caja"
    )

    precio = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="Precio en pesos chilenos"
    )

    cantidad_jugadores = models.CharField(
        max_length=50,
        verbose_name="Cantidad de jugadores"
    )

    edad_minima = models.PositiveSmallIntegerField(
        verbose_name="Edad mínima recomendada"
    )

    stock = models.PositiveIntegerField(
        default=0,
        verbose_name="Stock disponible"
    )

    disponible = models.BooleanField(
        default=True,
        verbose_name="Disponible para la venta"
    )

    # FORMATO DE PRECIO CHILENO
    @property
    def precio_formateado(self):
        return f"${self.precio:,.0f}".replace(",", ".")

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Juego"
        verbose_name_plural = "Juegos"
        ordering = ["nombre"]


# ==========================================
# MODELO: PEDIDO
# ==========================================

class Pedido(models.Model):

    codigo = models.CharField(
        max_length=12,
        unique=True,
        editable=False,
        verbose_name="Código del pedido"
    )

    juego = models.ForeignKey(
        Juego,
        on_delete=models.CASCADE,
        related_name="pedidos",
        verbose_name="Juego solicitado"
    )

    nombre_cliente = models.CharField(
        max_length=150,
        verbose_name="Nombre del cliente"
    )

    correo = models.EmailField(
        verbose_name="Correo electrónico"
    )

    telefono = models.CharField(
        max_length=20,
        verbose_name="Teléfono"
    )

    cantidad = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ],
        verbose_name="Cantidad de unidades"
    )

    fecha_pedido = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha y hora del pedido"
    )

    def save(self, *args, **kwargs):
        if not self.codigo:
            self.codigo = uuid.uuid4().hex[:12].upper()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.codigo} - {self.nombre_cliente}"

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ["-fecha_pedido"]

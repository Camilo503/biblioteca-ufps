from django.db import models
from django.db.models import Q


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre


class Autor(models.Model):
    nombre = models.CharField(max_length=150)

    class Meta:
        verbose_name_plural = "autores"

    def __str__(self):
        return self.nombre


class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    anio_publicacion = models.IntegerField()
    isbn = models.CharField(max_length=17, unique=True)
    categoria = models.ForeignKey(
        Categoria, on_delete=models.PROTECT, related_name="libros"
    )
    autores = models.ManyToManyField(Autor, related_name="libros")
    idioma = models.CharField(max_length=30, default="Español")

    def __str__(self):
        return f"{self.titulo} ({self.anio_publicacion})"


class Ejemplar(models.Model):
    class Condicion(models.TextChoices):
        NUEVO = "nuevo", "Nuevo"
        USADO = "usado", "Usado"
        DANADO = "danado", "Dañado"

    libro = models.ForeignKey(
        Libro, on_delete=models.PROTECT, related_name="ejemplares"
    )
    codigo_inventario = models.CharField(max_length=30, unique=True)
    condicion = models.CharField(
        max_length=10, choices=Condicion.choices, default=Condicion.NUEVO
    )

    class Meta:
        verbose_name_plural = "ejemplares"

    def __str__(self):
        return f"{self.codigo_inventario} · {self.libro.titulo}"


class Estudiante(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=150)
    correo = models.EmailField()

    def __str__(self):
        return f"{self.codigo} · {self.nombre}"


class Prestamo(models.Model):
    ejemplar = models.ForeignKey(
        Ejemplar, on_delete=models.PROTECT, related_name="prestamos"
    )
    estudiante = models.ForeignKey(
        Estudiante, on_delete=models.PROTECT, related_name="prestamos"
    )
    fecha_prestamo = models.DateField(auto_now_add=True)
    fecha_limite = models.DateField()
    fecha_devolucion_real = models.DateField(null=True, blank=True)

    class Meta:
        constraints = [
            # Solo puede haber UN préstamo sin devolver por cada ejemplar.
            models.UniqueConstraint(
                fields=["ejemplar"],
                condition=Q(fecha_devolucion_real__isnull=True),
                name="un_prestamo_activo_por_ejemplar",
            )
        ]

    def __str__(self):
        return f"{self.ejemplar.codigo_inventario} → {self.estudiante.nombre}"

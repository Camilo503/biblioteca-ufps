from django.contrib import admin
from django.utils import timezone
from .models import Autor, Categoria, Ejemplar, Estudiante, Libro, Prestamo


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre",)
    search_fields = ("nombre",)


@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ("nombre",)
    search_fields = ("nombre",)


class EjemplarInline(admin.TabularInline):
    model = Ejemplar
    extra = 1


@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ("titulo", "anio_publicacion", "isbn", "categoria", "idioma")
    search_fields = ("titulo", "isbn", "autores__nombre")
    list_filter = ("categoria", "anio_publicacion")
    inlines = [EjemplarInline]


@admin.register(Ejemplar)
class EjemplarAdmin(admin.ModelAdmin):
    list_display = ("codigo_inventario", "libro", "condicion")
    # search_fields es obligatorio para poder usar autocomplete desde Prestamo
    search_fields = ("codigo_inventario", "libro__titulo")
    list_filter = ("condicion",)


@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ("codigo", "nombre", "correo")
    search_fields = ("codigo", "nombre")


@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = ("ejemplar", "estudiante", "fecha_prestamo",
                    "fecha_limite", "fecha_devolucion_real", "sin_devolver")
    search_fields = ("estudiante__codigo", "estudiante__nombre",
                     "ejemplar__codigo_inventario", "ejemplar__libro__titulo")
    list_filter = ("fecha_devolucion_real", "fecha_limite")
    readonly_fields = ("fecha_prestamo",)
    autocomplete_fields = ("ejemplar", "estudiante")
    actions = ["marcar_devueltos"]

    @admin.display(boolean=True, description="¿Sin devolver?")
    def sin_devolver(self, obj):
        return obj.fecha_devolucion_real is None

    @admin.action(description="Marcar préstamos seleccionados como devueltos")
    def marcar_devueltos(self, request, queryset):
        n = queryset.filter(fecha_devolucion_real__isnull=True).update(
            fecha_devolucion_real=timezone.localdate()
        )
        self.message_user(request, f"{n} préstamo(s) marcado(s) como devuelto(s).")

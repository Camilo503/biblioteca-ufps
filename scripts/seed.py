"""Datos de prueba. Ejecutar UNA sola vez por base de datos."""
from datetime import date, timedelta
from biblioteca.models import (Autor, Categoria, Ejemplar, Estudiante,
                               Libro, Prestamo)

if Libro.objects.filter(isbn="9780060883287").exists():
    raise SystemExit("Los datos de prueba ya existen. No se creó nada.")

hoy = date.today()

# --- Categorías ---
novela = Categoria.objects.create(nombre="Novela")
ingenieria = Categoria.objects.create(nombre="Ingeniería")
historia = Categoria.objects.create(nombre="Historia")

# --- Autores ---
garcia = Autor.objects.create(nombre="Gabriel García Márquez")
martin = Autor.objects.create(nombre="Robert C. Martin")
hobsbawm = Autor.objects.create(nombre="Eric Hobsbawm")
beck = Autor.objects.create(nombre="Kent Beck")


def crear_libro(titulo, anio, isbn, categoria, autores):
    libro = Libro.objects.create(
        titulo=titulo, anio_publicacion=anio, isbn=isbn, categoria=categoria
    )
    libro.autores.add(*autores)
    return libro


# --- Libros (5) ---
l1 = crear_libro("Cien años de soledad", 1967, "9780060883287", novela, [garcia])
l2 = crear_libro("El amor en los tiempos del cólera", 1985, "9780307389732",
                 novela, [garcia])
l3 = crear_libro("Clean Code", 2008, "9780132350884", ingenieria, [martin])
l4 = crear_libro("Test Driven Development", 2002, "9780321146533",
                 ingenieria, [beck, martin])   # dos autores, para probar M2M
l5 = crear_libro("La era de la revolución", 1962, "9788498922974",
                 historia, [hobsbawm])

# --- Ejemplares (8): INV-001 a INV-008 ---
copias_de = [l1, l1, l2, l3, l3, l4, l5, l5]
ej = [
    Ejemplar.objects.create(libro=libro, codigo_inventario=f"INV-{i:03d}")
    for i, libro in enumerate(copias_de, start=1)
]

# --- Estudiantes (4) ---
datos_est = [
    ("1150001", "Ana Pérez", "ana.perez@ufps.edu.co"),
    ("1150002", "Luis Gómez", "luis.gomez@ufps.edu.co"),
    ("1150003", "Marta Ruiz", "marta.ruiz@ufps.edu.co"),
    ("1150004", "Pedro Díaz", "pedro.diaz@ufps.edu.co"),   # nunca presta
]
est = [Estudiante.objects.create(codigo=c, nombre=n, correo=m)
       for c, n, m in datos_est]


def prestar(ejemplar, estudiante, dias_limite, devuelto):
    p = Prestamo.objects.create(
        ejemplar=ejemplar, estudiante=estudiante,
        fecha_limite=hoy + timedelta(days=dias_limite),
    )
    if devuelto:
        p.fecha_devolucion_real = hoy
        p.save()


# --- Préstamos (6) ---
prestar(ej[0], est[0], 7, True)     # INV-001 Ana, devuelto
prestar(ej[0], est[1], 7, True)     # INV-001 Luis, devuelto (historial)
prestar(ej[2], est[0], 7, False)    # INV-003 Ana, ACTIVO
prestar(ej[3], est[1], -3, False)   # INV-004 Luis, ACTIVO y vencido
prestar(ej[5], est[2], 7, True)     # INV-006 Marta, devuelto
prestar(ej[6], est[0], 7, False)    # INV-007 Ana, ACTIVO

print("Listo:", Libro.objects.count(), "libros,", Autor.objects.count(),
      "autores,", Ejemplar.objects.count(), "copias,",
      Estudiante.objects.count(), "estudiantes,",
      Prestamo.objects.count(), "préstamos.")

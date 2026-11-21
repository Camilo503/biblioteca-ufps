# Diseño de datos

## Lista 1 · Entidades

- Categoría
- Autor
- Libro
- Ejemplar (la copia física)
- Estudiante
- Préstamo

Son 6 modelos.

## Lista 2 · Campos

| Modelo | Campos |
|---|---|
| Categoria | nombre (único) |
| Autor | nombre |
| Libro | titulo, anio_publicacion, isbn (único) |
| Ejemplar | codigo_inventario (único), condicion (nuevo/usado/dañado) |
| Estudiante | codigo (único), nombre, correo |
| Prestamo | fecha_prestamo, fecha_limite, fecha_devolucion_real (puede estar vacía) |

## Lista 3 · Relaciones

| Modelo | Relaciones |
|---|---|
| Categoria | Una categoría tiene muchos libros. Un libro pertenece a una sola categoría. |
| Autor | Muchos a muchos con Libro: un libro puede tener varios autores y un autor varios libros. |
| Libro | ForeignKey a Categoria (muchos libros → 1 categoría). ManyToManyField a Autor. |
| Ejemplar | ForeignKey a Libro: un libro tiene muchas copias físicas. |
| Estudiante | Ninguna directa; se relaciona a través de Préstamo. |
| Prestamo | ForeignKey a Ejemplar y a Estudiante. Se presta una copia física, no el libro abstracto. |

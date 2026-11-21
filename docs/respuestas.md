Respuestas de la Fase 1

1. ¿Cuál es la diferencia entre un proyecto y una app en Django?
El proyecto (`config`) es la configuración global: los ajustes, las URLs raíz y qué apps están activas. Una app (`biblioteca`) es un módulo con una responsabilidad concreta: sus modelos, vistas, admin y pruebas. Un proyecto contiene muchas apps, y una app se puede reutilizar en otros proyectos.

2. ¿Qué pasa si se crea una app y no se registra en INSTALLED_APPS?
Django no la reconoce: no ve sus modelos, `makemigrations` responde «No changes detected», no aparece en el admin y no se cargan sus plantillas.

3. ¿Para qué sirve manage.py?
Es el comando de entrada del proyecto: permite correr el servidor, aplicar migraciones, abrir el shell, crear superusuarios, etc. A diferencia de `django-admin`, que se usa una vez para crear el proyecto, `manage.py` ya conoce la configuración de este proyecto.

4. ¿Por qué no se sube db.sqlite3 a Git?
Es un archivo binario que cambia con cada prueba y produce conflictos que no se pueden fusionar. Además puede contener datos personales y contraseñas (con hash). Cada persona puede reconstruirla con `migrate` y los datos de prueba, así que no hace falta compartirla.
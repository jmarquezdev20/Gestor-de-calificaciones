
Gestor de Calificaciones

Gestor de Calificaciones: es una aplicación de escritorio desarrollada en Python con Tkinter y SQLite, diseñada para administrar estudiantes, materias y calificaciones escolares de forma local.  

Permite registrar alumnos, asignar materias, registrar notas por periodo y generar boletines en PDF automáticamente.

Características principales:

Gestión de estudiantes: Registrar, editar y eliminar alumnos fácilmente con control de identificación y grado académico.

Gestión de materias: Crear materias personalizadas con cantidad configurable de notas (1 a 10).

Gestión de calificaciones: Visualización tipo “matriz” que muestra estudiantes vs. materias.  
Permite ingresar notas por periodo académico, con promedio automático e indicador visual de aprobación o reprobación.

Periodos académicos: Soporta hasta 4 periodos configurables para registrar calificaciones independientes.

Reportes y exportación: Generación de reportes PDF con promedios por estudiante, materia o periodo.

Base de datos local SQLite: No requiere internet. Todos los datos se almacenan en `calificaciones.db` automáticamente.

Requisitos:
Python 3.10 o superior
Librerías incluidas o instalables vía `pip`:
pip install reportlab

Cómo ejecutar la aplicación:

1. Clona o descarga este repositorio.

2. Asegúrate de tener Python instalado.

3. Abre una terminal en la carpeta del proyecto.

Ejecuta:
python main.py

Estructura del proyecto:
Gestor_Calificaciones/
|
├── main.py               # Ventana principal y navegación general
├── students.py           # Gestión de estudiantes
├── materias.py           # Gestión de materias
├── grades.py             # Gestión de calificaciones (matriz visual)
├── reportes.py           # Generación de reportes PDF
├── database.py           # Creación y conexión de la base de datos SQLite
├── calificaciones.db     # Base de datos local (se crea automáticamente)
└── README.md             # Documentación del proyecto

Base de datos:
El sistema utiliza una base de datos SQLite con las siguientes tablas:
estudiantes (id, nombre, apellido, identificacion, grado)
materias (id, nombre, num_notas, descripcion)
calificaciones (id, estudiante_id, materia_id, periodo, nota_num, valor)

La función crear_tablas() (en database.py) asegura que las estructuras estén actualizadas incluso si ya existe una base de datos previa.

Autor

Juan Manuel Marquez
Desarrollado con usando Python + Tkinter + SQLite
Barranquilla, Colombia 🇨🇴

Licencia
Este proyecto se distribuye bajo la licencia MIT.
Eres libre de usarlo, modificarlo y compartirlo.

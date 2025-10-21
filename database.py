import sqlite3

def crear_tablas():
    """Crea o actualiza las tablas necesarias en la base de datos"""
    conn = sqlite3.connect('calificaciones.db')
    cursor = conn.cursor()

    #TABLA ESTUDIANTES
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS estudiantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Asegurar columna 'identificacion'
    cursor.execute("PRAGMA table_info(estudiantes)")
    columnas_est = [col[1] for col in cursor.fetchall()]
    if 'identificacion' not in columnas_est:
        cursor.execute("ALTER TABLE estudiantes ADD COLUMN identificacion TEXT")

    # Asegurar columna 'grado'
    if 'grado' not in columnas_est:
        cursor.execute("ALTER TABLE estudiantes ADD COLUMN grado TEXT")

    #TABLA MATERIAS
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS materias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE
        )
    ''')

    # Asegurar columnas nuevas en 'materias'
    cursor.execute("PRAGMA table_info(materias)")
    columnas_mat = [col[1] for col in cursor.fetchall()]
    if 'num_notas' not in columnas_mat:
        cursor.execute("ALTER TABLE materias ADD COLUMN num_notas INTEGER DEFAULT 3")
    if 'descripcion' not in columnas_mat:
        cursor.execute("ALTER TABLE materias ADD COLUMN descripcion TEXT")

    #TABLA CALIFICACIONES
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS calificaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            estudiante_id INTEGER,
            materia_id INTEGER,
            periodo INTEGER,
            nota_num INTEGER,
            valor REAL,
            FOREIGN KEY (estudiante_id) REFERENCES estudiantes (id),
            FOREIGN KEY (materia_id) REFERENCES materias (id)
        )
    ''')

    conn.commit()
    conn.close()

def conectar():
    """Retorna una conexión a la base de datos"""
    return sqlite3.connect('calificaciones.db')

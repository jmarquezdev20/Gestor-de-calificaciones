import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os
from datetime import datetime

DB_NAME = "calificaciones.db"
BOLETIN_DIR = "boletines"

# BASE DE DATOS
def inicializar_bd():
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS estudiantes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS materias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        cantidad_notas INTEGER NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        estudiante_id INTEGER,
        materia_id INTEGER,
        periodo INTEGER,
        nota REAL,
        FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id),
        FOREIGN KEY (materia_id) REFERENCES materias(id)
    )
    """)

    conexion.commit()
    conexion.close()

#FUNCIONES

def registrar_estudiante():
    nombre = entry_nombre_estudiante.get().strip()
    if not nombre:
        messagebox.showwarning("Atención", "Ingresa un nombre de estudiante")
        return

    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO estudiantes (nombre) VALUES (?)", (nombre,))
    conexion.commit()
    conexion.close()
    entry_nombre_estudiante.delete(0, tk.END)
    actualizar_tablas()
    messagebox.showinfo("Éxito", "Estudiante registrado con éxito")


def registrar_materia():
    nombre = entry_nombre_materia.get().strip()
    try:
        cantidad = int(entry_cantidad_notas.get())
    except ValueError:
        messagebox.showwarning("Atención", "La cantidad de notas debe ser un número")
        return

    if not nombre or cantidad <= 0:
        messagebox.showwarning("Atención", "Completa todos los campos correctamente")
        return

    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO materias (nombre, cantidad_notas) VALUES (?,?)", (nombre, cantidad))
    conexion.commit()
    conexion.close()
    entry_nombre_materia.delete(0, tk.END)
    entry_cantidad_notas.delete(0, tk.END)
    actualizar_tablas()
    messagebox.showinfo("Éxito", "Materia registrada correctamente")


def guardar_nota():
    try:
        estudiante_id = combo_estudiantes.get().split(" - ")[0]
        materia_id = combo_materias.get().split(" - ")[0]
        periodo = int(entry_periodo.get())
        nota = float(entry_nota.get())
    except Exception:
        messagebox.showwarning("Atención", "Verifica los datos ingresados")
        return

    if nota < 0 or nota > 5:
        messagebox.showwarning("Atención", "La nota debe estar entre 0 y 5")
        return

    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO notas (estudiante_id, materia_id, periodo, nota)
        VALUES (?, ?, ?, ?)
    """, (estudiante_id, materia_id, periodo, nota))
    conexion.commit()
    conexion.close()
    entry_nota.delete(0, tk.END)
    messagebox.showinfo("Éxito", "Nota guardada correctamente")
    actualizar_tablas()


def actualizar_tablas():
    for item in tree_notas.get_children():
        tree_notas.delete(item)

    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    cursor.execute("""
    SELECT e.nombre, m.nombre, n.periodo, n.nota
    FROM notas n
    JOIN estudiantes e ON e.id = n.estudiante_id
    JOIN materias m ON m.id = n.materia_id
    ORDER BY e.nombre, m.nombre, n.periodo
    """)

    for fila in cursor.fetchall():
        tree_notas.insert("", tk.END, values=fila)

    conexion.close()


def generar_boletin():
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre FROM estudiantes")
    estudiantes = cursor.fetchall()

    if not estudiantes:
        messagebox.showwarning("Atención", "No hay estudiantes registrados")
        return

    if not os.path.exists(BOLETIN_DIR):
        os.makedirs(BOLETIN_DIR)

    for estudiante_id, nombre_estudiante in estudiantes:
        cursor.execute("""
        SELECT m.nombre, n.periodo, AVG(n.nota)
        FROM notas n
        JOIN materias m ON m.id = n.materia_id
        WHERE n.estudiante_id = ?
        GROUP BY m.nombre, n.periodo
        """, (estudiante_id,))

        datos = cursor.fetchall()
        html = f"""
        <html>
        <head><title>Boletín - {nombre_estudiante}</title></head>
        <body>
        <h1>Boletín de Calificaciones</h1>
        <h2>Estudiante: {nombre_estudiante}</h2>
        <table border='1' cellpadding='5' cellspacing='0'>
        <tr><th>Materia</th><th>Periodo</th><th>Definitiva</th></tr>
        """

        for materia, periodo, definitiva in datos:
            # CAMBIO: Redondear la definitiva a número entero
            definitiva_redondeada = round(definitiva)
            html += f"<tr><td>{materia}</td><td>{periodo}</td><td>{definitiva_redondeada}</td></tr>"

        html += "</table></body></html>"

        nombre_archivo = os.path.join(BOLETIN_DIR, f"boletin_{nombre_estudiante.replace(' ', '_')}.html")
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            f.write(html)

    conexion.close()
    messagebox.showinfo("Éxito", "Boletines generados en la carpeta 'boletines'")

#INTERFAZ GRAFICA

root = tk.Tk()
root.title("Gestor de Calificaciones")
root.geometry("900x600")
root.resizable(False, False)

# Pestañas
tabs = ttk.Notebook(root)
tabs.pack(fill="both", expand=True)

frame_estudiantes = ttk.Frame(tabs)
frame_materias = ttk.Frame(tabs)
frame_notas = ttk.Frame(tabs)
frame_boletin = ttk.Frame(tabs)

tabs.add(frame_estudiantes, text="Estudiantes")
tabs.add(frame_materias, text="Materias")
tabs.add(frame_notas, text="Notas")
tabs.add(frame_boletin, text="Boletines")

#Estudiantes
ttk.Label(frame_estudiantes, text="Nombre del estudiante:").pack(pady=10)
entry_nombre_estudiante = ttk.Entry(frame_estudiantes, width=40)
entry_nombre_estudiante.pack()
ttk.Button(frame_estudiantes, text="Registrar", command=registrar_estudiante).pack(pady=10)

#Materias
ttk.Label(frame_materias, text="Nombre de la materia:").pack(pady=10)
entry_nombre_materia = ttk.Entry(frame_materias, width=40)
entry_nombre_materia.pack()

ttk.Label(frame_materias, text="Cantidad de notas:").pack(pady=10)
entry_cantidad_notas = ttk.Entry(frame_materias, width=10)
entry_cantidad_notas.pack()

ttk.Button(frame_materias, text="Registrar", command=registrar_materia).pack(pady=10)

#Notas
ttk.Label(frame_notas, text="Selecciona estudiante:").pack(pady=5)
combo_estudiantes = ttk.Combobox(frame_notas, width=40)
combo_estudiantes.pack()

ttk.Label(frame_notas, text="Selecciona materia:").pack(pady=5)
combo_materias = ttk.Combobox(frame_notas, width=40)
combo_materias.pack()

ttk.Label(frame_notas, text="Periodo (1-4):").pack(pady=5)
entry_periodo = ttk.Entry(frame_notas, width=10)
entry_periodo.pack()

ttk.Label(frame_notas, text="Nota (0-5):").pack(pady=5)
entry_nota = ttk.Entry(frame_notas, width=10)
entry_nota.pack()

ttk.Button(frame_notas, text="Guardar Nota", command=guardar_nota).pack(pady=10)

columns = ("Estudiante", "Materia", "Periodo", "Nota")
tree_notas = ttk.Treeview(frame_notas, columns=columns, show="headings")
for col in columns:
    tree_notas.heading(col, text=col)
tree_notas.pack(fill="both", expand=True, pady=10)

#Boletines
ttk.Label(frame_boletin, text="Generar boletines de todos los estudiantes").pack(pady=20)
ttk.Button(frame_boletin, text="Generar Boletines", command=generar_boletin).pack()

#INICIO
inicializar_bd()

def cargar_datos_combobox():
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre FROM estudiantes")
    combo_estudiantes["values"] = [f"{id} - {nombre}" for id, nombre in cursor.fetchall()]

    cursor.execute("SELECT id, nombre FROM materias")
    combo_materias["values"] = [f"{id} - {nombre}" for id, nombre in cursor.fetchall()]
    conexion.close()

cargar_datos_combobox()
actualizar_tablas()

root.mainloop()
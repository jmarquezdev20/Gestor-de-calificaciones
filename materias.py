import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

def ventana_materias(parent_frame):
    """Vista de gestión de materias dentro del frame principal"""
    frame = tk.Frame(parent_frame, bg="#f8f9fa")
    frame.pack(fill='both', expand=True, padx=20, pady=20)

    #ENCABEZADO
    header = tk.Frame(frame, bg="#2c3e50", height=85)
    header.pack(fill='x')
    header.pack_propagate(False)

    tk.Label(header, text="📚", font=("Segoe UI Emoji", 40), bg="#2c3e50").pack(side='left', padx=20)
    tk.Label(header, text="GESTIÓN DE MATERIAS", font=("Segoe UI", 22, "bold"),
             bg="#2c3e50", fg="white").pack(anchor='w', padx=10, pady=(15, 0))
    tk.Label(header, text="Agregue, edite o elimine las materias del sistema",
             font=("Segoe UI", 10), bg="#2c3e50", fg="#ecf0f1").pack(anchor='w', padx=10)

    #FORMULARIO
    form_frame = tk.Frame(frame, bg="#ffffff")
    form_frame.pack(fill='x', padx=10, pady=25, ipady=10)

    # Nombre de materia
    tk.Label(form_frame, text="📖 Nombre de la Materia:", font=("Segoe UI", 12, "bold"),
             bg="#ffffff", fg="#2c3e50").grid(row=0, column=0, padx=20, pady=10, sticky='e')
    materia_entry = tk.Entry(form_frame, font=("Segoe UI", 12), width=40, relief='solid', bd=2)
    materia_entry.grid(row=0, column=1, padx=10, pady=10, sticky='w')

    # Cantidad de notas
    tk.Label(form_frame, text="🔢 Cantidad de Notas:", font=("Segoe UI", 12, "bold"),
             bg="#ffffff", fg="#2c3e50").grid(row=0, column=2, padx=20, pady=10, sticky='e')
    num_notas_spin = tk.Spinbox(form_frame, from_=1, to=10, font=("Segoe UI", 12),
                                width=8, relief='solid', bd=2, justify='center')
    num_notas_spin.delete(0, 'end')
    num_notas_spin.insert(0, '3')
    num_notas_spin.grid(row=0, column=3, padx=10, pady=10, sticky='w')

    #FUNCIONES
    def cargar_materias():
        for item in tree.get_children():
            tree.delete(item)
        conn = sqlite3.connect('calificaciones.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, nombre, num_notas FROM materias ORDER BY nombre')
        for row in cursor.fetchall():
            tree.insert('', 'end', values=(row[0], row[1], row[2]))
        conn.close()

    def agregar_materia():
        nombre = materia_entry.get().strip()
        num_notas = num_notas_spin.get()
        if not nombre:
            messagebox.showwarning("⚠️ Advertencia", "El nombre de la materia es obligatorio")
            return
        try:
            num_notas = int(num_notas)
            if num_notas < 1 or num_notas > 10:
                raise ValueError
        except ValueError:
            messagebox.showerror("❌ Error", "La cantidad de notas debe estar entre 1 y 10")
            return
        try:
            conn = sqlite3.connect('calificaciones.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO materias (nombre, num_notas) VALUES (?, ?)', (nombre, num_notas))
            conn.commit(); conn.close()
            messagebox.showinfo("✅ Éxito", f"Materia '{nombre}' registrada correctamente")
            materia_entry.delete(0, 'end')
            num_notas_spin.delete(0, 'end')
            num_notas_spin.insert(0, '3')
            cargar_materias()
        except sqlite3.IntegrityError:
            messagebox.showerror("❌ Error", f"Ya existe una materia con el nombre '{nombre}'")

    def eliminar_materia():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("⚠️ Advertencia", "Seleccione una materia para eliminar")
            return
        item = tree.item(selected[0])
        materia_id = item['values'][0]
        materia_nombre = item['values'][1]
        if messagebox.askyesno("🗑️ Confirmar Eliminación",
                               f"¿Eliminar la materia '{materia_nombre}' y sus calificaciones?"):
            conn = sqlite3.connect('calificaciones.db')
            cursor = conn.cursor()
            cursor.execute('DELETE FROM calificaciones WHERE materia_id=?', (materia_id,))
            cursor.execute('DELETE FROM materias WHERE id=?', (materia_id,))
            conn.commit(); conn.close()
            cargar_materias()
            messagebox.showinfo("✅ Éxito", f"Materia '{materia_nombre}' eliminada correctamente")

    def editar_materia():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("⚠️ Advertencia", "Seleccione una materia para editar")
            return
        item = tree.item(selected[0])
        materia_id = item['values'][0]
        conn = sqlite3.connect('calificaciones.db')
        cursor = conn.cursor()
        cursor.execute('SELECT nombre, num_notas FROM materias WHERE id=?', (materia_id,))
        datos = cursor.fetchone()
        conn.close()

        materia_entry.delete(0, 'end')
        materia_entry.insert(0, datos[0])
        num_notas_spin.delete(0, 'end')
        num_notas_spin.insert(0, str(datos[1]))

        def guardar_edicion():
            nombre = materia_entry.get().strip()
            num_notas = num_notas_spin.get()
            if not nombre:
                messagebox.showwarning("⚠️ Advertencia", "El nombre es obligatorio")
                return
            try:
                conn = sqlite3.connect('calificaciones.db')
                cursor = conn.cursor()
                cursor.execute('UPDATE materias SET nombre=?, num_notas=? WHERE id=?',
                               (nombre, int(num_notas), materia_id))
                conn.commit(); conn.close()
                messagebox.showinfo("✅ Éxito", "Materia actualizada correctamente")
                btn_add.config(text="➕ Agregar Materia", command=agregar_materia)
                materia_entry.delete(0, 'end')
                num_notas_spin.delete(0, 'end')
                num_notas_spin.insert(0, '3')
                cargar_materias()
            except Exception as e:
                messagebox.showerror("❌ Error", f"Error al actualizar: {e}")

        btn_add.config(text="💾 Guardar Cambios", command=guardar_edicion)

    #BOTONES 
    btn_frame = tk.Frame(form_frame, bg="#ffffff")
    btn_frame.grid(row=1, column=0, columnspan=4, pady=10)
    btn_add = tk.Button(btn_frame, text="➕ Agregar Materia", command=agregar_materia,
                        bg="#27ae60", fg="white", font=("Segoe UI", 11, "bold"),
                        relief='flat', padx=20, pady=10, cursor="hand2")
    btn_add.pack(side='left', padx=10)
    tk.Button(btn_frame, text="✏️ Editar", command=editar_materia,
              bg="#f39c12", fg="white", font=("Segoe UI", 11, "bold"),
              relief='flat', padx=20, pady=10, cursor="hand2").pack(side='left', padx=10)
    tk.Button(btn_frame, text="🗑️ Eliminar", command=eliminar_materia,
              bg="#e74c3c", fg="white", font=("Segoe UI", 11, "bold"),
              relief='flat', padx=20, pady=10, cursor="hand2").pack(side='left', padx=10)

    #TABLA
    table_frame = tk.Frame(frame, bg="#f8f9fa")
    table_frame.pack(fill='both', expand=True, padx=10, pady=10)
    tk.Label(table_frame, text="📋 Materias Registradas", font=("Segoe UI", 15, "bold"),
             bg="#f8f9fa", fg="#2c3e50").pack(pady=10)

    style = ttk.Style()
    style.theme_use('clam')
    style.configure("Treeview", background="#ffffff", foreground="#2c3e50",
                    fieldbackground="#ffffff", rowheight=35, font=("Segoe UI", 12))
    style.configure("Treeview.Heading", background="#34495e", foreground="white",
                    font=("Segoe UI", 12, "bold"))
    style.map("Treeview", background=[("selected", "#3498db")])

    columns = ('ID', 'Materia', 'Cant. Notas')
    tree = ttk.Treeview(table_frame, columns=columns, show='headings')

    # CONFIGURACIÓN DE COLUMNAS
    for col in columns:
        tree.heading(col, text=col)
        if col == 'ID':
            tree.column(col, width=100, anchor='center')
        elif col == 'Cant. Notas':
            tree.column(col, width=180, anchor='center')
        else:
            tree.column(col, width=400, anchor='center')  # CAMBIADO A CENTER

    tree.pack(side='left', fill='both', expand=True)
    scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side='right', fill='y')

    tree.bind('<Double-1>', lambda e: editar_materia())

    cargar_materias()
    materia_entry.focus()
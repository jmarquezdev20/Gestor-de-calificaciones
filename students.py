import tkinter as tk
from tkinter import ttk, messagebox
from database import conectar, crear_tablas
import sqlite3

# Crear tablas al iniciar la app
crear_tablas()

def ventana_estudiantes(parent_frame):
    """Vista de gestión de estudiantes dentro del frame principal"""
    frame = tk.Frame(parent_frame, bg="#f8f9fa")  # Fondo gris claro suave
    frame.pack(fill='both', expand=True, padx=20, pady=20)

    # Variable para modo edición
    estudiante_editando = {'id': None}

    # HEADER 
    header = tk.Frame(frame, bg="#2c3e50", height=85)  # Azul grisáceo elegante
    header.pack(fill='x')
    header.pack_propagate(False)
    tk.Label(header, text="👨‍🎓", font=("Segoe UI Emoji", 38), bg="#2c3e50").pack(side='left', padx=20)
    tk.Label(header, text="GESTIÓN DE ESTUDIANTES", font=("Segoe UI", 20, "bold"),
             bg="#2c3e50", fg="#ffffff").pack(anchor='w', padx=10, pady=(15, 0))
    tk.Label(header, text="Registre y administre la información de los estudiantes",
             font=("Segoe UI", 10), bg="#2c3e50", fg="#ecf0f1").pack(anchor='w', padx=10)

    #  FORMULARIO 
    form_frame = tk.Frame(frame, bg="#ffffff")  # Blanco limpio
    form_frame.pack(fill='x', padx=10, pady=20, ipady=10)

    # Campos
    tk.Label(form_frame, text="📝 Nombre:", font=("Segoe UI", 11, "bold"), bg="#ffffff", fg="#2c3e50").grid(row=0, column=0, padx=10, pady=8, sticky='e')
    nombre_entry = tk.Entry(form_frame, font=("Segoe UI", 11), width=25, relief='solid', bd=2)
    nombre_entry.grid(row=0, column=1, padx=10, pady=8)

    tk.Label(form_frame, text="👤 Apellido:", font=("Segoe UI", 11, "bold"), bg="#ffffff", fg="#2c3e50").grid(row=0, column=2, padx=10, pady=8, sticky='e')
    apellido_entry = tk.Entry(form_frame, font=("Segoe UI", 11), width=25, relief='solid', bd=2)
    apellido_entry.grid(row=0, column=3, padx=10, pady=8)

    tk.Label(form_frame, text="🆔 Identificación:", font=("Segoe UI", 11, "bold"), bg="#ffffff", fg="#2c3e50").grid(row=1, column=0, padx=10, pady=8, sticky='e')
    id_entry = tk.Entry(form_frame, font=("Segoe UI", 11), width=25, relief='solid', bd=2)
    id_entry.grid(row=1, column=1, padx=10, pady=8)

    tk.Label(form_frame, text="🏫 Grado:", font=("Segoe UI", 11, "bold"), bg="#ffffff", fg="#2c3e50").grid(row=1, column=2, padx=10, pady=8, sticky='e')
    grado_entry = ttk.Combobox(form_frame, font=("Segoe UI", 11), width=23,
                               values=["Preescolar", "Primero", "Segundo", "Tercero", "Cuarto",
                                       "Quinto", "Sexto", "Séptimo", "Octavo", "Noveno",
                                       "Décimo", "Undécimo"])
    grado_entry.grid(row=1, column=3, padx=10, pady=8)
    grado_entry.set("Seleccionar grado")

    # FUNCIONES
    def limpiar_campos():
        nombre_entry.delete(0, 'end')
        apellido_entry.delete(0, 'end')
        id_entry.delete(0, 'end')
        grado_entry.set("Seleccionar grado")
        estudiante_editando['id'] = None

    def cargar_estudiantes():
        for i in tree.get_children():
            tree.delete(i)
        conn = conectar()
        cur = conn.cursor()
        cur.execute("SELECT id, nombre, apellido, identificacion, grado FROM estudiantes ORDER BY apellido, nombre")
        for row in cur.fetchall():
            row = list(row)
            if not row[4]:
                row[4] = "No asignado"
            tree.insert('', 'end', values=row)
        conn.close()

    def agregar_estudiante():
        n, a, i, g = nombre_entry.get().strip(), apellido_entry.get().strip(), id_entry.get().strip(), grado_entry.get().strip()
        if not all([n, a, i]) or g == "Seleccionar grado":
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")
            return
        try:
            conn = conectar()
            cur = conn.cursor()
            cur.execute("INSERT INTO estudiantes (nombre, apellido, identificacion, grado) VALUES (?, ?, ?, ?)",
                        (n, a, i, g))
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", f"{n} {a} ({g}) registrado correctamente")
            limpiar_campos()
            cargar_estudiantes()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Ya existe un estudiante con esa identificación")

    def editar_estudiante():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Advertencia", "Seleccione un estudiante para editar")
            return
        
        item = tree.item(sel[0])
        valores = item['values']
        
        # Guardar ID del estudiante en edición
        estudiante_editando['id'] = valores[0]
        
        # Cargar datos en los campos
        nombre_entry.delete(0, 'end')
        nombre_entry.insert(0, valores[1])
        
        apellido_entry.delete(0, 'end')
        apellido_entry.insert(0, valores[2])
        
        id_entry.delete(0, 'end')
        id_entry.insert(0, valores[3])
        
        grado_entry.set(valores[4] if valores[4] != "No asignado" else "Seleccionar grado")
        
        # Cambiar apariencia del botón
        btn_agregar.config(text="💾 Guardar Cambios", bg="#f39c12")
        btn_cancelar.pack(side='left', padx=6)

    def guardar_edicion():
        if estudiante_editando['id'] is None:
            agregar_estudiante()
            return
        
        n, a, i, g = nombre_entry.get().strip(), apellido_entry.get().strip(), id_entry.get().strip(), grado_entry.get().strip()
        if not all([n, a, i]) or g == "Seleccionar grado":
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")
            return
        
        try:
            conn = conectar()
            cur = conn.cursor()
            cur.execute("""
                UPDATE estudiantes 
                SET nombre=?, apellido=?, identificacion=?, grado=? 
                WHERE id=?
            """, (n, a, i, g, estudiante_editando['id']))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Éxito", f"Estudiante {n} {a} actualizado correctamente")
            cancelar_edicion()
            cargar_estudiantes()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Ya existe un estudiante con esa identificación")

    def cancelar_edicion():
        limpiar_campos()
        btn_agregar.config(text="➕ Agregar", bg="#27ae60")
        btn_cancelar.pack_forget()

    def eliminar_estudiante():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Advertencia", "Seleccione un estudiante para eliminar")
            return
        item = tree.item(sel[0])
        est_id, nombre = item['values'][0], f"{item['values'][1]} {item['values'][2]}"
        if messagebox.askyesno("Confirmar", f"¿Eliminar a {nombre}?"):
            conn = conectar()
            cur = conn.cursor()
            cur.execute("DELETE FROM estudiantes WHERE id=?", (est_id,))
            conn.commit()
            conn.close()
            cargar_estudiantes()
            messagebox.showinfo("Éxito", f"Estudiante {nombre} eliminado correctamente")

    def buscar_estudiante(e=None):
        term = buscar_entry.get().lower().strip()
        for i in tree.get_children():
            tree.delete(i)
        conn = conectar()
        cur = conn.cursor()
        if term:
            cur.execute("""
                SELECT id, nombre, apellido, identificacion, grado
                FROM estudiantes
                WHERE LOWER(nombre) LIKE ? OR LOWER(apellido) LIKE ? OR identificacion LIKE ? OR LOWER(grado) LIKE ?
                ORDER BY apellido, nombre
            """, (f'%{term}%', f'%{term}%', f'%{term}%', f'%{term}%'))
        else:
            cur.execute("SELECT id, nombre, apellido, identificacion, grado FROM estudiantes ORDER BY apellido, nombre")
        for row in cur.fetchall():
            row = list(row)
            if not row[4]:
                row[4] = "No asignado"
            tree.insert('', 'end', values=row)
        conn.close()

    # BOTONES
    btn_frame = tk.Frame(form_frame, bg="#ffffff")
    btn_frame.grid(row=2, column=0, columnspan=4, pady=10)
    
    btn_agregar = tk.Button(btn_frame, text="➕ Agregar", command=guardar_edicion, bg="#27ae60", fg="white",
              font=("Segoe UI", 10, "bold"), relief='flat', padx=18, pady=10, cursor="hand2")
    btn_agregar.pack(side='left', padx=6)
    
    tk.Button(btn_frame, text="✏️ Editar", command=editar_estudiante, bg="#f39c12", fg="white",
              font=("Segoe UI", 10, "bold"), relief='flat', padx=18, pady=10, cursor="hand2").pack(side='left', padx=6)
    
    btn_cancelar = tk.Button(btn_frame, text="❌ Cancelar", command=cancelar_edicion, bg="#95a5a6", fg="white",
              font=("Segoe UI", 10, "bold"), relief='flat', padx=18, pady=10, cursor="hand2")
    
    tk.Button(btn_frame, text="🗑️ Eliminar", command=eliminar_estudiante, bg="#e74c3c", fg="white",
              font=("Segoe UI", 10, "bold"), relief='flat', padx=18, pady=10, cursor="hand2").pack(side='left', padx=6)

    # BUSCADOR
    search_frame = tk.Frame(frame, bg="#f8f9fa")
    search_frame.pack(fill='x', padx=10, pady=5)
    tk.Label(search_frame, text="🔍 Buscar:", font=("Segoe UI", 10, "bold"), bg="#f8f9fa", fg="#2c3e50").pack(side='left', padx=10)
    buscar_entry = tk.Entry(search_frame, font=("Segoe UI", 10), width=40, relief='solid', bd=2)
    buscar_entry.pack(side='left', padx=10)
    buscar_entry.bind("<KeyRelease>", buscar_estudiante)

    # TABLA 
    table_frame = tk.Frame(frame, bg="#f8f9fa")
    table_frame.pack(fill='both', expand=True, padx=10, pady=10)

    style = ttk.Style()
    style.theme_use('clam')
    style.configure("Treeview", background="#ffffff", foreground="#2c3e50", rowheight=30, fieldbackground="#ffffff")
    style.configure("Treeview.Heading", background="#34495e", foreground="white", font=("Segoe UI", 10, "bold"))
    style.map('Treeview', background=[('selected', '#3498db')])

    columns = ('ID', 'Nombre', 'Apellido', 'Identificación', 'Grado')
    tree = ttk.Treeview(table_frame, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor='center', width=200 if col != "ID" else 60)

    tree.pack(side='left', fill='both', expand=True)
    scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side='right', fill='y')

    # Doble clic para editar
    tree.bind('<Double-1>', lambda e: editar_estudiante())

    cargar_estudiantes()
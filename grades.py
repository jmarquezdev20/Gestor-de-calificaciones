import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

def ventana_notas(parent):
    """Vista de gestión de calificaciones con tabla matriz mostrando todas las notas"""
    for widget in parent.winfo_children():
        widget.destroy()

    parent.configure(bg="#f0f3f7")

    #HEADER
    header = tk.Frame(parent, bg="#1e3a5f", height=90)
    header.pack(fill='x')
    header.pack_propagate(False)
    
    tk.Frame(header, bg="#4a90e2", height=3).pack(fill='x')
    
    header_content = tk.Frame(header, bg="#1e3a5f")
    header_content.pack(fill='both', expand=True)
    
    tk.Label(header_content, text="📊", font=("Segoe UI Emoji", 42), bg="#1e3a5f").pack(side='left', padx=25, pady=5)
    
    title_frame = tk.Frame(header_content, bg="#1e3a5f")
    title_frame.pack(side='left', pady=12)
    tk.Label(title_frame, text="Gestión de Calificaciones", font=("Segoe UI", 22, "bold"), 
             bg="#1e3a5f", fg="white").pack(anchor='w')
    tk.Label(title_frame, text="Sistema de Evaluación Académica", font=("Segoe UI", 10), 
             bg="#1e3a5f", fg="#a8c5e8").pack(anchor='w')

    #TOOLBAR 
    toolbar = tk.Frame(parent, bg="white", height=75)
    toolbar.pack(fill='x', padx=30, pady=18)
    toolbar.pack_propagate(False)
    
    #Sombra sutil
    tk.Frame(parent, bg="#d1d9e6", height=2).place(x=30, y=183, relwidth=0.92)

    toolbar_content = tk.Frame(toolbar, bg="white")
    toolbar_content.pack(fill='both', expand=True, padx=20, pady=12)

    left_section = tk.Frame(toolbar_content, bg="white")
    left_section.pack(side='left')

    tk.Label(left_section, text="📅", font=("Segoe UI Emoji", 22), bg="white").pack(side='left', padx=(0, 12))
    
    periodo_container = tk.Frame(left_section, bg="white")
    periodo_container.pack(side='left')
    tk.Label(periodo_container, text="Periodo Académico", font=("Segoe UI", 9, "bold"),
             bg="white", fg="#4a5568").pack(anchor='w')
    
    combo_periodo = ttk.Combobox(periodo_container, 
                                values=['1 - Primer Periodo', '2 - Segundo Periodo', 
                                        '3 - Tercer Periodo', '4 - Cuarto Periodo'], 
                                width=22, state='readonly', font=("Segoe UI", 10))
    combo_periodo.current(0)
    combo_periodo.pack(pady=(3, 0))

    right_section = tk.Frame(toolbar_content, bg="white")
    right_section.pack(side='right')

    btn_cargar = tk.Button(right_section, text="🔄  Actualizar", bg="#4a90e2", fg="white",
                          font=("Segoe UI", 10, "bold"), relief='flat', padx=22, pady=11, 
                          cursor="hand2", bd=0, activebackground="#357abd", activeforeground="white")
    btn_cargar.pack(side='left', padx=5)

    # Banner informativo 
    info_banner = tk.Frame(parent, bg="#e8f4fd", height=42)
    info_banner.pack(fill='x', padx=30, pady=(0, 15))
    info_banner.pack_propagate(False)
    
    tk.Frame(info_banner, bg="#4a90e2", width=4).pack(side='left', fill='y')
    tk.Label(info_banner, text="💡", font=("Segoe UI Emoji", 16), bg="#e8f4fd").pack(side='left', padx=12)
    tk.Label(info_banner, text="Haz doble clic en cualquier celda para ingresar o modificar las calificaciones", 
             font=("Segoe UI", 10), bg="#e8f4fd", fg="#2d5f8e").pack(side='left', pady=10)

    #TABLA PRINCIPAL
    tabla_outer = tk.Frame(parent, bg="white", bd=0)
    tabla_outer.pack(fill='both', expand=True, padx=30, pady=(0, 25))
    
    # Sombra de la tabla
    tk.Frame(tabla_outer, bg="#cbd5e0", height=3).pack(fill='x', side='bottom')

    tabla_frame = tk.Frame(tabla_outer, bg="white")
    tabla_frame.pack(fill='both', expand=True, padx=3, pady=3)

    canvas = tk.Canvas(tabla_frame, bg="white", highlightthickness=0)
    scrollbar_y = ttk.Scrollbar(tabla_frame, orient='vertical', command=canvas.yview)
    scrollbar_x = ttk.Scrollbar(tabla_frame, orient='horizontal', command=canvas.xview)
    
    tabla_container = tk.Frame(canvas, bg="white")
    
    canvas.create_window((0, 0), window=tabla_container, anchor='nw')
    canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

    canvas.pack(side='left', fill='both', expand=True)
    scrollbar_y.pack(side='right', fill='y')
    scrollbar_x.pack(side='bottom', fill='x')

    celdas_info = {}

    def abrir_ventana_notas(est_id, est_nombre, mat_id, mat_nombre, num_notas, periodo):
        """Abre ventana emergente para ingresar las notas individuales"""
        ventana = tk.Toplevel()
        ventana.title(f"Notas - {est_nombre} - {mat_nombre}")
        ventana.geometry("500x600")
        ventana.configure(bg="#f8f9fa")
        ventana.resizable(False, False)
        ventana.grab_set()

        header_v = tk.Frame(ventana, bg="#3498db", height=80)
        header_v.pack(fill='x')
        header_v.pack_propagate(False)
        
        tk.Label(header_v, text=f"👨‍🎓 {est_nombre}", font=("Segoe UI", 14, "bold"),
                bg="#3498db", fg="white").pack(pady=5)
        tk.Label(header_v, text=f"📚 {mat_nombre} - Periodo {periodo}", font=("Segoe UI", 11),
                bg="#3498db", fg="white").pack()

        conn = sqlite3.connect('calificaciones.db')
        cursor = conn.cursor()
        cursor.execute("""
            SELECT nota_num, valor FROM calificaciones 
            WHERE estudiante_id = ? AND materia_id = ? AND periodo = ?
            ORDER BY nota_num
        """, (est_id, mat_id, periodo))
        notas_existentes = dict(cursor.fetchall())
        conn.close()

        notas_frame = tk.Frame(ventana, bg="#ffffff", bd=1, relief='solid')
        notas_frame.pack(pady=20, padx=30, fill='both', expand=True)

        tk.Label(notas_frame, text="📝 Ingrese las Calificaciones", 
                font=("Segoe UI", 12, "bold"), bg="#ffffff", fg="#2c3e50").pack(pady=15)

        entries = []
        for i in range(num_notas):
            fila = tk.Frame(notas_frame, bg="#ffffff")
            fila.pack(pady=8, padx=20, fill='x')
            
            tk.Label(fila, text=f"Nota {i+1}:", font=("Segoe UI", 11, "bold"),
                    bg="#ffffff", fg="#2c3e50", width=10, anchor='e').pack(side='left', padx=10)
            
            entry = tk.Entry(fila, font=("Segoe UI", 12), width=12, justify='center', bd=2)
            entry.pack(side='left', padx=5)
            
            if (i+1) in notas_existentes:
                entry.insert(0, str(notas_existentes[i+1]))
            
            entries.append(entry)

        definitiva_frame = tk.Frame(notas_frame, bg="#ecf0f1", bd=2, relief='solid')
        definitiva_frame.pack(pady=20, padx=20, fill='x')
        
        definitiva_label = tk.Label(definitiva_frame, text="Definitiva: -- ", 
                                    font=("Segoe UI", 14, "bold"), bg="#ecf0f1", fg="#2c3e50")
        definitiva_label.pack(pady=15)

        def calcular_definitiva_temporal():
            valores = []
            for entry in entries:
                val = entry.get().strip()
                if val:
                    try:
                        nota = float(val)
                        if 0 <= nota <= 10:
                            valores.append(nota)
                    except:
                        pass
            
            if valores:
                promedio = sum(valores) / len(valores)
                color = "#27ae60" if promedio >= 6 else "#e74c3c"
                estado = "✅ APROBADO" if promedio >= 6 else "❌ REPROBADO"
                definitiva_label.config(text=f"Definitiva: {promedio:.2f} | {estado}", fg=color)
            else:
                definitiva_label.config(text="Definitiva: --", fg="#2c3e50")

        for entry in entries:
            entry.bind('<KeyRelease>', lambda e: calcular_definitiva_temporal())

        calcular_definitiva_temporal()

        botones_frame = tk.Frame(ventana, bg="#f8f9fa")
        botones_frame.pack(pady=15)

        def guardar_notas_individuales():
            notas = []
            for i, entry in enumerate(entries):
                val = entry.get().strip()
                if val:
                    try:
                        nota = float(val)
                        if 0 <= nota <= 10:
                            notas.append((i+1, nota))
                        else:
                            messagebox.showerror("Error", f"La nota {i+1} debe estar entre 0.0 y 10.0")
                            return
                    except:
                        messagebox.showerror("Error", f"La nota {i+1} no es válida")
                        return

            if not notas:
                messagebox.showwarning("Advertencia", "Ingrese al menos una nota")
                return

            conn = sqlite3.connect('calificaciones.db')
            cursor = conn.cursor()
            
            cursor.execute("""
                DELETE FROM calificaciones 
                WHERE estudiante_id=? AND materia_id=? AND periodo=?
            """, (est_id, mat_id, periodo))
            
            for nota_num, valor in notas:
                cursor.execute("""
                    INSERT INTO calificaciones (estudiante_id, materia_id, periodo, nota_num, valor)
                    VALUES (?, ?, ?, ?, ?)
                """, (est_id, mat_id, periodo, nota_num, valor))
            
            conn.commit()
            conn.close()

            promedio = sum(n[1] for n in notas) / len(notas)
            messagebox.showinfo("Éxito", f"✅ Notas guardadas\nDefinitiva: {promedio:.2f}")
            
            ventana.destroy()
            crear_tabla_matriz()

        tk.Button(botones_frame, text="💾 Guardar Notas", bg="#27ae60", fg="white",
                 font=("Segoe UI", 11, "bold"), padx=25, pady=10, relief='flat',
                 command=guardar_notas_individuales).pack(side='left', padx=5)

        tk.Button(botones_frame, text="❌ Cancelar", bg="#95a5a6", fg="white",
                 font=("Segoe UI", 11, "bold"), padx=25, pady=10, relief='flat',
                 command=ventana.destroy).pack(side='left', padx=5)

    def crear_tabla_matriz():
        """Crea tabla profesional con diseño premium"""
        nonlocal celdas_info
        celdas_info = {}
        
        for widget in tabla_container.winfo_children():
            widget.destroy()

        conn = sqlite3.connect('calificaciones.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, nombre, apellido FROM estudiantes ORDER BY apellido, nombre")
        estudiantes = cursor.fetchall()
        
        cursor.execute("SELECT id, nombre, num_notas FROM materias ORDER BY nombre")
        materias = cursor.fetchall()
        
        if not estudiantes or not materias:
            empty_frame = tk.Frame(tabla_container, bg="white")
            empty_frame.grid(row=0, column=0, padx=100, pady=80)
            
            tk.Label(empty_frame, text="📋", font=("Segoe UI Emoji", 60), bg="white").pack(pady=15)
            tk.Label(empty_frame, text="No hay datos disponibles",
                    font=("Segoe UI", 17, "bold"), bg="white", fg="#2d3748").pack()
            tk.Label(empty_frame, text="Registra estudiantes y materias para comenzar",
                    font=("Segoe UI", 11), bg="white", fg="#718096").pack(pady=8)
            conn.close()
            return

        periodo = int(combo_periodo.get().split(' - ')[0])

        cursor.execute("""
            SELECT estudiante_id, materia_id, nota_num, valor
            FROM calificaciones
            WHERE periodo = ?
            ORDER BY estudiante_id, materia_id, nota_num
        """, (periodo,))
        
        notas_por_celda = {}
        for row in cursor.fetchall():
            est_id, mat_id, nota_num, valor = row
            key = (est_id, mat_id)
            if key not in notas_por_celda:
                notas_por_celda[key] = []
            notas_por_celda[key].append((nota_num, valor))
        
        conn.close()

        # HEADER ESQUINA
        esquina = tk.Frame(tabla_container, bg="#1e3a5f", bd=0)
        esquina.grid(row=0, column=0, sticky='nsew', padx=0, pady=0)
        tk.Label(esquina, text="ESTUDIANTES", font=("Segoe UI", 10, "bold"),
                bg="#1e3a5f", fg="white", padx=25, pady=20).pack()

        # HEADERS DE MATERIAS - Gradiente azul
        for col_idx, materia in enumerate(materias, start=1):
            header_frame = tk.Frame(tabla_container, bg="#4a90e2", bd=0)
            header_frame.grid(row=0, column=col_idx, sticky='nsew', padx=0, pady=0)
            
            # Borde inferior del header
            tk.Frame(header_frame, bg="#357abd", height=3).pack(side='bottom', fill='x')
            
            tk.Label(header_frame, text=materia[1].upper(), font=("Segoe UI", 9, "bold"),
                    bg="#4a90e2", fg="white", padx=15, pady=20, wraplength=170).pack()

        # FILAS DE ESTUDIANTES
        for row_idx, estudiante in enumerate(estudiantes, start=1):
            est_id, nombre, apellido = estudiante
            nombre_completo = f"{apellido}, {nombre}"
            
            # Alternar colores sutiles
            row_bg = "#f7fafc" if row_idx % 2 == 0 else "#ffffff"
            
            # Celda del estudiante
            est_frame = tk.Frame(tabla_container, bg="#e8f1f8", bd=0)
            est_frame.grid(row=row_idx, column=0, sticky='nsew', padx=0, pady=0)
            
            # Borde izquierdo de acento
            tk.Frame(est_frame, bg="#4a90e2", width=4).pack(side='left', fill='y')
            
            tk.Label(est_frame, text=nombre_completo, font=("Segoe UI", 10, "bold"),
                    bg="#e8f1f8", fg="#1e3a5f", padx=20, pady=22, anchor='w').pack(side='left', fill='both', expand=True)

            for col_idx, materia in enumerate(materias, start=1):
                mat_id, mat_nombre, num_notas = materia
                key = (est_id, mat_id)
                
                celda_frame = tk.Frame(tabla_container, bg=row_bg, bd=0, cursor="hand2", highlightthickness=1, highlightbackground="#e2e8f0")
                celda_frame.grid(row=row_idx, column=col_idx, sticky='nsew', padx=0, pady=0)

                contenido_frame = tk.Frame(celda_frame, bg=row_bg)
                contenido_frame.pack(fill='both', expand=True, padx=12, pady=12)

                if key in notas_por_celda:
                    notas = notas_por_celda[key]
                    definitiva = sum(n[1] for n in notas) / len(notas)
                    
                    # Colores premium según estado (aprobación desde 6.0)
                    if definitiva >= 9.0:
                        bg_color = "#d4edda"  # Verde excelente
                        fg_color = "#155724"
                        icon = "🌟"
                    elif definitiva >= 6.0:
                        bg_color = "#d1ecf1"  # Azul aprobado
                        fg_color = "#0c5460"
                        icon = "✓"
                    else:
                        bg_color = "#f8d7da"  # Rojo reprobado
                        fg_color = "#721c24"
                        icon = "✗"
                    
                    celda_frame.config(bg=bg_color, highlightbackground="#c3e6cb" if definitiva >= 6.0 else "#f5c6cb")
                    contenido_frame.config(bg=bg_color)
                    
                    # Notas individuales en formato compacto y elegante
                    notas_text = "  •  ".join([f"{valor:.1f}" for _, valor in sorted(notas)])
                    tk.Label(contenido_frame, text=notas_text, 
                            font=("Segoe UI", 9),
                            bg=bg_color, fg="#4a5568").pack()
                    
                    # Línea separadora decorativa
                    sep_frame = tk.Frame(contenido_frame, bg=bg_color, height=8)
                    sep_frame.pack(fill='x')
                    tk.Frame(sep_frame, bg="#95a5a6", height=2).pack(expand=True, fill='x', pady=3)
                    
                    # Definitiva con ícono y estilo destacado
                    def_container = tk.Frame(contenido_frame, bg=bg_color)
                    def_container.pack(pady=(3, 0))
                    
                    tk.Label(def_container, text=icon, font=("Segoe UI", 13),
                            bg=bg_color, fg=fg_color).pack(side='left', padx=(0, 5))
                    tk.Label(def_container, text=f"{definitiva:.2f}", 
                            font=("Segoe UI", 15, "bold"),
                            bg=bg_color, fg=fg_color).pack(side='left')
                else:
                    # Sin notas - diseño minimalista
                    tk.Label(contenido_frame, text="─", 
                            font=("Segoe UI", 18), bg=row_bg, fg="#cbd5e0").pack(pady=5)
                    tk.Label(contenido_frame, text="Sin calificaciones", 
                            font=("Segoe UI", 8, "italic"),
                            bg=row_bg, fg="#a0aec0").pack()

                # Efecto hover premium
                def on_enter(e, frame=celda_frame, orig_bg=celda_frame['bg']):
                    frame.config(highlightbackground="#4a90e2", highlightthickness=2)
                
                def on_leave(e, frame=celda_frame):
                    frame.config(highlightthickness=1)

                celda_frame.bind('<Enter>', on_enter)
                celda_frame.bind('<Leave>', on_leave)

                # Handler de doble clic
                def crear_handler(e_id, e_nom, m_id, m_nom, n_notas, per):
                    return lambda e: abrir_ventana_notas(e_id, f"{apellido}, {nombre}", m_id, m_nom, n_notas, per)

                handler = crear_handler(est_id, nombre_completo, mat_id, mat_nombre, num_notas, periodo)
                
                for widget in [celda_frame, contenido_frame] + list(contenido_frame.winfo_children()):
                    widget.bind('<Double-Button-1>', handler)

                celdas_info[key] = celda_frame

        # Configurar columnas con ancho mínimo
        for i in range(len(materias) + 1):
            tabla_container.grid_columnconfigure(i, weight=1, minsize=190)

        tabla_container.update_idletasks()
        canvas.config(scrollregion=canvas.bbox('all'))

    btn_cargar.config(command=crear_tabla_matriz)
    combo_periodo.bind('<<ComboboxSelected>>', lambda e: crear_tabla_matriz())

    crear_tabla_matriz()
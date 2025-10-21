from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import sqlite3, os
from datetime import datetime

def ventana_reportes(parent):
    frame = tk.Frame(parent, bg="#f8f9fa")
    frame.pack(fill='both', expand=True)

    #HEADER
    header = tk.Frame(frame, bg="#2c3e50", height=70)
    header.pack(fill='x')
    header.pack_propagate(False)
    tk.Label(header, text="📄 Reportes y Boletines",
             bg="#2c3e50", fg="white",
             font=("Segoe UI", 18, "bold")).pack(pady=15)

    #SELECCIÓN 
    select_frame = tk.Frame(frame, bg="#ffffff")
    select_frame.pack(fill='x', padx=20, pady=20)

    tk.Label(select_frame, text="👨‍🎓 Estudiante:",
             bg="#ffffff", fg="#2c3e50",
             font=("Segoe UI", 12, "bold")).pack(side='left', padx=10)

    student_combo = ttk.Combobox(select_frame, width=45, state='readonly', font=("Segoe UI", 11))
    student_combo.pack(side='left', padx=10)

    btn_ver = tk.Button(select_frame, text="📊 Ver Boletín",
                        bg="#f39c12", fg="white", relief='flat',
                        font=("Segoe UI", 11, "bold"), cursor="hand2", padx=20, pady=5)
    btn_ver.pack(side='left', padx=5)

    btn_pdf = tk.Button(select_frame, text="💾 Descargar PDF",
                        bg="#27ae60", fg="white", relief='flat',
                        font=("Segoe UI", 11, "bold"), cursor="hand2", padx=20, pady=5)
    btn_pdf.pack(side='left', padx=5)

    btn_todos = tk.Button(select_frame, text="📘 PDF Todos los Estudiantes",
                          bg="#3498db", fg="white", relief='flat',
                          font=("Segoe UI", 11, "bold"), cursor="hand2", padx=20, pady=5)
    btn_todos.pack(side='left', padx=5)

    #PREVIEW 
    preview_frame = tk.Frame(frame, bg="#f8f9fa")
    preview_frame.pack(fill='both', expand=True, padx=20, pady=10)

    tk.Label(preview_frame, text="📋 Vista previa del boletín",
             bg="#f8f9fa", fg="#2c3e50", font=("Segoe UI", 13, "bold")).pack(pady=10)

    preview_text = scrolledtext.ScrolledText(preview_frame,
                                             font=("Consolas", 11),
                                             bg="#ffffff", fg="#2c3e50",
                                             wrap='word', padx=20, pady=20)
    preview_text.pack(fill='both', expand=True)

    #FUNCIONES
    def cargar_estudiantes():
        conn = sqlite3.connect('calificaciones.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, nombre, apellido FROM estudiantes ORDER BY apellido, nombre')
        estudiantes = cursor.fetchall()
        conn.close()
        student_combo['values'] = [f"{e[0]} - {e[1]} {e[2]}" for e in estudiantes]
        if estudiantes:
            student_combo.current(0)

    def obtener_calificaciones(student_id):
        conn = sqlite3.connect('calificaciones.db')
        cursor = conn.cursor()
        cursor.execute("SELECT nombre, apellido, identificacion, grado FROM estudiantes WHERE id = ?", (student_id,))
        estudiante = cursor.fetchone()
        if not estudiante:
            conn.close()
            return None, [], None
        cursor.execute("""
            SELECT m.nombre, c.periodo, c.valor
            FROM calificaciones c
            JOIN materias m ON m.id = c.materia_id
            WHERE c.estudiante_id = ?
            ORDER BY m.nombre, c.periodo
        """, (student_id,))
        calificaciones = cursor.fetchall()
        
        # Detectar el período académico más reciente
        periodo_actual = None
        if calificaciones:
            periodo_actual = max([c[1] for c in calificaciones])
        
        conn.close()
        return estudiante, calificaciones, periodo_actual

    def calcular_desempeno(promedio):
        """Calcula el desempeño según la escala"""
        if promedio >= 9.5:
            return "SUPERIOR"
        elif promedio >= 8.0:
            return "ALTO"
        elif promedio >= 6.0:
            return "BASICO"
        else:
            return "BAJO"

    def ver_boletin():
        if not student_combo.get():
            messagebox.showwarning("⚠️", "Seleccione un estudiante")
            return

        student_id = int(student_combo.get().split(" - ")[0])
        estudiante, calificaciones, periodo_actual = obtener_calificaciones(student_id)
        if not estudiante:
            messagebox.showerror("❌ Error", "Estudiante no encontrado")
            return

        nombre_completo = f"{estudiante[0]} {estudiante[1]}"
        identificacion = estudiante[2]
        grado = estudiante[3]

        if not calificaciones:
            preview_text.delete("1.0", "end")
            preview_text.insert("end", f"No hay calificaciones registradas para {nombre_completo}")
            return

        materias = {}
        for materia, periodo, valor in calificaciones:
            if materia not in materias:
                materias[materia] = {1: None, 2: None, 3: None}
            materias[materia][periodo] = valor

        periodo_texto = f"{periodo_actual}ro" if periodo_actual else "N/A"
        
        preview_text.delete("1.0", "end")
        preview_text.insert("end", "INSTITUCIÓN EDUCATIVA DEPARTAMENTAL TÉCNICA AGROPECUARIA LAS MERCEDES\n")
        preview_text.insert("end", "Res. DANE No 025099 de 31 de DICIEMBRE 2021\n")
        preview_text.insert("end", "RECONOCIMIENTO OFICIAL Resolución N° 002145\n\n")
        preview_text.insert("end", f"ESTUDIANTE: {nombre_completo.upper()}\n")
        preview_text.insert("end", f"DIR. GRUPO: {grado}\n")
        preview_text.insert("end", f"GRADO: PRIMERO - 1\n")
        preview_text.insert("end", f"JORNADA: MAÑANA\n")
        preview_text.insert("end", f"PERIODO ACADÉMICO: {periodo_texto}\n")
        preview_text.insert("end", f"AÑO LECTIVO: 2025\n\n")
        preview_text.insert("end", "─" * 100 + "\n")
        preview_text.insert("end", "ÁREAS              ASIGNATURAS         1er Per  2do Per  3ro Per  PROMEDIO  DESEMPEÑO\n")
        preview_text.insert("end", "─" * 100 + "\n")

        for materia, notas in materias.items():
            p = [f"{notas[i]:.1f}" if notas[i] else "--" for i in range(1, 4)]
            valores_validos = [n for n in notas.values() if n is not None]
            promedio = sum(valores_validos) / len(valores_validos) if valores_validos else 0
            desempeno = calcular_desempeno(promedio)
            
            preview_text.insert("end", 
                f"{materia[:25].ljust(25)} {p[0]:>6}   {p[1]:>6}   {p[2]:>6}   {promedio:>6.1f}    {desempeno}\n")

    def generar_pdf_estudiante(estudiante_data=None):
        if estudiante_data:
            estudiante, calificaciones, periodo_actual = estudiante_data
        else:
            if not student_combo.get():
                messagebox.showwarning("⚠️", "Seleccione un estudiante")
                return
            student_id = int(student_combo.get().split(" - ")[0])
            estudiante, calificaciones, periodo_actual = obtener_calificaciones(student_id)

        if not estudiante or not calificaciones:
            messagebox.showerror("❌", "No hay datos para generar el PDF")
            return

        nombre_completo = f"{estudiante[0]} {estudiante[1]}".upper()
        identificacion = estudiante[2]
        grado = estudiante[3]
        pdf_name = f"Boletin_{nombre_completo.replace(' ', '_')}.pdf"
        
        # Determinar texto del período
        periodo_texto = f"{periodo_actual}ro" if periodo_actual else "N/A"

        c = canvas.Canvas(pdf_name, pagesize=letter)
        width, height = letter

        #ENCABEZADO CON LOGOS 
        y_position = height - 40
        
        # Título de la institución (centrado)
        c.setFont("Helvetica-Bold", 9)
        c.drawCentredString(width / 2, y_position, 
            "NOMBRE DE LA INSTITUCIÓN")
        y_position -= 12
        
        c.setFont("Helvetica", 7)
        c.drawCentredString(width / 2, y_position, 
            "Res. DANE No")
        y_position -= 10
        c.drawCentredString(width / 2, y_position, 
            "RECONOCIMIENTO (nombre de la institucion)")
        y_position -= 10
        c.drawCentredString(width / 2, y_position, 
            "CORREGIMIENTO (nombre) - REPUBLICA DE COLOMBIA")
        y_position -= 10
        c.drawCentredString(width / 2, y_position, 
            "Correo: institución - www.institución - Tel: institucion")
        y_position -= 5
        
        c.setFont("Helvetica", 6)
        c.drawRightString(width - 50, y_position, "Libertad y Orden")
        
        # Línea separadora
        y_position -= 8
        c.line(40, y_position, width - 40, y_position)
        y_position -= 20

        #INFORMACIÓN DEL ESTUDIANTE 
        c.setFont("Helvetica", 8)
        
        # Fila 1: Estudiante, Grado, Jornada
        x_labels = 50
        x_values = 120
        
        c.setFont("Helvetica-Bold", 8)
        c.drawString(x_labels, y_position, "ESTUDIANTE")
        c.drawString(300, y_position, "GRADO")
        c.drawString(450, y_position, "JORNADA")
        
        c.setFont("Helvetica", 8)
        c.drawString(x_labels, y_position - 12, f": {nombre_completo}")
        c.drawString(300, y_position - 12, f": PRIMERO - 1")
        c.drawString(450, y_position - 12, f": MAÑANA")
        
        y_position -= 30
        
        # Fila 2: Dir. Grupo, Periodo Académico, Año Lectivo
        c.setFont("Helvetica-Bold", 8)
        c.drawString(x_labels, y_position, "DIR. GRUPO")
        c.drawString(300, y_position, "PERIODO ACADEMICO")
        c.drawString(450, y_position, "AÑO LECTIVO")
        
        c.setFont("Helvetica", 8)
        c.drawString(x_labels, y_position - 12, f": nombre docente")
        c.drawString(300, y_position - 12, f": {periodo_texto}")
        c.drawString(450, y_position - 12, f": 2025")
        
        y_position -= 25

        #TABLA DE CALIFICACIONES
        
        # Organizar calificaciones por materia y período
        materias = {}
        for materia, periodo, valor in calificaciones:
            if materia not in materias:
                materias[materia] = {1: None, 2: None, 3: None}
            materias[materia][periodo] = valor

        # Preparar datos para la tabla
        data = []
        
        # Encabezados
        headers = [
            ['AREAS', 'ASIGNATURAS', 'I.H', 'AU', 
             '1er Per.', '', '2do Per.', '', '3ro Per.', '',
             'PROMEDIO\nASIGNATURA', 'PROMEDIO\nACUMULADO', 'DESEMPEÑO']
        ]
        
        # Sub-encabezados para períodos
        sub_headers = [
            ['', '', '', '', 'Val', 'Rec', 'Val', 'Rec', 'Val', 'Rec', '', '', '']
        ]
        
        data.extend(headers)
        data.extend(sub_headers)
        
        # Usar las materias que realmente están en la base de datos
        for materia_nombre, notas in materias.items():
            # Calcular promedio
            valores_validos = [n for n in notas.values() if n is not None]
            promedio = sum(valores_validos) / len(valores_validos) if valores_validos else 0
            promedio_acumulado = promedio
            desempeno = calcular_desempeno(promedio) if promedio > 0 else ""
            
            # Formatear valores
            p1_val = f"{notas[1]:.1f}" if notas[1] else ""
            p2_val = f"{notas[2]:.1f}" if notas[2] else ""
            p3_val = f"{notas[3]:.1f}" if notas[3] else ""
            prom_str = f"{promedio:.1f}" if promedio > 0 else ""
            prom_acum_str = f"{promedio_acumulado:.1f}" if promedio_acumulado > 0 else ""
            
            # Usar el nombre de la materia como área y asignatura
            row = [
                materia_nombre.upper(),  # AREA
                '',  # ASIGNATURA
                '5',  # I.H (intensidad horaria por defecto)
                '0',  # AU (ausencias)
                p1_val, '',  # Val, Rec periodo 1
                p2_val, '',  # Val, Rec periodo 2
                p3_val, '',  # Val, Rec periodo 3
                prom_str,
                prom_acum_str,
                desempeno
            ]
            data.append(row)

        # Escala de valoración
        data.append(['', 'ESCALA DE VALORACION NACIONAL', '', '', 'BAJO', '', 'BASICO', '', 'ALTO', '', 'SUPERIOR', '', ''])
        data.append(['', 'ESCALA DE VALORACION INSTITUCIONAL', '', '', '1.0 a 5.9', '', '6.0 a 7.99', '', '8.0 a 9.49', '', '9.5 a 10.0', '', ''])
        
        # Crear tabla
        table = Table(data, colWidths=[
            1.0*inch, 1.3*inch, 0.3*inch, 0.3*inch,
            0.35*inch, 0.35*inch, 0.35*inch, 0.35*inch, 0.35*inch, 0.35*inch,
            0.6*inch, 0.7*inch, 0.7*inch
        ])
        
        # Estilo de la tabla
        table_style = TableStyle([
            # Encabezados principales
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 7),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            
            # Sub-encabezados
            ('BACKGROUND', (0, 1), (-1, 1), colors.lightgrey),
            ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 1), (-1, 1), 6),
            ('ALIGN', (0, 1), (-1, 1), 'CENTER'),
            
            # Bordes
            ('GRID', (0, 0), (-1, -3), 0.5, colors.black),
            ('BOX', (0, 0), (-1, -3), 1, colors.black),
            
            # Alineación
            ('ALIGN', (2, 2), (-1, -1), 'CENTER'),
            ('ALIGN', (0, 2), (1, -1), 'LEFT'),
            
            # Fuente del contenido
            ('FONTNAME', (0, 2), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 2), (-1, -3), 7),
            
            # Escala de valoración
            ('BACKGROUND', (0, -2), (-1, -1), colors.lightgrey),
            ('FONTNAME', (0, -2), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, -2), (-1, -1), 6),
            ('ALIGN', (0, -2), (-1, -1), 'CENTER'),
            
            # Valign
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ])
        
        table.setStyle(table_style)
        
        # Dibujar tabla
        table.wrapOn(c, width, height)
        table.drawOn(c, 40, y_position - 320)
        
        y_position -= 340

        #PIE DE PÁGINA CON FIRMAS
        y_position = 120
        
        c.setFont("Helvetica", 7)
        c.drawString(50, y_position, "CONVENCIONES: AU Ausencias, I.H Intensidad Horaria, H.D Horas Dictadas Por El Docente, Val Valoración, Rec Recuperación, Per Periodo")
        
        y_position -= 40
        
        # Líneas para firmas
        c.line(70, y_position, 220, y_position)
        c.line(380, y_position, 530, y_position)
        
        y_position -= 15
        
        c.setFont("Helvetica-Bold", 8)
        c.drawString(80, y_position, "NOMBRE DEL RECTOR")
        c.drawString(390, y_position, "NOMBRE DIRECTOR DE GRUPO")
        
        y_position -= 12
        c.setFont("Helvetica", 7)
        c.drawRightString(220, y_position, "Director(a) de Grupo.")

        c.save()
        os.startfile(pdf_name)
        messagebox.showinfo("✅ PDF Generado", f"Boletín generado: {pdf_name}")

    def generar_pdf_todos():
        conn = sqlite3.connect('calificaciones.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM estudiantes")
        estudiantes_ids = [e[0] for e in cursor.fetchall()]
        conn.close()

        if not estudiantes_ids:
            messagebox.showwarning("⚠️", "No hay estudiantes para generar PDFs")
            return

        for student_id in estudiantes_ids:
            estudiante_data = obtener_calificaciones(student_id)
            if estudiante_data[0] and estudiante_data[1]:
                generar_pdf_estudiante(estudiante_data)

        messagebox.showinfo("✅ PDFs Generados", f"Se generaron los boletines de {len(estudiantes_ids)} estudiantes.")

    #EVENTOS
    btn_ver.config(command=ver_boletin)
    btn_pdf.config(command=generar_pdf_estudiante)
    btn_todos.config(command=generar_pdf_todos)

    cargar_estudiantes()
    preview_text.insert("end", "\n\nSeleccione un estudiante y presione '📊 Ver Boletín' para ver las calificaciones.\n")
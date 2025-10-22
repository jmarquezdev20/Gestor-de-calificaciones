from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import sqlite3, os


def ventana_reportes(parent):
    frame = tk.Frame(parent, bg="#f8f9fa")
    frame.pack(fill='both', expand=True)

    # HEADER
    header = tk.Frame(frame, bg="#2c3e50", height=70)
    header.pack(fill='x')
    header.pack_propagate(False)
    tk.Label(header, text="📄 Reportes y Boletines",
             bg="#2c3e50", fg="white",
             font=("Segoe UI", 18, "bold")).pack(pady=15)

    # SELECCIÓN
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

    # PREVIEW
    preview_frame = tk.Frame(frame, bg="#f8f9fa")
    preview_frame.pack(fill='both', expand=True, padx=20, pady=10)

    tk.Label(preview_frame, text="📋 Vista previa del boletín",
             bg="#f8f9fa", fg="#2c3e50", font=("Segoe UI", 13, "bold")).pack(pady=10)

    preview_text = scrolledtext.ScrolledText(preview_frame,
                                             font=("Consolas", 11),
                                             bg="#ffffff", fg="#2c3e50",
                                             wrap='word', padx=20, pady=20)
    preview_text.pack(fill='both', expand=True)

    # FUNCIONES
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
        notas_raw = cursor.fetchall()

        periodo_actual = max([n[1] for n in notas_raw]) if notas_raw else None

        materias_dict = {}
        for materia, periodo, valor in notas_raw:
            if materia not in materias_dict:
                materias_dict[materia] = {1: None, 2: None, 3: None, 4: None}
            if materias_dict[materia][periodo] is None:
                materias_dict[materia][periodo] = []
            if isinstance(materias_dict[materia][periodo], list):
                materias_dict[materia][periodo].append(valor)

        calificaciones = []
        for materia, periodos in materias_dict.items():
            for periodo in range(1, 5):
                notas = periodos[periodo]
                if isinstance(notas, list) and notas:
                    promedio = sum(notas) / len(notas)
                    periodos[periodo] = round(promedio, 1)
                elif notas is None:
                    periodos[periodo] = "--"

            valores = [v for v in periodos.values() if v != "--"]
            definitiva = round(sum(valores) / len(valores), 1) if valores else 0
            calificaciones.append((materia, periodos[1], periodos[2], periodos[3], periodos[4], definitiva))

        conn.close()
        return estudiante, calificaciones, periodo_actual

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
        grado = estudiante[3]
        periodo_texto = f"{periodo_actual}°" if periodo_actual else "N/A"

        preview_text.delete("1.0", "end")
        preview_text.insert("end", f"INSTITUCIÓN EDUCATIVA DEPARTAMENTAL TÉCNICA AGROPECUARIA LAS MERCEDES\n")
        preview_text.insert("end", f"ESTUDIANTE: {nombre_completo.upper()}\n")
        preview_text.insert("end", f"GRADO: {grado}\n")
        preview_text.insert("end", f"PERIODO ACADÉMICO: {periodo_texto}\n")
        preview_text.insert("end", f"AÑO LECTIVO: 2025\n\n")
        preview_text.insert("end", "─" * 100 + "\n")
        preview_text.insert("end", "MATERIA                 1er   2do   3er   4to   DEFINITIVA\n")
        preview_text.insert("end", "─" * 100 + "\n")

        for materia, p1, p2, p3, p4, definitiva in calificaciones:
            preview_text.insert("end",
                f"{materia[:25].ljust(25)} {str(p1).rjust(6)}  {str(p2).rjust(6)}  {str(p3).rjust(6)}  {str(p4).rjust(6)}  {str(definitiva).rjust(8)}\n"
            )

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
        grado = estudiante[3]
        periodo_texto = f"{periodo_actual}°" if periodo_actual else "N/A"
        pdf_name = f"Boletin_{nombre_completo.replace(' ', '_')}.pdf"

        c = canvas.Canvas(pdf_name, pagesize=letter)
        width, height = letter

        # ENCABEZADO
        c.setFillColor(colors.HexColor("#2c3e50"))
        c.rect(0, height - 70, width, 70, fill=1)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(width / 2, height - 45, "I.E.D TÉCNICA AGROPECUARIA LAS MERCEDES")

        # DATOS DEL ESTUDIANTE
        c.setFillColor(colors.black)
        c.setFont("Helvetica", 10)
        c.drawString(50, height - 100, f"Estudiante: {nombre_completo}")
        c.drawString(350, height - 100, f"Grado: {grado}")
        c.drawString(50, height - 115, f"Periodo Académico: {periodo_texto}")
        c.drawString(350, height - 115, "Año Lectivo: 2025")

        # TABLA DE CALIFICACIONES
        data = [["MATERIA", "1er", "2do", "3er", "4to", "DEFINITIVA"]]
        for materia, p1, p2, p3, p4, definitiva in calificaciones:
            def fmt(v): return f"{v:.1f}" if isinstance(v, (float, int)) else v
            data.append([materia, fmt(p1), fmt(p2), fmt(p3), fmt(p4), fmt(definitiva)])

        table = Table(data, colWidths=[2.2*inch, 0.7*inch, 0.7*inch, 0.7*inch, 0.7*inch, 0.9*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#34495e")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1),
             [colors.whitesmoke, colors.lightgrey])
        ]))

        table.wrapOn(c, width, height)
        table.drawOn(c, 50, height - 400)

        # PIE DE PÁGINA
        c.setFont("Helvetica-Oblique", 8)
        c.setFillColor(colors.grey)
        c.drawCentredString(width / 2, 40, "Sistema de Calificaciones • Generado automáticamente")

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

    btn_ver.config(command=ver_boletin)
    btn_pdf.config(command=generar_pdf_estudiante)
    btn_todos.config(command=generar_pdf_todos)

    cargar_estudiantes()
    preview_text.insert("end", "\nSeleccione un estudiante y presione '📊 Ver Boletín' para ver las calificaciones.\n")

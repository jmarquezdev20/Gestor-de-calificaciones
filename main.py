import tkinter as tk
from tkinter import ttk
from database import crear_tablas
from students import ventana_estudiantes
from materias import ventana_materias
from grades import ventana_notas
from reportes import ventana_reportes

# Crear base de datos
crear_tablas()

#Ventana principal
root = tk.Tk()
root.title("📚 Gestor de Calificaciones")
root.geometry("1100x750")
root.configure(bg="#ecf0f1")
root.minsize(1100, 750)

#Estructura principal
main_container = tk.Frame(root, bg="#bdc3c7")
main_container.pack(fill='both', expand=True, padx=3, pady=3)

#HEADER SUPERIOR 
header_frame = tk.Frame(main_container, bg="#2c3e50", height=110)
header_frame.pack(fill='x')
header_frame.pack_propagate(False)

header_icon = tk.Label(header_frame, text="🧾", font=("Segoe UI Emoji", 42), bg="#2c3e50")
header_icon.pack(side='left', padx=20)

header_text = tk.Frame(header_frame, bg="#2c3e50")
header_text.pack(side='left', pady=15)
tk.Label(header_text, text="GESTOR DE CALIFICACIONES", font=("Segoe UI", 22, "bold"),
         bg="#2c3e50", fg="white").pack(anchor='w')
tk.Label(header_text, text="Sistema de Gestión Académica", font=("Segoe UI", 10),
         bg="#2c3e50", fg="#ecf0f1").pack(anchor='w')

#MENÚ SUPERIOR
menu_frame = tk.Frame(main_container, bg="#34495e", height=60)
menu_frame.pack(fill='x')

content_frame = tk.Frame(main_container, bg="#ecf0f1")
content_frame.pack(fill='both', expand=True)

# Lista para almacenar todos los botones del menú
botones_menu = []
boton_activo = None

def limpiar_vista():
    for widget in content_frame.winfo_children():
        widget.destroy()

def cambiar_vista(vista_func, boton_clickeado):
    global boton_activo
    
    # Restaurar color de todos los botones
    for btn in botones_menu:
        btn.configure(bg="#7f8c8d")
    
    # Marcar el botón activo
    boton_clickeado.configure(bg="#3498db")
    boton_activo = boton_clickeado
    
    # Cambiar vista
    limpiar_vista()
    vista_func(content_frame)

def crear_boton_menu(text, vista_func, color="#7f8c8d", activo="#3498db"):
    def on_enter(e): 
        if btn != boton_activo:
            btn.configure(bg=activo)
    
    def on_leave(e): 
        if btn != boton_activo:
            btn.configure(bg=color)
    
    def on_click():
        cambiar_vista(vista_func, btn)
    
    btn = tk.Button(menu_frame, text=text, command=on_click,
                    bg=color, fg="white", font=("Segoe UI", 11, "bold"),
                    relief='flat', padx=20, pady=10, cursor="hand2")
    btn.pack(side='left', padx=10, pady=10)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    
    botones_menu.append(btn)
    return btn

# Botones del menú
btn_estudiantes = crear_boton_menu("👨‍🎓 Estudiantes", ventana_estudiantes)
btn_materias = crear_boton_menu("📚 Materias", ventana_materias)
btn_notas = crear_boton_menu("📊 Notas", ventana_notas)
btn_reportes = crear_boton_menu("📄 Reportes", ventana_reportes)

# Botón salir
tk.Button(menu_frame, text="🚪 Salir", command=root.quit,
          bg="#e74c3c", fg="white", font=("Segoe UI", 11, "bold"),
          relief='flat', padx=20, pady=10, cursor="hand2").pack(side='right', padx=10, pady=10)

#FOOTER
footer_frame = tk.Frame(main_container, bg="#34495e", height=40)
footer_frame.pack(fill='x', side='bottom')
footer_frame.pack_propagate(False)

footer_label = tk.Label(footer_frame,
                        text="© 2025 Sistema de Gestión Académica | v1.0",
                        font=("Segoe UI", 9),
                        bg="#34495e", fg="#bdc3c7")
footer_label.pack(pady=10)

# Mostrar por defecto la vista de estudiantes y marcar el botón
cambiar_vista(ventana_estudiantes, btn_estudiantes)

root.mainloop()
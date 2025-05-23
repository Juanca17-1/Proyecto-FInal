import tkinter as tk
from tkinter import ttk, messagebox

class FormularioMascota:
    def __init__(self, root, controller, titulo, estado, callback=None):
        self.root = root
        self.controller = controller
        self.callback = callback
        
        self.window = tk.Toplevel(root)
        self.window.title(titulo)
        self.window.geometry("500x600")
        
        self.setup_ui(titulo, estado)
    
    def setup_ui(self, titulo, estado):
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(main_frame, text=titulo, font=('Segoe UI', 14, 'bold')).pack(pady=(0, 20))
        
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(fill=tk.X, pady=5)
        
        campos = [
            ("Nombre:", "entry"),
            ("Tipo:", "combobox", ["Perro", "Gato", "Conejo", "Ave", "Otro"]),
            ("Raza:", "entry"),
            ("Edad:", "spinbox", (0, 30)),
            ("Descripción:", "text"),
            ("Contacto:", "entry")
        ]
        
        self.widgets = {}
        for i, (label, tipo, *args) in enumerate(campos):
            frame = ttk.Frame(form_frame)
            frame.pack(fill=tk.X, pady=5)
            
            ttk.Label(frame, text=label).pack(side=tk.LEFT, padx=5)
            
            if tipo == "entry":
                widget = ttk.Entry(frame)
                widget.pack(side=tk.RIGHT, fill=tk.X, expand=True)
            elif tipo == "combobox":
                widget = ttk.Combobox(frame, values=args[0])
                widget.pack(side=tk.RIGHT, fill=tk.X, expand=True)
                widget.set(args[0][0])
            elif tipo == "spinbox":
                widget = ttk.Spinbox(frame, from_=args[0][0], to=args[0][1])
                widget.pack(side=tk.RIGHT)
            elif tipo == "text":
                widget = tk.Text(frame, height=4)
                widget.pack(side=tk.RIGHT, fill=tk.X, expand=True)
            
            self.widgets[label.lower().replace(":", "")] = widget
        
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X, pady=20)
        
        ttk.Button(buttons_frame, text="Cancelar", command=self.window.destroy).pack(side=tk.RIGHT, padx=5)
        ttk.Button(buttons_frame, text="Guardar", style='Accent.TButton',
                  command=lambda: self.guardar_mascota(estado)).pack(side=tk.RIGHT)
    
    def guardar_mascota(self, estado):
        try:
            mascota_data = {
                'nombre': self.widgets['nombre'].get(),
                'tipo': self.widgets['tipo'].get(),
                'raza': self.widgets['raza'].get(),
                'edad': int(self.widgets['edad'].get()),
                'estado': estado,
                'descripcion': self.widgets['descripción'].get("1.0", tk.END).strip(),
                'contacto': self.widgets['contacto'].get()
            }
            
            if not mascota_data['nombre'] or not mascota_data['tipo'] or not mascota_data['raza']:
                raise ValueError("Complete los campos obligatorios")
            
            self.controller.agregar_mascota(mascota_data)
            messagebox.showinfo("Éxito", "Mascota registrada correctamente")
            self.window.destroy()
            
            if self.callback:
                self.callback()
                
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar: {str(e)}")
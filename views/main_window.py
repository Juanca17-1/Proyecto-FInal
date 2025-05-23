import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import sv_ttk
from controllers.mascota_controller import MascotaController

class PetFinderApp:
    def __init__(self, root):
        self.root = root
        self.controller = MascotaController()
        self.setup_window()
        self.load_assets()
        self.setup_styles()
        self.create_widgets()
    
    def setup_window(self):
        self.root.title("PetFinder Pro")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        sv_ttk.set_theme("dark")
    
    def load_assets(self):
        try:
            self.logo_img = ImageTk.PhotoImage(Image.open("assets/logo.png").resize((150, 50)))
            self.pet_placeholder = ImageTk.PhotoImage(Image.open("assets/pet_placeholder.png").resize((200, 200)))
            self.root.iconphoto(False, ImageTk.PhotoImage(Image.open("assets/logo.png")))
        except:
            self.logo_img = None
            self.pet_placeholder = None
    
    def setup_styles(self):
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#2d2d2d')
        self.style.configure('TLabel', background='#2d2d2d', foreground='white', font=('Segoe UI', 10))
        self.style.configure('Header.TLabel', font=('Segoe UI', 18, 'bold'), foreground='#4fc3f7')
        self.style.configure('Card.TFrame', background='#383838', relief='raised', borderwidth=0)
        self.style.configure('Card.TLabel', background='#383838', font=('Segoe UI', 9))
        self.style.configure('Accent.TButton', font=('Segoe UI', 10, 'bold'), foreground='white', background='#2196F3')
        self.style.map('Accent.TButton', background=[('active', '#1976D2')])
    
    def create_widgets(self):
        self.create_main_frame()
        self.create_header()
        self.create_actions_panel()
        self.create_featured_pets()
    
    def create_main_frame(self):
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    def create_header(self):
        self.header_frame = ttk.Frame(self.main_frame)
        self.header_frame.pack(fill=tk.X, pady=(0, 20))
        
        if self.logo_img:
            ttk.Label(self.header_frame, image=self.logo_img).pack(side=tk.LEFT)
        else:
            ttk.Label(self.header_frame, text="PetFinder Pro", style='Header.TLabel').pack(side=tk.LEFT)
        
        search_frame = ttk.Frame(self.header_frame)
        search_frame.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=10)
        
        self.search_entry = ttk.Entry(search_frame, font=('Segoe UI', 10))
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        ttk.Button(search_frame, text="Buscar", style='Accent.TButton',
                  command=self.buscar_mascotas).pack(side=tk.RIGHT, padx=5)
    
    def create_actions_panel(self):
        actions_frame = ttk.Frame(self.main_frame)
        actions_frame.pack(fill=tk.X, pady=(0, 20))
        
        actions = [
            ("Reportar Mascota Perdida", self.report_lost_pet),
            ("Ofrecer en Adopción", self.offer_adoption),
            ("Estadísticas", self.show_stats)
        ]
        
        for text, command in actions:
            ttk.Button(actions_frame, text=text, style='Accent.TButton', 
                      command=command).pack(side=tk.LEFT, expand=True, padx=5)
    
    def create_featured_pets(self):
        ttk.Label(self.main_frame, text="Mascotas Destacadas", style='Header.TLabel').pack(anchor=tk.W, pady=(10, 5))
        self.featured_pets_frame = ttk.Frame(self.main_frame)
        self.featured_pets_frame.pack(fill=tk.BOTH, expand=True)
        self.create_pet_cards()
    
    def create_pet_cards(self):
        mascotas = self.controller.obtener_mascotas() or [
        ]
        
        for i, mascota in enumerate(mascotas):
            self.create_pet_card(i, mascota if hasattr(mascota, 'to_dict') else mascota)
    
    def create_pet_card(self, index, mascota):
        card = ttk.Frame(self.featured_pets_frame, style='Card.TFrame')
        card.grid(row=index//2, column=index%2, padx=10, pady=10, sticky="nsew")
        self.featured_pets_frame.grid_columnconfigure(index%2, weight=1)
        
        if self.pet_placeholder:
            ttk.Label(card, image=self.pet_placeholder).pack(pady=(10, 5))
        
        info_frame = ttk.Frame(card, style='Card.TFrame')
        info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        datos = mascota.to_dict() if hasattr(mascota, 'to_dict') else mascota
        
        ttk.Label(info_frame, text=datos['nombre'], style='Card.TLabel', 
                 font=('Segoe UI', 12, 'bold')).pack(anchor=tk.W)
        ttk.Label(info_frame, text=f"{datos['tipo']} • {datos['raza']}", 
                 style='Card.TLabel').pack(anchor=tk.W)
        ttk.Label(info_frame, text=f"Edad: {datos['edad']} años", 
                 style='Card.TLabel').pack(anchor=tk.W)
        
        status_color = "#FF5252" if datos['estado'] == "Perdido" else "#4CAF50" if datos['estado'] == "En adopción" else "#2196F3"
        ttk.Label(info_frame, text=datos['estado'], style='Card.TLabel',
                 font=('Segoe UI', 10, 'bold'), foreground=status_color).pack(anchor=tk.W, pady=(5, 0))
        
        btn_frame = ttk.Frame(card, style='Card.TFrame')
        btn_frame.pack(fill=tk.X, padx=10, pady=(5, 10))
        ttk.Button(btn_frame, text="Ver detalles", style='Accent.TButton',
                  command=lambda m=datos: self.show_pet_details(m)).pack(fill=tk.X)
    
    def show_pet_details(self, mascota):
        details_window = tk.Toplevel(self.root)
        details_window.title(f"Detalles de {mascota['nombre']}")
        details_window.geometry("500x400")
        
        main_frame = ttk.Frame(details_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        if self.pet_placeholder:
            ttk.Label(main_frame, image=self.pet_placeholder).pack(pady=10)
        
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(info_frame, text=f"Nombre: {mascota['nombre']}", font=('Segoe UI', 12)).grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Label(info_frame, text=f"Tipo: {mascota['tipo']}", font=('Segoe UI', 12)).grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Label(info_frame, text=f"Raza: {mascota['raza']}", font=('Segoe UI', 12)).grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Label(info_frame, text=f"Edad: {mascota['edad']} años", font=('Segoe UI', 12)).grid(row=3, column=0, sticky=tk.W, pady=5)
        
        status_color = "#FF5252" if mascota['estado'] == "Perdido" else "#4CAF50" if mascota['estado'] == "En adopción" else "#2196F3"
        ttk.Label(info_frame, text=f"Estado: {mascota['estado']}", font=('Segoe UI', 12, 'bold'),
                 foreground=status_color).grid(row=4, column=0, sticky=tk.W, pady=5)
        
        if 'descripcion' in mascota:
            desc_frame = ttk.Frame(main_frame)
            desc_frame.pack(fill=tk.X, pady=10)
            ttk.Label(desc_frame, text="Descripción:", font=('Segoe UI', 12, 'bold')).pack(anchor=tk.W)
            desc_text = tk.Text(desc_frame, height=4, width=50, wrap=tk.WORD)
            desc_text.insert(tk.END, mascota['descripcion'])
            desc_text.config(state=tk.DISABLED)
            desc_text.pack(fill=tk.X, pady=5)
        
        if 'contacto' in mascota:
            contact_frame = ttk.Frame(main_frame)
            contact_frame.pack(fill=tk.X, pady=10)
            ttk.Label(contact_frame, text="Contacto:", font=('Segoe UI', 12, 'bold')).pack(anchor=tk.W)
            ttk.Label(contact_frame, text=mascota['contacto'], font=('Segoe UI', 12)).pack(anchor=tk.W)
        
        ttk.Button(main_frame, text="Cerrar", command=details_window.destroy).pack(pady=10)
    
    def report_lost_pet(self):
        from views.formulario_mascota import FormularioMascota
        FormularioMascota(self.root, self.controller, "Reportar Mascota Perdida", "extraviada", self.actualizar_interfaz)
    
    def offer_adoption(self):
        from views.formulario_mascota import FormularioMascota
        FormularioMascota(self.root, self.controller, "Ofrecer en Adopción", "en_adopcion", self.actualizar_interfaz)
    
    def view_found_pets(self):
        found_pets = self.controller.obtener_mascotas(estado="encontrada")
        if not found_pets:
            tk.messagebox.showinfo("Mascotas Encontradas", "No hay mascotas encontradas recientemente")
            return
        
        found_window = tk.Toplevel(self.root)
        found_window.title("Mascotas Encontradas")
        found_window.geometry("800x600")
        
        main_frame = ttk.Frame(found_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(main_frame, text="Mascotas Encontradas Recientemente", style='Header.TLabel').pack()
        
        pets_frame = ttk.Frame(main_frame)
        pets_frame.pack(fill=tk.BOTH, expand=True)
        
        for i, mascota in enumerate(found_pets):
            self.create_pet_card(i, mascota)
    
    def show_stats(self):
        stats_window = tk.Toplevel(self.root)
        stats_window.title("Estadísticas")
        stats_window.geometry("500x300")
        
        main_frame = ttk.Frame(stats_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(main_frame, text="Estadísticas de Mascotas", style='Header.TLabel').pack()
        
        stats = [
            f"Total mascotas registradas: {len(self.controller.mascotas)}",
            f"Mascotas perdidas: {len(self.controller.obtener_mascotas(estado='extraviada'))}",
            f"Mascotas en adopción: {len(self.controller.obtener_mascotas(estado='en_adopcion'))}"
        ]
        
        for stat in stats:
            ttk.Label(main_frame, text=stat, font=('Segoe UI', 12)).pack(anchor=tk.W, pady=5)
    
    
    def buscar_mascotas(self):
        criterio = "nombre"
        valor = self.search_entry.get().strip()

        resultados = self.controller.buscar_mascotas(criterio, valor)
        if not resultados:
            from tkinter import Toplevel, Label
            ventana = Toplevel(self.root)
            ventana.title("Resultados de Búsqueda")
            ventana.geometry("400x200")
            Label(ventana, text=f"No se encontraron resultados para '{valor}'", font=('Segoe UI', 12)).pack(pady=20)
            return

        from tkinter import Toplevel, Label, Frame, Button
        ventana = Toplevel(self.root)
        ventana.title("Resultados de Búsqueda")
        ventana.geometry("600x400")
        Label(ventana, text=f"Resultados para '{valor}'", font=('Segoe UI', 14, 'bold'), fg='cyan').pack(pady=10)

        for m in resultados:
            frame = Frame(ventana, bg="#2d2d2d", bd=2, relief="groove")
            frame.pack(padx=10, pady=5, fill="x")
            Label(frame, text=f"{m.nombre}", font=('Segoe UI', 10, 'bold'), bg="#2d2d2d", fg="white").pack(anchor="w", padx=10)
            Label(frame, text=f"{m.tipo} - {m.raza}", bg="#2d2d2d", fg="white").pack(anchor="w", padx=10)
            Label(frame, text=f"Edad: {m.edad} años", bg="#2d2d2d", fg="white").pack(anchor="w", padx=10)
            Label(frame, text=m.estado, fg="cyan", bg="#2d2d2d").pack(anchor="w", padx=10)
            Button(frame, text="Ver detalles", bg="#00bfff", fg="white").pack(anchor="e", padx=10, pady=5)
        self.create_pet_cards()

    def actualizar_interfaz(self):
        # Método agregado para evitar errores al reportar mascota perdida o en adopción
        pass
    

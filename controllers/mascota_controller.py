
from models.mascota import Mascota
from models.usuario import Usuario
import csv
import os

class MascotaController:
    def __init__(self):
        self.mascotas = []
        self.usuarios = []
        self.next_id = 1
        self.csv_path = os.path.join(os.path.dirname(__file__), '../mascotas_registradas.csv')
        self._cargar_desde_archivo()
    def _cargar_desde_archivo(self):
        if os.path.exists(self.csv_path):
            with open(self.csv_path, mode='r', encoding='utf-8') as archivo:
                reader = csv.DictReader(archivo)
                for row in reader:
                    mascota = Mascota(
                        id=int(row['ID']),
                        nombre=row['Nombre'],
                        tipo=row['Tipo'],
                        raza=row['Raza'],
                        edad=row['Edad'],
                        estado=row['Estado'],
                        descripcion=row['Descripción'],
                        contacto=row['Contacto']
                    )
                    self.mascotas.append(mascota)
                    self.next_id = max(self.next_id, mascota.id + 1)


    def agregar_mascota(self, mascota_data):
        nueva_mascota = Mascota(
            id=self.next_id,
            nombre=mascota_data['nombre'],
            tipo=mascota_data['tipo'],
            raza=mascota_data['raza'],
            edad=mascota_data['edad'],
            estado=mascota_data['estado'],
            descripcion=mascota_data.get('descripcion', ''),
            contacto=mascota_data.get('contacto', '')
        )
        self.mascotas.append(nueva_mascota)
        self._guardar_en_archivo(nueva_mascota)
        self.next_id += 1
        return nueva_mascota

    def _guardar_en_archivo(self, mascota):
        existe = os.path.exists(self.csv_path)
        with open(self.csv_path, mode='a', newline='', encoding='utf-8') as archivo:
            writer = csv.writer(archivo)
            if not existe:
                writer.writerow(['ID', 'Nombre', 'Tipo', 'Raza', 'Edad', 'Estado', 'Descripción', 'Contacto'])
            writer.writerow([
                mascota.id,
                mascota.nombre,
                mascota.tipo,
                mascota.raza,
                mascota.edad,
                mascota.estado,
                mascota.descripcion,
                mascota.contacto
            ])

    def obtener_mascotas(self, estado=None):
        if estado:
            return [m for m in self.mascotas if m.estado == estado]
        return self.mascotas

    def buscar_mascotas(self, criterio, valor):
        return [m for m in self.mascotas if getattr(m, criterio, '').lower() == valor.lower()]

    def registrar_usuario(self, usuario_data):
        nuevo_usuario = Usuario(
            id=len(self.usuarios) + 1,
            nombre=usuario_data['nombre'],
            email=usuario_data['email'],
            telefono=usuario_data['telefono'],
            direccion=usuario_data.get('direccion', '')
        )
        self.usuarios.append(nuevo_usuario)
        return nuevo_usuario

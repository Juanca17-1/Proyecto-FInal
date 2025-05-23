class Mascota:
    def __init__(self, id, nombre, tipo, raza, edad, estado, foto=None, descripcion="", contacto=""):
        self.id = id
        self.nombre = nombre
        self.tipo = tipo
        self.raza = raza
        self.edad = edad
        self.estado = estado  # "extraviada", "en_adopcion", "encontrada"
        self.foto = foto
        self.descripcion = descripcion
        self.contacto = contacto
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'tipo': self.tipo,
            'raza': self.raza,
            'edad': self.edad,
            'estado': self.estado,
            'descripcion': self.descripcion,
            'contacto': self.contacto
        }
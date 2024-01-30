class Sujeto:
    def __init__(self, nombre, apellido, nif):
        self.nombre = nombre
        self.apellido = apellido
        self.nif = nif

    def to_dict(self):
        return {
            'nombre': self.nombre,
            'apellido': self.apellido,
            'nif': self.nif
        }


import re
import json
from flask import Flask, jsonify
from busquedaBoeB import buscar_boe

app = Flask(__name__)

# TODO: Almacenar las claves env
endpoint = 'https://search-boe.search.windows.net/'
index_name = 'azureblob-index'
# key del servicio search AI
key = 'LkbQQOQVnBN6JSUjkipQtO8y8HGqpjDd4SYWKDyD2WAzSeDIHEye'

class Persona:
    def __init__(self, nombre_apellido, nif, nombre_archivo_pdf, texto_del_pdf):
        self.nombre_apellido = nombre_apellido
        self.nif = nif
        self.nombre_archivo_pdf = nombre_archivo_pdf
        self.texto_del_pdf = texto_del_pdf

    def to_dict(self):
        return {
            'Nombre y Apellido': self.nombre_apellido,
            'NIF': self.nif,
            'Archivo PDF' : self.nombre_archivo_pdf,
            'Texto del BOE' : self.texto_del_pdf
        }

@app.route('/')
def mostrar_resultados():
    # Llamar a la función para obtener los resultados
    resultados = buscar_boe(endpoint, index_name, key)
    
    # Lista para almacenar los NIFs encontrados
    nifs_encontrados = []
    # Guardar resultados con nombre de archivo
    resultados_con_nombre = []
    personas_encontradas = []

    # Definir el patrón de regex para NIF
    patron_nif = re.compile(
        r'\b\d{2}[.]?\d{3}[.]?\d{3}[-]?[A-Za-z]\b', re.IGNORECASE)
    # Definir el patrón de regex para Nombre y Apellido
    patron_nombre_apellido = re.compile(
        r'(?:a|Entidad concursada\.|Entidad concursada\.\s+|deudor|Deudor:|deudor\s+)\s+([A-Za-zÁÉÍÓÚÜÑáéíóúüñ\s]+),?\s*con\s*(?:NIF|DNI)?\s*[A-Za-z\s]*\b\d{2}[.]?\d{3}[.]?\d{3}[-]?[A-Za-z]\b', re.IGNORECASE)

    for resultado in resultados:
        texto_del_pdf = resultado.get('texto_del_pdf', '')
        nombre_archivo_pdf = resultado.get('nombre_archivo_pdf', '')

        coincidencias_nombre_apellido = patron_nombre_apellido.findall(
            texto_del_pdf)

        for match in coincidencias_nombre_apellido:
            nombre_apellido = match.strip(", ")
            nifs = patron_nif.findall(texto_del_pdf)

            for nif in nifs:
                persona = Persona(nombre_apellido, nif, nombre_archivo_pdf, texto_del_pdf)
                personas_encontradas.append(persona)
   
    # Mostrar resultados como JSON
    resultados_json = [persona.to_dict() for persona in personas_encontradas]
    return jsonify(resultados_json)


if __name__ == '__main__':
    app.run(debug=True)
    
    
    
# TODO: Validación de Datos: Es importante validar los datos extraídos para asegurarse de que la correspondencia entre NIF y nombres sea correcta

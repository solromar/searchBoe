import re
from busquedaBoeB import buscar_boe

#TODO: Almacenar las claves env
endpoint = 'https://search-boe.search.windows.net/'
index_name = 'azureblob-index'
key = 'LkbQQOQVnBN6JSUjkipQtO8y8HGqpjDd4SYWKDyD2WAzSeDIHEye' #key del servicio search AI

# Llamar a la función para obtener los resultados
resultados = buscar_boe(endpoint, index_name, key)
#print(resultados)
# Definir el patrón de regex para NIF
patron_nif = re.compile(r'\b\d{2}[.]?\d{3}[.]?\d{3}[-]?[A-Za-z]\b', re.IGNORECASE)
patron_nombre_apellido = re.compile(r'(?:a|Entidad concursada\.|Entidad concursada\.\s+|Que en el Concurso consecutivo 1386/2019 se dictó un auto por el que se ha declarado concluso el concurso y otorgado el BEPI definitivo a|deudor|Deudor:|deudor\s+)\s+([A-Za-zÁÉÍÓÚÜÑáéíóúüñ\s]+),?\s*con\s*(?:NIF|DNI)?\s*[A-Za-z\s]*\b\d{2}[.]?\d{3}[.]?\d{3}[-]?[A-Za-z]\b', re.IGNORECASE)
#patron_nombre_apellido = re.compile(r'([A-Za-zÁÉÍÓÚÜÑáéíóúüñ\s]+),?\s*con\s*[A-Za-z\s]*\b\d{2}[.]?\d{3}[.]?\d{3}[-]?[A-Za-z]\b', re.IGNORECASE)
 
 
                         
# Lista para almacenar los NIFs encontrados
nifs_encontrados = []
# Guardar resultados con nombre de archivo
resultados_con_nombre = []

for resultado in resultados:
    texto_del_pdf = resultado.get('texto_del_pdf', '')
    nombre_archivo_pdf = resultado.get('nombre_archivo_pdf', '')
    # Buscar patrón para extraer nombre y apellido antes del NIF
    coincidencias_nombre_apellido = patron_nombre_apellido.findall(texto_del_pdf)
    
    for match in coincidencias_nombre_apellido:
        nombre_apellido = match.strip(", ")
    nifs = patron_nif.findall(texto_del_pdf)
    nifs_encontrados.extend(nifs)

    # Guardar resultados con nombre de archivo
    for nif in nifs:
        resultados_con_nombre.append({
            'nombre_archivo': nombre_archivo_pdf,
            'nombre_apellido': nombre_apellido,
            'valor': nif,
            'tipo': 'NIF',
            
        })    

# Imprimir el total de NIFs y CIFs encontrados
print(f"Total de NIFs: {len(nifs_encontrados)}")

# Imprimir nombre de archivo junto con cada NIF 
for resultado in resultados_con_nombre:
    print(f"Nombre del archivo: {resultado['nombre_archivo']}, Tipo: {resultado['tipo']}, Valor: {resultado['valor']}, Nombre y Apellido: {resultado['nombre_apellido']},")

# Guarda todos los resultados encontrados en un archivo txt
with open('aditionalFunctions/txt/resultados_persona.txt', 'w', encoding='utf-8') as file:
    for resultado in resultados_con_nombre:
        file.write(f"Nombre del archivo: {resultado['nombre_archivo']},Nombre y Apellido: {resultado['nombre_apellido']}, Tipo: {resultado['tipo']}, Valor: {resultado['valor']}\n")
        
# Ahora 'nifs_encontrados' contiene todos los NIFs encontrados en los textos

#TODO: Validación de Datos: Es importante validar los datos extraídos para asegurarse de que la correspondencia entre NIF y nombres sea correcta
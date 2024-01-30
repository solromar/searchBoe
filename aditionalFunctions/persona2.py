import re
from busquedaBoeB import buscar_boe

#TODO: Almacenar las claves env
endpoint = 'https://search-boe.search.windows.net/'
index_name = 'azureblob-index'
key = 'LkbQQOQVnBN6JSUjkipQtO8y8HGqpjDd4SYWKDyD2WAzSeDIHEye' #key del servicio search AI

# Llamar a la función para obtener los resultados
resultados = buscar_boe(endpoint, index_name, key)

# Definir el patrón de regex para NIF
patron_nif = re.compile(r'\b\d{2}[.]?\d{3}[.]?\d{3}[-]?[A-Za-z]\b', re.IGNORECASE)
#patron_cif = re.compile(r'[A-Z]{1}[0-9]{7}[A-J0-9]{1}')
patron_cif = re.compile(r'[A-Za-z]{1}[-]?[0-9]{8}[A-J0-9]{1}')

                         
# Lista para almacenar los NIFs encontrados
nifs_encontrados = []
cifs_encontrados = []

# Guardar resultados con nombre de archivo
resultados_con_nombre = []

for resultado in resultados:
    texto_del_pdf = resultado['texto_del_pdf']
    nombre_archivo_pdf = resultado['nombre_archivo_pdf']
    nifs = patron_nif.findall(texto_del_pdf)
    cifs = patron_cif.findall(texto_del_pdf)
    nifs_encontrados.extend(nifs)  # Añadir los NIFs encontrados a la lista
    cifs_encontrados.extend(cifs)

# Imprimir el total de NIFs y CIFs encontrados
total_nifs = len(nifs_encontrados)
total_cifs = len(cifs_encontrados)
print(f"Total de NIFs: {len(nifs_encontrados)}")
print(f"Total de NIFs: {nifs_encontrados}\n")
print(f"Total de CIFs: {len(cifs_encontrados)}")
print(f"Total de CIFs: {cifs_encontrados}")


# Guarda todos los resultados encontrados en un archivo txt
with open('resultados_nif_cif.txt', 'w', encoding='utf-8') as file:
    file.write(f"Total de NIFs: {total_nifs}\n")
    file.write("NIFs encontrados:\n")
    for nif in nifs_encontrados:
        file.write(f"{nif}\n")

    file.write(f"\nTotal de CIFs: {total_cifs}\n")
    file.write("\nCIFs encontrados:\n")
    for cif in cifs_encontrados:
        file.write(f"{cif}\n") 
        
# Ahora 'nifs_encontrados' contiene todos los NIFs encontrados en los textos

#TODO: Validación de Datos: Es importante validar los datos extraídos para asegurarse de que la correspondencia entre NIF y nombres sea correcta
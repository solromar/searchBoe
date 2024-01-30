from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential


#TODO: Almacenar las claves env
endpoint = 'https://search-boe.search.windows.net/'
index_name = 'azureblob-index'
key = 'LkbQQOQVnBN6JSUjkipQtO8y8HGqpjDd4SYWKDyD2WAzSeDIHEye' #key del servicio search AI

# --------------------- Busca en el index de Search AI los BOE B que corresponden a 2da Oportunidad ------------------------#

def buscar_boe(endpoint, index_name, key):
    # Create Azure SDK client
    client = SearchClient(endpoint=endpoint, index_name=index_name, credential=AzureKeyCredential(key))

    # Frases y palabras exclusivas de búsqueda para los BOE de la ley de segunda oportunidad
    search_terms = ["ley concursal", "concursado", "beneficio de exoneracion del pasivo insatisfecho", 
                    "concurso al deudor", "administracion concursal", "autodeclaracion de concurso", 
                    "concurso abreviado consecutivo"]

    # Convertir los términos de búsqueda en una consulta
    search_query = " OR ".join(f'"{term}"' for term in search_terms)

    # Añadir filtros adicionales que deben contener OBLIGATORIAMENTE las frases "IV. Administración de Justicia" y "JUZGADOS DE LO MERCANTIL"
    search_query += 'AND "JUZGADOS DE LO MERCANTIL"'

    # Crear una lista vacía para almacenar los resultados de la búsqueda
    resultados = []

    for result in client.search(search_text=search_query, 
                                   filter="metadata_storage_name ge 'BOE-B-' and metadata_storage_name lt 'BOE-C-'", #Filtra solo los BOE B
                                   select="metadata_storage_name, extracted_content"):#devuelve los campos del index que contienen el nombre del archivo y su texto
        # Crear un diccionario con el nombre del archivo y su contenido extraído
        resultado = {
            "nombre_archivo_pdf": result['metadata_storage_name'],
            "texto_del_pdf": result['extracted_content']
        }
        
        # Verifica si las frases a excluir están presentes en el texto del PDF para no traer esos textos
        frases_a_excluir = ["Anuncio de subasta judicial", "Anuncio de subasta judicial concursal", "Anuncio de subasta", "judicial concursal"]
        if not any(frase.lower() in resultado["texto_del_pdf"].lower() for frase in frases_a_excluir):
            # Añadir el diccionario a la lista de resultados solo si no contiene las frases a excluir
            resultados.append(resultado)
        
    
    # Filtrar resultados para asegurarse de que contienen las frases con saltos de línea ya que los BOE 2ºOportunidad solo se encuentran en IV. Administración de Justicia JUZGADOS DE LO MERCANTIL
    resultados_filtrados = []
    for resultado in resultados:
        texto = resultado['texto_del_pdf']
        if "\nIV. Administración de Justicia\n" in texto and "\nJUZGADOS DE LO MERCANTIL\n" in texto:
            resultados_filtrados.append(resultado)
    
    return resultados_filtrados

# ---------------------- Guarda en un TXT el total de archivos encontrados, con su nombre y su texto --------------------------------#

def guardar_resultados_en_txt(resultados, nombre_archivo):
    with open(nombre_archivo, 'w', encoding='utf-8') as file:
        for result in resultados:
            total_archivos = len(resultados)
            file.write(f"Total de archivos PDF encontrados: {total_archivos}\n")
            file.write(f"Nombre de Archivo PDF: {result['nombre_archivo_pdf']}\n")
            file.write(f"Texto del PDF: {result['texto_del_pdf']}\n\n")
            
            
# ----------------------------------------------------------------------------------------------------------------------------------#            

if __name__ == "__main__":
    
    # Llamar a la función para obtener los resultados
    resultados = buscar_boe(endpoint, index_name, key)
    
    buscar_boe(endpoint, index_name, key)

    # Llamar a la función que guarda los resultados en un archivo TXT
    guardar_resultados_en_txt(resultados, 'aditionalFunctions/txt/resultadosBusquedaBoeB.txt')


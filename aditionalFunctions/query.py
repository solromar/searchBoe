
import os
import re
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

service_endpoint = 'https://search-boe.search.windows.net/'
index_name = 'azureblob-index'
key = 'LkbQQOQVnBN6JSUjkipQtO8y8HGqpjDd4SYWKDyD2WAzSeDIHEye'

def search_documents(query):
    search_client = SearchClient(service_endpoint, index_name, AzureKeyCredential(key))

    # Definir los parámetros de búsqueda, en este caso utilizando la consulta especificada.
    search_results = search_client.search(search_text=query)

    print(f"Documents containing '{query}':")
    for result in search_results:
        document_id = result["metadata_storage_name"]
        score = result["@search.score"]
        text = result["content"]
        fecha = result["metadata_creation_date"]
        print("    Document ID: {} (Score: {}) Fecha: {}  ".format(document_id, score,  fecha))

def extract_nif_from_text(text):
    # Puedes ajustar este patrón según la estructura específica del NIF en tus documentos
    nif_pattern = r'\b\d{8}[a-zA-Z]\b'
    nif_matches = re.findall(nif_pattern, text)
    return nif_matches


     
        
#if __name__ == '__main__':
    query_to_search_nif = '11731641p'
    search_results = search_documents(query_to_search_nif)

    
    
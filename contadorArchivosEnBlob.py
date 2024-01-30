from azure.storage.blob import BlobServiceClient

def contar_pdfs_por_tipo_en_azure(contenedor_nombre, conexion_string, ruta_especifica):
    total_contador = 0
    boe_a_contador = 0
    boe_b_contador = 0
    boe_s_contador = 0

    blob_service_client = BlobServiceClient.from_connection_string(conexion_string)
    contenedor_client = blob_service_client.get_container_client(contenedor_nombre)

    blob_list = contenedor_client.list_blobs(name_starts_with=ruta_especifica)

    for blob in blob_list:
        if blob.name.lower().endswith('.pdf'):
            total_contador += 1
            if 'boe-a' in blob.name.lower():
                boe_a_contador += 1
            elif 'boe-b' in blob.name.lower():
                boe_b_contador += 1           
            elif 'boe-s' in blob.name.lower():
                boe_s_contador += 1

    return total_contador, boe_a_contador, boe_b_contador, boe_s_contador

# Cuenta la cantidad de archivos pdfs de cada tipo en un blob y en una carpeta en especifico
contenedor_nombre = 'boe'
conexion_string = "DefaultEndpointsProtocol=https;AccountName=ifinancierastorage;AccountKey=Mk762JjOjWLCYiWkbXtRg6UU/4U84+aobQuxFuCIsmAwm6EMs0WV92fmBvbiOCYUwsvHHPFmO53r+ASt7jjlFg==;EndpointSuffix=core.windows.net"
ruta_especifica = 'dias/2021/05/01/pdfs'
total_pdfs, total_pdfs_boe_a, total_pdfs_boe_b, total_pdfs_boe_s = contar_pdfs_por_tipo_en_azure(contenedor_nombre, conexion_string, ruta_especifica)
print(f"Total de archivos PDF en Azure Blob Storage: {total_pdfs}")
print(f"Total de archivos PDF 'BOE-A': {total_pdfs_boe_a}")
print(f"Total de archivos PDF 'BOE-B': {total_pdfs_boe_b}")
print(f"Total de archivos PDF 'BOE-S': {total_pdfs_boe_s}")





import os

import requests
from bs4 import BeautifulSoup

url_semilla = "https://file-examples.com/index.php/sample-documents-download/sample-xls-download/"

resp = requests.get(url_semilla)
soup = BeautifulSoup(resp.text, 'lxml')

urls = []

descargas = soup.find_all('a', class_="download-button")
for descarga in descargas:
    urls.append(descarga["href"])
print(urls)
i = 0

download_dir = './archivos'  # Store the directory path in a variable

if not os.path.exists(download_dir):  # Check if the directory exists
    os.makedirs(download_dir)       # Create the directory if it doesn't exist
elif not os.path.isdir(download_dir): # Check if exists and is a directory
    print(f"Error: {download_dir} exists, but it's not a directory.")
    exit() # Or handle the error as you see fit



for url in urls: # Por cada url de los archivos que quiero descargar
    r = requests.get(url, allow_redirects=True)
    nombre_archivo = download_dir + str(i)+ '.xls'
    output = open(nombre_archivo, 'wb')
    output.write(r.content) # Escribir el archivo en mi PC
    output.close()
    i += 1

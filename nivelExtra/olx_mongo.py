from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import random
from time import sleep
from pymongo.mongo_client import MongoClient

# Configuración de opciones del navegador
opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36")
opts.add_argument("--disable-search-engine-choice-screen")

# Iniciar WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
driver.get('https://www.olx.in/cars_c84')

# Espera explícita
wait = WebDriverWait(driver, 10)

# Desplazar para cargar más elementos
for _ in range(3):  # Ajustar número de desplazamientos
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(random.uniform(1, 3))

# creo funcion para extraer datos de coches
def extraer_datos(autos, collection):
    """Extrae y muestra datos de una lista de elementos de autos y los guarda en MongoDB."""
    for auto in autos:
        precio = auto.find_element(By.XPATH, './/span[@data-aut-id="itemPrice"]').text if auto.find_elements(By.XPATH, './/span[@data-aut-id="itemPrice"]') else "No disponible"
        titulo = auto.find_element(By.XPATH, './/div[@data-aut-id="itemTitle"]').text if auto.find_elements(By.XPATH, './/div[@data-aut-id="itemTitle"]') else "No disponible"
        print(f"Precio: {precio}")
        print(f"Título: {titulo}")

        # Guardar en MongoDB
        car_data = {"precio": precio, "titulo": titulo}
        collection.insert_one(car_data)

# Buscar elementos de autos
autos = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//li[@data-aut-id="itemBox2"]')))
print(f"Cantidad de autos encontrados: {len(autos)}")

# Configuración de MongoDB
MONGODB_URI = "mongodb+srv://ivanroscuenca:<dbpassword>@cluster0.wqa40.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGODB_URI)
db = client.get_database("olx_cars")  # Nombre de la base de datos
collection = db.get_collection("cars")  # Nombre de la colección

# Extraer información y guardar en MongoDB
extraer_datos(autos, collection)

try:
    # Esperar a que el botón esté visible y selecciono página 2
    wait = WebDriverWait(driver, 10)
    boton_pagina = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@data-aut-id="pageItem" and text()="2"]')))

    # Hacer clic en el botón de la página 2
    boton_pagina.click()
    print("Navegando a la página 2...")
    sleep(2)  # Esperar a que la página se cargue completamente

    # Continuar con la extracción de datos en la nueva página
except Exception as e:
    print(f"Error al intentar cambiar de página: {e}")

# Buscar elementos de autos
autos = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//li[@data-aut-id="itemBox2"]')))
print(f"Cantidad de autos encontrados: {len(autos)}")
extraer_datos(autos, collection)

driver.quit()
client.close()

# Nivel 3
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import random

# Configuración de opciones del navegador
opts = Options()
opts.add_argument(
    "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36")
opts.add_argument("--disable-search-engine-choice-screen")

# Iniciar WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                          options=opts)
#driver.get('https://listado.mercadolibre.com.ec/deportes-y-fitness/basketball')
#driver.get('https://listado.mercadolibre.com.ar/basket')
#driver.get('https://listado.mercadolibre.com.uy/basket')
driver.get('https://listado.mercadolibre.co.cr/zapatos-zapatillas')

# Espera explícita
wait = WebDriverWait(driver, 5)

# Desplazar para cargar más elementos
for _ in range(3):  # Ajustar número de desplazamientos
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(random.uniform(1, 3))
while True:
    links_productos = driver.find_elements(By.XPATH,
                                           '//h2[@class="poly-box poly-component__title"]//a')
    links_pagina = []
    for tag_a in links_productos:
        links_pagina.append(tag_a.get_attribute('href'))
    for link in links_pagina:
        try:
            driver.get(link)
            titulo = driver.find_elements(By.XPATH, '//h1[@class="ui-pdp-title"]')
            if titulo:
                titulo1 = titulo[0].text
                print(f"Título del producto: {titulo1}")
            else:
                print("Título del producto no disponible.")

            precio = driver.find_elements(By.CLASS_NAME,
                                          'andes-money-amount__fraction')
            if precio:
                precio1 = precio[0].text
                print(f"Precio del producto: {precio1}")
            else:
                print("Precio del producto no disponible.")

            driver.back()
            print('vuelta a pagina principal')

        except Exception as e:
            print(e)
            driver.back()

    # Esperar a que el botón esté visible y selecciono página siguiente
    # Esperar al botón "Siguiente" y hacer clic
    # Navegar entre páginas

    try:
        print("Esperando al botón 'Siguiente'...")
        boton_siguiente = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@title="Siguiente"]')))
        boton_siguiente.click()
        print('Se ha ido a pagina 2')
        sleep(random.uniform(2, 4))
    except Exception as e:
        print(f"No se pudo hacer clic en el botón 'Siguiente': {e}")
        break


driver.quit()


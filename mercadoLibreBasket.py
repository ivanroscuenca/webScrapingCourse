from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep

# Configuración de opciones del navegador
opts = Options()
opts.add_argument(
    "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36")
opts.add_argument("--disable-search-engine-choice-screen")

# Iniciar WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                          options=opts)
driver.get('https://listado.mercadolibre.com.ec/deportes-y-fitness/basketball')

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
# Localiza el botón "Siguiente" usando su clase y haz clic en él
boton_siguiente = driver.find_element(By.CLASS_NAME, 'andes-pagination__link')
boton_siguiente.click()
print("Se hizo clic en el botón 'Siguiente'")


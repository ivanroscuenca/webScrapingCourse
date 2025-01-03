#Nivel 3
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import \
    ChromeDriverManager  # pip install webdriver-manager

opts = Options()
opts.add_argument(
    "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")
# Agregar a todos sus scripts de selenium para que no aparezca la ventana de seleccionar navegador por defecto: (desde agosto 2024)
opts.add_argument("--disable-search-engine-choice-screen")
#evitar que se abra el navegador
#opts.add_argument('--headless')

# Descarga automática del ChromeDriver
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=opts
)

driver.get('https://queramic.com/grifos-de-cocina/')
sleep(3)


def extract_titles(driver):
    titulos = driver.find_elements(By.XPATH,
                                   '//a[@class="stsb_mini_product_name stsb_flex_wrapper"]')
    for titulo in titulos:
        texto = titulo.text.strip()  # Eliminar espacios en blanco al principio y al final
        if texto:  # Verificar si el texto no está vacío
            print(texto)


extract_titles(driver)

try:
    # Esperar a que el botón esté visible y selecciono página 2
    wait = WebDriverWait(driver, 10)
    boton_pagina2 = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//a[@class=" stsb_page js-search-link"]')))

    # Hacer clic en el botón de la página 2
    boton_pagina2.click()
    print("Navegando a la página 2...")
    sleep(2)  # Esperar a que la página se cargue completamente
    extract_titles(driver)

    # Continuar con la extracción de datos en la nueva página
except Exception as e:
    print(f"Error al intentar cambiar de página: {e}")

driver.quit()


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
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36")
opts.add_argument("--disable-search-engine-choice-screen")

# Iniciar WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
driver.get('https://listado.mercadolibre.com.ec/deportes-y-fitness/basketball')

links_productos = driver.find_elements(By.XPATH,'//h2[@class="poly-box poly-component__title"]//a')
links_pagina = []
for tag_a in links_productos:
    links_pagina.append(tag_a.get_attribute('href'))
for link in links_pagina:
    try:
        driver.get(link)
    except:
        print('error')


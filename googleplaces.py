import random
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import \
    ChromeDriverManager  # pip install webdriver-manager

# Script de Scrolling
scrollingScript = """ 
    document.getElementsByClassName('e07Vkf kA9KIf')[0].scroll(0, 20000)
"""

# Configuración del User-Agent y opciones del navegador
opts = Options()
opts.add_argument(
    "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
)
opts.add_argument("--disable-search-engine-choice-screen")

# Inicializar WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                          options=opts)
driver.get(
    "https://www.google.com/maps/place/Restaurante+Amazonico/@40.423706,-3.6872655,17z/data=!4m7!3m6!1s0xd422899dc90366b:0xce28a1dc0f39911d!8m2!3d40.423706!4d-3.6850768!9m1!1b1"
)

sleep(random.uniform(4.0, 5.0))

# Realizar scroll en la página principal
SCROLLS = 0
while SCROLLS != 3:
    driver.execute_script(scrollingScript)
    sleep(random.uniform(5, 6))
    SCROLLS += 1

# Extraer reseñas
reviews_restaurante = driver.find_elements(By.XPATH,
                                           '//div[contains(@class, "jJc9Ad ")]')

for review in reviews_restaurante:
    userLink = review.find_element(By.XPATH, './/button[@class="al6Kxe"]')
    try:
        # Guardar pestañas abiertas antes del clic
        current_tabs = driver.window_handles

        # Hacer clic en el enlace del usuario
        userLink.click()
        sleep(2)  # Espera para que la nueva pestaña se cargue

        # Verificar si se abrió una nueva pestaña
        if len(driver.window_handles) > len(current_tabs):
            driver.switch_to.window(
                driver.window_handles[-1])  # Cambiar a la nueva pestaña
            try:
                # Esperar el botón de opiniones y hacer clic
                boton_opiniones = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH,
                                                    '//div[contains(@class, "Gpq6kf fontTitleSmall") and text()="Reseñas"]'))
                )
                boton_opiniones.click()

                # Realizar scroll y obtener las reseñas del usuario
                USER_SCROLLS = 0
                while USER_SCROLLS != 3:
                    driver.execute_script(scrollingScript)
                    sleep(random.uniform(5, 6))
                    USER_SCROLLS += 1

                # Extraer reseñas del usuario
                userReviews = driver.find_elements(By.XPATH,
                                                   '//div[contains(@class,"jJc9Ad ")]')
                for userReview in userReviews:
                    # Verificar si la descripción existe, de lo contrario usar "Sin comentarios"
                    descripcion_element = userReview.find_elements(By.XPATH,
                                                                   './/span[@class="wiI7pd"]')  # Usar find_elements para evitar excepciones
                    descripcion = descripcion_element[
                        0].text if descripcion_element else "Sin comentarios"

                    # Verificar si el rating existe, de lo contrario usar "0"
                    rating_element = userReview.find_elements(By.XPATH,
                                                              './/span[@class="kvMYJc"]')  # Usar find_elements para evitar excepciones
                    rating = rating_element[0].get_attribute(
                        'aria-label') if rating_element else "0"

                    print(descripcion)
                    print(rating)
            finally:
                driver.close()  # Cerrar la pestaña actual
                driver.switch_to.window(
                    driver.window_handles[0])  # Regresar a la pestaña principal
        else:
            print("No se abrió una nueva pestaña para el usuario.")
    except Exception as e:
        print(f"Error al procesar la reseña del usuario: {e}")
        if len(driver.window_handles) > 1:
            driver.close()
        driver.switch_to.window(driver.window_handles[0])

# Cerrar el navegador al finalizar
driver.quit()

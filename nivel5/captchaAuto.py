from selenium import webdriver
from time import sleep
import requests
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Configuración de Selenium
opts = Options()
opts.add_argument(
    "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)

# URL de la página con reCAPTCHA
url = 'https://www.google.com/recaptcha/api2/demo'
driver.get(url)

try:
    # Obtengo el identificador único del captcha
    captcha_key = driver.find_element(By.ID, 'recaptcha-demo').get_attribute('data-sitekey')

    # Armo el requerimiento a 2Captcha
    api_url = "https://2captcha.com/in.php?"
    api_url += "key=359681215a18407ad2edefe651e4a8f8"  # API KEY 2CAPTCHA
    api_url += "&method=userrecaptcha"
    api_url += "&googlekey=" + captcha_key
    api_url += "&pageurl=" + url  # URL de la página con reCAPTCHA
    api_url += "&json=0"

    print("URL de la API de 2Captcha:", api_url)  # Visualizo URL

    # Hago un requerimiento GET con requests a la URL del API de 2captcha
    respuesta_requerimiento = requests.get(api_url)
    # Ellos encolan el captcha para ser resuelto y nos dan un ID para consultar el estado del captcha
    captcha_service_key = respuesta_requerimiento.text

    print("Respuesta de 2Captcha:", captcha_service_key)
    # Parseo la respuesta para obtener el ID que nuestro captcha tiene en el sistema de 2CAPTCHA
    if '|' in captcha_service_key:
        captcha_service_key = captcha_service_key.split('|')[-1]
    else:
        raise Exception("Error al enviar el captcha a 2Captcha: " + captcha_service_key)

    # Armo el requerimiento para consultar si el captcha ya se encuentra resuelto
    url_resp = "https://2captcha.com/res.php?"
    url_resp += "key=549e65d80665da200ed415388e9dcfc4"  # API KEY
    url_resp += "&action=get"
    url_resp += "&id=" + captcha_service_key  # ID del captcha en el sistema de 2CAPTCHA obtenido previamente
    url_resp += "&json=0"

    print("URL para consultar el estado del captcha:", url_resp)

    # Espero 20 segundos tal y como me lo indican sus instrucciones
    sleep(20)

    # Entro en un lazo para consultar el estado del captcha hasta que esté resuelto
    while True:
        respuesta_solver = requests.get(url_resp)
        respuesta_solver = respuesta_solver.text
        print("Estado del captcha:", respuesta_solver)
        # Si el captcha no está listo, espero 5 segundos, itero nuevamente en el lazo y vuelvo a preguntar
        if respuesta_solver == "CAPCHA_NOT_READY":
            sleep(5)
        # Caso contrario, el captcha está resuelto y puedo romper el lazo
        else:
            break

    # Obtengo la solución del captcha que me devolvió el API de 2CAPTCHA
    if '|' in respuesta_solver:
        respuesta_solver = respuesta_solver.split('|')[-1]
    else:
        raise Exception("Error al resolver el captcha: " + respuesta_solver)

    print("Solución del captcha:", respuesta_solver)

    # Utilizo el script que tienen en su documentación para insertar la solución dentro de la página web
    insertar_solucion = 'document.getElementById("g-recaptcha-response").innerHTML="' + respuesta_solver + '";'
    print("Script para insertar la solución:", insertar_solucion)

    # Ejecuto el script con Selenium
    driver.execute_script(insertar_solucion)

    # Doy click en el botón de submit y debería avanzar
    submit_button = driver.find_element(By.XPATH, '//input[@id="recaptcha-demo-submit"]')
    submit_button.click()

    # Espero un momento para que la página cargue después de resolver el captcha
    sleep(5)

    # Extraigo la información detrás del captcha
    contenido = driver.find_element(By.CLASS_NAME, 'recaptcha-success')
    print("Contenido después de resolver el captcha:", contenido.text)

except Exception as e:
    print("Error:", e)

finally:
    # Cierro el navegador
    driver.quit()
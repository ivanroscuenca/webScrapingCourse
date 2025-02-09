from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

opts = Options()
opts.add_argument(
    "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)

url = 'https://www.google.com/recaptcha/api2/demo'
driver.get(url)

try:

    # Para interactuar con los elementos dentro de un iframe tengo que realizar
    # un cambio de contexto hacia el iframe
    driver.switch_to.frame(driver.find_element('xpath', '//iframe'))
    # Luego yo ya puedo buscar elementos dentro del iframe e interactuar con estos
    captcha = driver.find_element('xpath', '//div[@class="recaptcha-checkbox-border"]')
    captcha.click()

    # El script se detiene para esperar que el usuario apriete ENTER en terminal, luego de resolver el catpcha
    input()

    # Una vez resuelto el captcha, devolvemos el driver al contexto de la pagina principal
    # Es decir, salimos del iframe
    driver.switch_to.default_content()

    # Damos click en el boton de submit
    submit_button = driver.find_element('xpath', '//input[@id="recaptcha-demo-submit"]')
    submit_button.click()

except Exception as e:
    print(e)

# Me voy a encontrar aqui solamente si he resuelto el captcha
print("Ya he resuelto el captcha")

# Extraigo la informacion que estaba detras del captcha
contenido = driver.find_element(By.CLASS_NAME, 'recaptcha-success')
print(contenido.text)
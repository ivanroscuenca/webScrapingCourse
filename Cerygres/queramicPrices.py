from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import datetime


# Flag to track if cookies have been accepted
cookies_accepted = False

opts = Options()
opts.add_argument(
    "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")
opts.add_argument("--disable-search-engine-choice-screen")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=opts
)

ean_codes = ['CALP', 'CALI', 'CALF', 'XXXX', 'CACO']
results = {}

for ean_code in ean_codes:
    driver.get('https://queramic.com/#3eb1/fullscreen/m=and&q=')

    # Locate the search bar element using its id or name attribute
    search_bar = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "dfd-searchbox-input"))  # Replace with the actual ID or name of the search bar
    )

    # Clear any pre-filled text in the search bar
    search_bar.clear()

    # Send the EAN code to the search bar and submit the search
    search_bar.send_keys(ean_code)
    search_bar.send_keys(Keys.RETURN)

    # Wait for the search results to load (modify as needed)
    time.sleep(3)

    # Accept cookies only once per session
    if not cookies_accepted:
        try:
            accept_cookies_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".cookiesplus-btn.cookiesplus-accept"))
            )
            accept_cookies_button.click()
            cookies_accepted = True  # Set flag after successful click

        except TimeoutException:
            print(f"No se pudo encontrar el botón de aceptar cookies para {ean_code}")
        except Exception as e:
            print(f"Error al procesar {ean_code} (aceptando cookies): {e}")

    # Proceed with price extraction
    try:
        result_element = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='dfd-meta']//strong[text()='1']"))
        )

        # Wait a short time for potential JavaScript updates (adjust the wait time as needed)
        time.sleep(2)

        price_element = result_element.find_element(By.XPATH, "//span[@class='dfd-card-price']")
        # Extraer el valor del atributo data-value
        price = price_element.get_attribute("data-value")
        print(f"Precio para {ean_code}: {price}")
        results[ean_code] = price

    except TimeoutException:
        print(f"No se encontró el resultado '1' para {ean_code}")
        results[ean_code] = 0

    except Exception as e:
        print(f"Error al procesar {ean_code}: {e}")
        results[ean_code] = 0

print("Resultados:", results)

# Crear un DataFrame a partir de los resultados
df = pd.DataFrame.from_dict(results, orient='index', columns=['precio'])
df.reset_index(inplace=True)
df.columns = ['ean_code', 'precio']

# Obtener la fecha actual en formato AAAA-MM-DD
fecha_actual = datetime.date.today().strftime('%d-%m-%Y')

# Guardar el DataFrame en el CSV
nombre_archivo = f"preciosQueramic_{fecha_actual}.csv"
df.to_csv(nombre_archivo, index=False)
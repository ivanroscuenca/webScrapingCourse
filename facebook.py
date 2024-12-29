from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager # pip install webdriver-manager


# Funcion para hacer un Scrolling SUAVIZADO dependiendo de cuantos scrollings ya he hecho
# Mientras mas escrolls llevo dando, mas pixeles voy bajando
# Para esto utilizo el scrolling que voy haciendo actualmente para bajar hasta cierta posicion en la pagina
def hacer_scrolling_suavizado(driver, iteracion):
    bajar_hasta = 2000 * (iteracion + 1)
    inicio = (iteracion * 2000) # Inicio donde termine la anterior iteracion
    for i in range(inicio, bajar_hasta, 10): # Cada vez avanzo 5 pixeles
        scrollingScript = f""" 
          window.scrollTo(0, {i})
        """
        driver.execute_script(scrollingScript)

opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
# Agregar a todos sus scripts de selenium para que no aparezca la ventana de seleccionar navegador por defecto: (desde agosto 2024)
opts.add_argument("--disable-search-engine-choice-screen")
#opts.add_argument("--headless") # Headless Mode

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)

driver.get('https://www.facebook.com/elcorteingles')
sleep(2)


# Boton cookies con Espera explícita
wait = WebDriverWait(driver, 2)
boton_cookies = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[not(@aria-disabled) and @aria-label="Permitir todas las cookies"]')))
boton_cookies.click()
print('cookies aceptadas')
sleep(0.5)

# Boton X con espera
wait = WebDriverWait(driver, 2)
boton_X = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@aria-label="Cerrar"]/i[@data-visualcompletion="css-img"]')))
boton_X.click()
print('Cerrado X')
sleep(0.5)

# Scrolling para cargar más posts

hacer_scrolling_suavizado(driver,0)
posts = driver.find_elements(By.XPATH, '//div[@aria-describedby and @aria-labelledby]')
print(f"Se encontraron {len(posts)} posts")
for post in posts:
    texto_post = post.find_element(By.XPATH,
                                   '(.//div[@data-ad-comet-preview="message"])[1]').text
    reacciones = post.find_element(By.XPATH, './/span[@class="x1e558r4"]').text

    # Traer los comentarios y compartidas es complicado debido a que comparten mismo XPATH
    # y debido a que podria existir solo uno de los dos, ambos, o ninguno
    n_comentarios = 0
    compartidas = 0
    # Asumimos que ambos existen y los traemos con un solo xpath
    comentarios_y_compartidas = post.find_elements(By.XPATH,
                                                   './/span[@class="x193iq5w xeuugli x13faqbe x1vvkbs xlh3980 xvmahel x1n0sxbx x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x3x7a5m x6prxxf xvq8zen xo1l8bm xi81zsa"]')
    if len(comentarios_y_compartidas) == 2:  # Si este XPATH nos trae dos elementos no hay problema
        n_comentarios = comentarios_y_compartidas[0].text
        compartidas = comentarios_y_compartidas[1].text
    elif len(
            comentarios_y_compartidas) == 0:  # Si este XPATH no nos trae ningun elemento, ambos quedan en 0
        n_comentarios = 0
        compartidas = 0
    else:
        # Caso contrario tenemos que verificar cual de los dos existe, comentarios o compartidas
        # Si el post tiene un texto para ver mas comentarios, sabemos que comentarios debe existir
        texto_comentarios = post.find_elements(By.XPATH,
                                               './/span[text()="Ver más comentarios"]')
        hay_comentarios = len(texto_comentarios) > 0
        if hay_comentarios:
            n_comentarios = comentarios_y_compartidas[0].text
        else:  # Caso contrario las compartidas son las que existen
            compartidas = comentarios_y_compartidas[0].text


    url_post = post.find_element(By.XPATH, './/span[@dir]//div[@id]//a').get_attribute('href')

    print('Texto:')
    print(texto_post)
    print('Reacciones: ', reacciones)
    print('N Comentarios: ', n_comentarios)  # Tambien lo podriamos sacar con len(comentarios)
    print('N compartidas: ', compartidas)
    print('URL: ', url_post)
    print()



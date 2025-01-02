import cloudscraper
import pandas as pd

# Define los encabezados
headers = {
    "referer": "https://www.udemy.com/courses/search/?src=ukw&q=python",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}


# Utilizamos cloudscraper debido al mecanismo anti detección de bots de Udemy
scraper = cloudscraper.create_scraper()

# Este lazo for me ayudara a iterar el parametro "page" del API, HACEMOS 3 ITERACIONES
cursos_totales = []
for i in range (1, 4):
    print(f"Página actual: {i}")
    # Esta URL, y los parametros la deciframos gracias al panel de Networks y a una tarea de investigacio
    url_api = 'https://www.udemy.com/api-2.0/search-courses/?src=ukw&q=python&skip_price=true&p=' + str(i)
    response = scraper.get(url_api, headers=headers)
    print(response)
    # Parseo la respuesta en formato JSON. Requests automaticamente lo convierte en un diccionario de Python
    data = response.json()

    # Extraigo los datos del diccionario
    cursos = data["courses"]
    for curso in cursos:
        #ponemos dentro de un diccionario
        cursos_totales.append({
            "title":  curso["title"],
            "num_reviews": curso["num_reviews"],
            "rating": curso["rating"]
        })
        #imprimimos en pantalla
        #print (curso["title"])
        #print (curso["num_reviews"])
        #print (curso["rating"])
        #print()

df = pd.DataFrame(cursos_totales)
print(df)
df.to_csv('udemy_cursos')
import requests
import pandas as pd
from bs4 import BeautifulSoup

url = "https://es.wikipedia.org/wiki/Provincia_(Espa%C3%B1a)"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)
response.encoding = "utf-8"

soup = BeautifulSoup(response.text, "html.parser")

contenido = soup.find("div", id="mw-content-text")
tablas = contenido.find_all("table")

tabla = tablas[2]  # 3ª tabla, las dos tablas de antes son fotos

capitales = []

for fila in tabla.find_all("tr"):
    columnas = fila.find_all("td")
    if len(columnas) >= 3:
        capitales.append(columnas[2].get_text(strip=True))

df = pd.DataFrame(capitales)

# SIN CABECERA
df.to_csv("../data/capitales.csv", index=False, header=False, encoding="utf-8-sig")


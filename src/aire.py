# -*- coding: utf-8 -*-
"""
Created on Tue Jan 27 18:47:49 2026

@author: Lucía
"""

import requests
import pandas as pd

API_KEY = '233305def63ffc949b51c60e55e6d9a3cc9ef86d'

# Leer ciudades desde CSV SIN cabecera
ruta_csv = "../data/capitales.csv"
ciudades_df = pd.read_csv(ruta_csv, header=None, names=["ciudad"])

datos = []

for _, fila in ciudades_df.iterrows():
    ciudad = fila["ciudad"]

    url = f"https://api.waqi.info/feed/{ciudad}/?token={API_KEY}"
    response = requests.get(url).json()

    if response["status"] == "ok":
        iaqi = response["data"]["iaqi"]

        datos.append({
            "ciudad": ciudad,
            "pm25": iaqi.get("pm25", {}).get("v"),
            "no2": iaqi.get("no2", {}).get("v")
        })

df = pd.DataFrame(datos)

# Guardar resultados
df.to_csv("../data/aire.csv", index=False, encoding="utf-8-sig")

print("✔ Datos de calidad del aire guardados")
print(df)


# -*- coding: utf-8 -*-
"""
Created on Wed Jan 28 13:13:34 2026

@author: Lucía
"""
import unicodedata
import pandas as pd
import numpy as np

df_aire = pd.read_csv("../data/aire.csv", encoding='utf-8-sig')
df_enf= pd.read_csv('../data/77518(1)(in).csv', encoding= 'latin-1', sep=';')
print(df_aire.columns)

df_enf = df_enf.rename(columns={"Provincias": "ciudad"})
print(df_enf.columns)

def quitar_tildes(texto):
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )

def normalizar_provincia(nombre):
    if pd.isna(nombre):
        return nombre
    nombre = nombre.lower().strip()
    nombre = quitar_tildes(nombre)
    nombre = nombre.lstrip("0123456789 ").strip()
    nombre = nombre.replace("/", " ")
    nombre = " ".join(nombre.split())
    return nombre


map_comunidad_a_provincia_oficial = {
    "madrid, comunidad de": "madrid",
    "murcia, region de": "murcia",
    "navarra, comunidad foral de": "navarra",
    "rioja, la": "la rioja",
    "asturias, principado de": "asturias",
    "cantabria": "cantabria",
    "balears, illes": "illes balears",
    
}

#comunidad normalizada
df_enf["comunidad_norm"] = df_enf["Comunidades y Ciudades Autónomas"].apply(normalizar_provincia)

# Si "ciudad" está vacío, rellenamos con la provincia de esa comunidad
df_enf["ciudad"] = np.where(
    (df_enf["ciudad"].isna()) | (df_enf["ciudad"].astype(str).str.strip() == ""),
    df_enf["comunidad_norm"].map(map_comunidad_a_provincia_oficial),
    df_enf["ciudad"])



s = df_enf["Total"].astype(str).str.strip()

# 1) Quitar los puntos de miles: un punto seguido de 3 dígitos
s = s.str.replace(r'\.(?=\d{3}(?:\D|$))', '', regex=True)

# 2) Convertir a número
df_enf["Total"] = pd.to_numeric(s, errors="coerce")




df_aire["ciudad"] = df_aire["ciudad"].apply(normalizar_provincia)
df_enf['ciudad']=df_enf['ciudad'].apply(normalizar_provincia)

diccionario_normalizacion = {
    "coruna": "a coruna",
    'coruna, a': 'a coruna',
    "la coruna": "a coruna",
    "alicante alacant": "alicante",
    "valencia valencia": "valencia",
    "castellon castello": "castellon",
    "illes balears": "palma de mallorca",
    "palmas": "las palmas",
    "bizkaia":"bilbao",
    "navarra":'pamplona',
    "lleida": "lerida",
    'gipuzkoa':'san sebastian',
    'cantabria': 'santander',
    'castilla y leon': 'avila',
    'asturias':'oviedo',
    'ourense':'orense',
    'asturias (principado de)' : 'oviedo',
    'navarra (comun. foral de)' : 'navarra',
    'palmas, las': 'las palmas de gran canaria',
    'madrid (comunidad de)' : 'madrid',
    'murcia (region de)': 'murcia',
    'navarra':'pamplona',
    'girona':'gerona',
    'araba alava':'vitoria',
    'asturias':'oviedo',
    
}

df_aire["ciudad"] = df_aire["ciudad"].replace(diccionario_normalizacion)
df_enf['ciudad']=df_enf['ciudad'].replace(diccionario_normalizacion)

provincias_aire = set(df_aire["ciudad"])
provincias_enf = set(df_enf["ciudad"])

print("Provincias en aire no en enfermedades:", provincias_aire - provincias_enf)
print("Provincias en enfermedades no en aire:", provincias_enf - provincias_aire)


df_final = pd.merge(df_aire, df_enf, on="ciudad", how="inner")
print(df_final.head())
df_final.to_csv("df_final5.csv", index=False, encoding="utf-8-sig")


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import os

# --------------------------------------------------
# 0. CONFIGURAR DESCARGAS (RUTA REAL)
# --------------------------------------------------
download_dir = r"C:\Users\pspau\OneDrive - UPV\UPV\calidad-aire-salud\data"

chrome_prefs = {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
}
# --------------------------------------------------
# 2. INICIAR SELENIUM
# --------------------------------------------------
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_experimental_option("prefs", chrome_prefs)

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 60)

url = "https://ine.es/jaxi/Tabla.htm?tpx=77518&L=0"
driver.get(url)

wait.until(EC.presence_of_element_located((By.ID, "cri0")))
wait.until(EC.presence_of_element_located((By.ID, "contCri1")))

print("✔ Menús desplegables cargados")

# --------------------------------------------------
# 3. SELECCIONAR GRUPO
# --------------------------------------------------
boton_borrar = driver.find_element(
    By.XPATH,
    "//button[@title='Borrar selección']"
)

driver.execute_script("arguments[0].click();", boton_borrar)
time.sleep(1)

# Seleccionar grupo 1000
select_diag = Select(driver.find_element(By.ID, "cri0"))

for option in select_diag.options:
    if "1000 ENFERMEDADES DEL SISTEMA RESPIRATORIO" in option.text:
        option.click()
        print("✔ Grupo 1000 seleccionado")
        break

# Forzar onchange (imprescindible)
driver.execute_script(
    "arguments[0].dispatchEvent(new Event('change'));",
    driver.find_element(By.ID, "cri0")
)

time.sleep(2)

# --------------------------------------------------
# 4. CLICK EN TOTAL NACIONAL Y PROVINCIAS
# --------------------------------------------------
# Provincias
label_provincias = driver.find_element(
    By.XPATH,
    "//div[@id='contCri1']//label[contains(.,'Provincias')]"
)
driver.execute_script("arguments[0].click();", label_provincias)

# Total Nacional (desmarcar si está marcado)
label_total = driver.find_element(
    By.XPATH,
    "//div[@id='contCri1']//label[contains(.,'Total Nacional')]"
)
chk_total = label_total.find_element(By.TAG_NAME, "input")
if chk_total.is_selected():
    driver.execute_script("arguments[0].click();", label_total)

# --------------------------------------------------
# 4.1 SELECCIONAR PROVINCIAS CONCRETAS
# --------------------------------------------------
provincias_ids = [
    "cri1_164",  # Asturias
    "cri1_165",  # Illes Balears
    "cri1_169",  # Cantabria
    "cri1_203",  # Madrid
    "cri1_204",  # Murcia
    "cri1_205",  # Navarra
    "cri1_210"   # La Rioja
]

for prov_id in provincias_ids:
    label = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, f"//label[@for='{prov_id}']")
        )
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", label)
    time.sleep(0.3)
    driver.execute_script("arguments[0].click();", label)
    print(f"✔ Provincia seleccionada: {label.text}")

# --------------------------------------------------
# 5. CONSULTAR SELECCIÓN
# --------------------------------------------------
boton_consultar = wait.until(
    EC.presence_of_element_located((By.ID, "botonConsulSele"))
)
driver.execute_script("arguments[0].click();", boton_consultar)
print("✔ Consulta lanzada")

# --------------------------------------------------
# 11. FORMATOS DE DESCARGA
# --------------------------------------------------
boton_descarga = wait.until(
    EC.presence_of_element_located((By.ID, "btnDescargaForm"))
)
driver.execute_script("arguments[0].click();", boton_descarga)
print("✔ Menú de formatos de descarga abierto")
time.sleep(2)

# --------------------------------------------------
# 12. CSV SEPARADO POR ;
# --------------------------------------------------
csv_punto_coma = wait.until(
    EC.presence_of_element_located(
        (By.XPATH, "//li[contains(text(),'CSV: separado por ;')]")
    )
)
driver.execute_script("arguments[0].click();", csv_punto_coma)
print("✔ CSV descargado en carpeta data")

# --------------------------------------------------
# 13. ESPERAR Y NO CERRAR
# --------------------------------------------------
time.sleep(5)
print("⏸️ Descarga completada. Navegador abierto")
input("Pulsa ENTER para cerrar el navegador...")

driver.quit()


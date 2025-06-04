from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from pymongo import MongoClient
import time

def iniciar_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-notifications")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def mover_mapa(driver):
    mapa = driver.find_element(By.CLASS_NAME, "leaflet-container")
    movimientos = [(200, 0), (-200, 0), (0, 200), (0, -200), (150, 150), (-150, -150)]
    for dx, dy in movimientos:
        driver.execute_script("arguments[0].scrollBy(arguments[1], arguments[2]);", mapa, dx, dy)
        time.sleep(1)

def extraer_tipo_desde_clase(clase_str):
    for parte in clase_str.split():
        if "wm-alert-icon--" in parte:
            return parte.replace("wm-alert-icon--", "").capitalize()
        elif "wazer-" in parte or "wazer" in parte:
            return "Usuario"
    return "Otro"

def scrapear_eventos(driver, coleccion):
    driver.get("https://www.waze.com/es-419/live-map/")
    time.sleep(10)

    eventos = []
    claves_vistas = set()
    mover_mapa(driver)

    try:
        markers = driver.find_elements(By.CLASS_NAME, "leaflet-marker-icon")
        print(f"[+] Total marcadores detectados: {len(markers)}")

        tipos_detectados = {}

        for marker in markers:
            try:
                clase = marker.get_attribute("class")
                tipo = extraer_tipo_desde_clase(clase)
                posicion = marker.location
                clave = f"{tipo}-{posicion}"

                if clave in claves_vistas:
                    continue
                claves_vistas.add(clave)

                # Si es usuario, no hacer click
                if tipo == "Usuario":
                    descripcion = "Usuario en el mapa"
                    direccion = "Desconocida"
                else:
                    try:
                        marker.click()
                        time.sleep(1.5)

                        titulo = WebDriverWait(driver, 3).until(
                            EC.presence_of_element_located((By.CLASS_NAME, "wm-alert-details__title"))
                        ).text.strip()

                        direccion = driver.find_element(By.CLASS_NAME, "wm-alert-details__address").text.strip()
                        descripcion = f"{titulo} - {direccion}"
                    except Exception as e:
                        print(f"[!] No se pudo abrir detalle de marcador ({tipo}): {e}")
                        continue

                tipos_detectados[tipo] = tipos_detectados.get(tipo, 0) + 1

                evento = {
                    "tipo": tipo,
                    "direccion": direccion,
                    "descripcion": descripcion,
                    "posicion": posicion,
                    "clase": clase
                }
                eventos.append(evento)

            except Exception as e:
                print(f"[!] Error con un marcador general: {e}")
                continue

    except Exception as e:
        print(f"[!] Error al recolectar íconos: {e}")

    if eventos:
        coleccion.insert_many(eventos)
        print(f"[✓] Insertados {len(eventos)} eventos.")
    else:
        print("[!] No se insertaron eventos nuevos.")

    print("\n📊 Tipos recolectados:")
    for tipo, cant in tipos_detectados.items():
        print(f" - {tipo}: {cant}")

def main():
    cliente = MongoClient("mongodb://localhost:27017/")
    db = cliente["trafico_rm"]
    coleccion = db["eventos"]

    driver = iniciar_driver()

    try:
        while True:
            scrapear_eventos(driver, coleccion)
            print("Esperando 15 segundos antes del siguiente ciclo...\n")
            time.sleep(15)
    except KeyboardInterrupt:
        print("Scraping detenido.")
        driver.quit()

if __name__ == "__main__":
    main()

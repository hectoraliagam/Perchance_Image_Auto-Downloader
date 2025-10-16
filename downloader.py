import os
import time
import base64
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException

def connect_to_chrome():
    options = Options()
    options.debugger_address = "127.0.0.1:9222"
    driver = webdriver.Chrome(options=options)
    print("✅ Conectado correctamente a Chrome.")
    return driver

def get_outer_iframe(driver):
    try:
        return driver.find_element(By.XPATH, '//*[@id="outputIframeEl"]')
    except NoSuchElementException:
        print("⚠️ No se encontró el iframe externo (outputIframeEl).")
        return None

def click_generate_button(driver):
    outer_iframe = get_outer_iframe(driver)
    if not outer_iframe:
        print("⚠️ No se pudo acceder al iframe principal. No se pulsará el botón.")
        return
    try:
        driver.switch_to.frame(outer_iframe)
        generate_button = driver.find_element(By.XPATH, '//*[@id="generateButtonEl"]')
        driver.execute_script("arguments[0].scrollIntoView(true);", generate_button)
        time.sleep(0.5)
        generate_button.click()
        print("🚀 Botón 'Generate' pulsado correctamente.")
    except (NoSuchElementException, ElementClickInterceptedException) as e:
        print(f"⚠️ No se pudo pulsar el botón 'Generate': {e}")
    finally:
        driver.switch_to.default_content()

def detect_new_images(driver, known_urls):
    new_imgs = []
    outer_iframe = get_outer_iframe(driver)
    if not outer_iframe:
        return []
    try:
        driver.switch_to.frame(outer_iframe)
        containers = driver.find_elements(By.XPATH, '//*[@id="outputAreaEl"]/div')
        print(f"📦 Detectados {len(containers)-1} contenedores de imágenes válidos.")
        for div in containers:
            try:
                inner_iframe = div.find_element(By.TAG_NAME, "iframe")
                if not inner_iframe.is_displayed():
                    continue
                driver.switch_to.frame(inner_iframe)
                img = driver.find_element(By.ID, "resultImgEl")
                img_src = img.get_attribute("src")
                if img_src and img_src not in known_urls:
                    new_imgs.append(img_src)
            except Exception:
                pass
            finally:
                driver.switch_to.parent_frame()
    except Exception as e:
        print(f"⚠️ Error general al detectar imágenes: {e}")
    finally:
        driver.switch_to.default_content()
    return new_imgs

def download_images(driver, save_path, max_images=32, poll_interval=2):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    downloaded = set()
    print("🖼️ Iniciando la generación y descarga de imágenes...")
    click_generate_button(driver)
    print("🖼️ Esperando imágenes generadas dinámicamente...")
    while len(downloaded) < max_images:
        new_imgs = detect_new_images(driver, downloaded)
        if new_imgs:
            for img_src in new_imgs:
                downloaded.add(img_src)
                filename = os.path.join(save_path, f"{len(downloaded):02}.jpeg")
                try:
                    if img_src.startswith("data:image/jpeg;base64,"):
                        img_data = base64.b64decode(img_src.split(",")[1])
                        with open(filename, "wb") as f:
                            f.write(img_data)
                        print(f"✅ Imagen {len(downloaded):02} descargada correctamente.")
                    else:
                        print(f"⚠️ Fuente no reconocida: {img_src[:60]}...")
                except Exception as e:
                    print(f"❌ Error al guardar imagen {len(downloaded):02}: {e}")
                if len(downloaded) >= max_images:
                    break
        else:
            print("⏳ Aún no hay nuevas imágenes, esperando...")
        time.sleep(poll_interval)
    print("\n🎉 Descarga completada con éxito.")

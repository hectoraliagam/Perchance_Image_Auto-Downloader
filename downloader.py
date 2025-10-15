import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def connect_to_chrome():
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(options=chrome_options)
    print("\n✅ Conectado a la sesión abierta de Chrome.")
    print("🌐 URL actual:", driver.current_url)
    print("🧭 Título actual:", driver.title)
    return driver


def get_generator_iframe(driver):
    """
    Encuentra automáticamente el iframe donde se ejecuta el generador de imágenes.
    """
    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    print(f"🔎 Detectando iframes en la página ({len(iframes)} encontrados)...")

    image_sources = driver.execute_script("""
        const app = document.querySelector('perchance-app');
        if (!app) return [];
        const root = app.shadowRoot;
        if (!root) return [];
        const generator = root.querySelector('perchance-ai-text-to-image-generator');
        if (!generator) return [];
        const shadow = generator.shadowRoot;
        if (!shadow) return [];
        const imgs = shadow.querySelectorAll('img');
        return Array.from(imgs).map(img => img.src);
    """)

    if image_sources and len(image_sources) > 0:
        print(f"🖼️ Se encontraron {len(image_sources)} imágenes para descargar.")
        for i, src in enumerate(image_sources, start=1):
            print(f"   {i:02d} → {src}")
    else:
        print("⚠️ No se encontraron imágenes dentro del shadow root del generador.")

    for idx, iframe in enumerate(iframes):
        src = iframe.get_attribute("src")
        if src and "perchance.org/ai-text-to-image-generator" in src:
            print(f"✅ Iframe correcto detectado: #{idx} ({src})")
            return iframe

    print("❌ No se encontró el iframe del generador. Asegúrate de estar en la página correcta.")
    return None


def click_generate_if_needed(driver):
    print("\n🔍 Verificando si hay imágenes generadas...")

    target_iframe = get_generator_iframe(driver)
    if not target_iframe:
        return

    try:
        driver.switch_to.frame(target_iframe)
        print("✅ Cambiado al iframe del generador.")

        images = driver.find_elements(By.XPATH, '//*[@id="resultImgEl"]')

        if len(images) == 0:
            print("⚠️ No hay imágenes visibles. Intentando presionar el botón 'Generar'...")

            wait = WebDriverWait(driver, 15)
            generate_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="generateButtonEl"]'))
            )

            driver.execute_script("arguments[0].scrollIntoView(true);", generate_button)
            time.sleep(0.8)
            generate_button.click()
            print("✅ Botón 'Generar' presionado correctamente.")

            print("⏳ Esperando a que se generen las imágenes...")
            WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="resultImgEl"]'))
            )
            print("🖼️ Imágenes generadas correctamente.")

        else:
            print(f"🖼️ Ya hay {len(images)} imágenes visibles en la página.")

    except Exception as e:
        print(f"❌ Error al intentar generar imágenes: {e}")

    finally:
        driver.switch_to.default_content()


def download_images_from_page(driver, save_path, num_images=32):
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    click_generate_if_needed(driver)

    print("\n🔍 Buscando imágenes dentro del iframe...")
    target_iframe = get_generator_iframe(driver)
    if not target_iframe:
        print("❌ No se puede descargar porque no se detectó el iframe.")
        return

    driver.switch_to.frame(target_iframe)
    time.sleep(2)

    images = driver.find_elements(By.XPATH, '/html/body/div[1]/main/div[2]/img')
    print(f"🖼️ Se encontraron {len(images)} imágenes para descargar.")

    if not images:
        print("⚠️ No se encontraron imágenes para descargar.")
        driver.switch_to.default_content()
        return

    for idx, img in enumerate(images[:num_images], start=1):
        src = img.get_attribute("src")
        if src:
            filename = os.path.join(save_path, f"{idx:02}.jpeg")
            try:
                r = requests.get(src, timeout=15)
                with open(filename, "wb") as f:
                    f.write(r.content)
                print(f"✅ Imagen {idx:02} descargada correctamente.")
            except Exception as e:
                print(f"❌ Error al descargar imagen {idx:02}: {e}")
        else:
            print(f"⚠️ Imagen {idx:02} no tiene atributo 'src'.")

    driver.switch_to.default_content()
    print("\n🎉 Descarga completada con éxito.")

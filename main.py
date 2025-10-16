import os
from downloader import connect_to_chrome, download_images

BASE_PATH = r"C:\\Users\\Hector\\Documents\\The Fearless Storyteller\\images"
SUBCARPETAS_TOTALES = 16
IMAGENES_POR_SUBCARPETA = 32

def listar_carpetas_y_archivos(path):
    print("\n📂 Carpetas existentes dentro de la madre:")
    carpetas = sorted(os.listdir(path))
    if not carpetas:
        print("\n   (Vacío)")
        return
    for carpeta in carpetas:
        carpeta_path = os.path.join(path, carpeta)
        if os.path.isdir(carpeta_path):
            imagenes = [
                img for img in sorted(os.listdir(carpeta_path))
                if img.lower().endswith(('.jpg', '.png', '.jpeg', '.webp'))
            ]
            if imagenes:
                print(f"\n N° {carpeta} ({len(imagenes)} imágenes)")
            else:
                print(f"\n N° {carpeta} (vacía)")

def obtener_ultima_carpeta_madre():
    carpetas = [c for c in os.listdir(BASE_PATH) if c.isdigit()]
    if not carpetas:
        return None
    return f"{max(int(c) for c in carpetas):04d}"

def obtener_siguiente_madre(actual):
    return f"{int(actual) + 1:04d}"

def obtener_subcarpetas_completas(path):
    completas = 0
    for carpeta in sorted(os.listdir(path)):
        carpeta_path = os.path.join(path, carpeta)
        if os.path.isdir(carpeta_path):
            imagenes = [
                img for img in os.listdir(carpeta_path)
                if img.lower().endswith(('.jpg', '.png', '.jpeg', '.webp'))
            ]
            if len(imagenes) >= IMAGENES_POR_SUBCARPETA:
                completas += 1
    return completas

def obtener_siguiente_hija(path):
    carpetas = sorted([c for c in os.listdir(path) if c.isdigit()])
    for carpeta in carpetas:
        carpeta_path = os.path.join(path, carpeta)
        if os.path.isdir(carpeta_path):
            imagenes = [
                img for img in os.listdir(carpeta_path)
                if img.lower().endswith(('.jpg', '.png', '.jpeg', '.webp'))
            ]
            if len(imagenes) < IMAGENES_POR_SUBCARPETA:
                return carpeta
    siguiente = len(carpetas) + 1
    return f"{siguiente:02d}"

def main():
    print("🔄 Buscando carpeta madre activa...")
    ultima_madre = obtener_ultima_carpeta_madre()
    if ultima_madre:
        ruta_madre = os.path.join(BASE_PATH, ultima_madre)
        subcarpetas_completas = obtener_subcarpetas_completas(ruta_madre)
        if subcarpetas_completas >= SUBCARPETAS_TOTALES:
            carpeta_madre = obtener_siguiente_madre(ultima_madre)
            ruta_madre = os.path.join(BASE_PATH, carpeta_madre)
            os.makedirs(ruta_madre, exist_ok=True)
            print(f"\n🆕 Nueva carpeta madre creada automáticamente: {carpeta_madre}")
        else:
            carpeta_madre = ultima_madre
            print(f"\n📁 Continuando con la carpeta madre existente: {carpeta_madre}")
    else:
        carpeta_madre = "0001"
        ruta_madre = os.path.join(BASE_PATH, carpeta_madre)
        os.makedirs(ruta_madre, exist_ok=True)
        print(f"\n🆕 Creada carpeta madre inicial: {carpeta_madre}")
    listar_carpetas_y_archivos(ruta_madre)
    while True:
        subcarpetas_completas = obtener_subcarpetas_completas(ruta_madre)
        if subcarpetas_completas >= SUBCARPETAS_TOTALES:
            print(f"\n🎯 Carpeta madre {carpeta_madre} completada (16 subcarpetas llenas).")
            break
        siguiente_hija = obtener_siguiente_hija(ruta_madre)
        ruta_hija = os.path.join(ruta_madre, siguiente_hija)
        os.makedirs(ruta_hija, exist_ok=True)
        print(f"\n🆕 Preparando subcarpeta hija {siguiente_hija}...")
        print(f"📍 Ruta final: {ruta_hija}")
        print("\nConectando a Chrome abierto...")
        driver = connect_to_chrome()
        if driver:
            download_images(driver, ruta_hija, max_images=IMAGENES_POR_SUBCARPETA)
            print(f"✅ Subcarpeta {siguiente_hija} completada correctamente.")
        else:
            print("❌ No se pudo conectar a Chrome. Abortando ciclo.")
            break
    print("\n🏁 Proceso de generación terminado por completo.")

if __name__ == "__main__":
    main()

import playwright.sync_api

URL_MERCADO_LIBRE = "https://www.mercadolibre.com/"
SELECTOR_BUSCAR = "input[placeholder='Buscar productos, marcas y más']"

def buscar_productos(page):
    # Buscar productos
    page.get_by_placeholder("Buscar productos, marcas y más").fill("playstation5")
    page.get_by_role("button", name="Buscar").click()

def aplicar_filtros(page):
    # Aplicar filtros de búsqueda
    page.get_by_label("Nuevo, 132 resultados").click()
    page.get_by_label("Distrito Federal, 58").click()

def extraer_informacion_productos(page):
    # Extraer información de los productos
    productos = []
    for i in range(5):
        nombre_elemento = page.query_selector(f"xpath=(//*[contains(concat(' ', @class, ' '), concat(' ', 'poly-component__title', ' '))])[{i+1}]")
        precio_elemento = page.query_selector(f"xpath=(//*[contains(concat(' ', @class, ' '), concat(' ', 'poly-component__price', ' '))])[{i+1}]")

        # Verificar si los elementos fueron encontrados
        if nombre_elemento and precio_elemento:
            nombre = nombre_elemento.text_content()
            precio = precio_elemento.text_content()
            productos.append({"nombre": nombre, "precio": precio})
    return productos

def imprimir_resultados(productos):
    # Imprimir resultados
    for producto in productos:
        print(f"Nombre: {producto['nombre']}, Precio: {producto['precio']}")

def main():
    with playwright.sync_api.sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(URL_MERCADO_LIBRE)
        page.get_by_role("link", name="México").click()
        
        buscar_productos(page)
        
        # Esperar a que la página cargue los resultados
        page.wait_for_timeout(2000)  # Ajusta el tiempo según sea necesario
        
        # Aplicar filtros
        aplicar_filtros(page)
        
        # Esperar a que se apliquen los filtros y se actualicen los resultados
        page.wait_for_timeout(2000)  # Ajusta el tiempo según sea necesario
        
        productos = extraer_informacion_productos(page)
        imprimir_resultados(productos)
        
        page.wait_for_timeout(10000)
        browser.close()

if __name__ == '__main__':
    main()
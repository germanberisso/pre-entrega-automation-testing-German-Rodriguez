import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def test_verificar_catalogo(login_in_driver):
    """Verifica que el catálogo de productos se muestre correctamente tras el login."""
    
    driver = login_in_driver  # driver ya logueado

    # Espera explícita para el título
    titulo = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "title"))
    ).text
    assert titulo == "Products", f"Se esperaba 'Products', pero se encontró '{titulo}'"

    # Verificar productos visibles
    productos = driver.find_elements(By.CLASS_NAME, "inventory_item")
    assert len(productos) > 0, "No se encontraron productos visibles."

    # Validar elementos importantes
    menu_boton = driver.find_element(By.ID, "react-burger-menu-btn")
    filtro = driver.find_element(By.CLASS_NAME, "product_sort_container")

    assert menu_boton.is_displayed(), "Botón de menú no visible."
    assert filtro.is_displayed(), "Selector de filtro no visible."

    # Mostrar primer producto
    primer_producto = productos[0]
    nombre = primer_producto.find_element(By.CLASS_NAME, "inventory_item_name").text
    precio = primer_producto.find_element(By.CLASS_NAME, "inventory_item_price").text
    print(f"Primer producto: {nombre} - Precio: {precio}")

    # Screenshot
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    driver.save_screenshot(f"reports/catalogo_ok_{timestamp}.png")
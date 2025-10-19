import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from utils.helpers import login

@pytest.fixture
def driver():
    """Inicializa y cierra el navegador para cada test."""
    from selenium import webdriver
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

def test_verificar_catalogo(driver):
    """Verifica que el catálogo de productos se muestre correctamente tras el login."""
    
    # Login reutilizando helper
    login(driver)

    # Espera explícita para el título de la página
    titulo = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "title"))
    ).text
    assert titulo == "Products", f"Se esperaba el título 'Products', pero se encontró '{titulo}'"

    # Verificar que haya productos visibles
    productos = driver.find_elements(By.CLASS_NAME, "inventory_item")
    assert len(productos) > 0, "No se encontraron productos visibles en la página de inventario."

    # Validar elementos importantes de la interfaz
    menu_boton = driver.find_element(By.ID, "react-burger-menu-btn")
    filtro = driver.find_element(By.CLASS_NAME, "product_sort_container")

    assert menu_boton.is_displayed(), "El botón del menú lateral no está visible."
    assert filtro.is_displayed(), "El selector de filtro no está visible."

    # Mostrar nombre y precio del primer producto como validación adicional
    primer_producto = productos[0]
    nombre = primer_producto.find_element(By.CLASS_NAME, "inventory_item_name").text
    precio = primer_producto.find_element(By.CLASS_NAME, "inventory_item_price").text
    print(f"Primer producto: {nombre} - Precio: {precio}")

    # Evidencia (screenshot)
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    driver.save_screenshot(f"reports/catalogo_ok_{timestamp}.png")
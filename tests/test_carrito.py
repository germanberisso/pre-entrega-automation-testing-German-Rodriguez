import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.helpers import login

@pytest.fixture
def driver():
    """Inicializa y cierra el navegador para cada test."""
    from selenium import webdriver
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

def test_agregar_producto_al_carrito(driver):
    """Verifica que se pueda agregar un producto al carrito y que aparezca correctamente."""
    
    # Login reutilizando helper
    login(driver)

    # Esperar a que cargue la lista de productos
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "inventory_item"))
    )

    # Seleccionar el primer producto y hacer clic en "Add to cart"
    primer_boton = driver.find_element(By.CSS_SELECTOR, ".inventory_item button.btn_inventory")
    primer_boton.click()

    # Verificar que el ícono del carrito muestre el número "1"
    carrito_icono = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "shopping_cart_badge"))
    )
    assert carrito_icono.text == "1", f"El contador del carrito debería ser '1', pero se encontró '{carrito_icono.text}'"

    # Ir al carrito
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()

    # Esperar a que se cargue la página del carrito
    WebDriverWait(driver, 10).until(EC.url_contains("/cart.html"))

    # Verificar que el producto esté presente en el carrito
    producto_en_carrito = driver.find_elements(By.CLASS_NAME, "cart_item")
    assert len(producto_en_carrito) > 0, "El carrito está vacío, no se agregó ningún producto."

    # Mostrar nombre del producto agregado (para debug/log)
    nombre_producto = producto_en_carrito[0].find_element(By.CLASS_NAME, "inventory_item_name").text
    print(f"Producto en el carrito: {nombre_producto}")

    # Evidencia (screenshot)
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    driver.save_screenshot(f"reports/carrito_ok_{timestamp}.png")
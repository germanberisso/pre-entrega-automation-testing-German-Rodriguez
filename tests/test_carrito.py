import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def test_agregar_producto_al_carrito(login_in_driver):
    """Verifica que se pueda agregar un producto al carrito y que aparezca correctamente."""
    
    driver = login_in_driver  # driver ya logueado

    # Esperar a que carguen productos
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "inventory_item"))
    )

    # Seleccionar primer producto y click en "Add to cart"
    primer_boton = driver.find_element(By.CSS_SELECTOR, ".inventory_item button.btn_inventory")
    primer_boton.click()

    # Verificar ícono carrito
    carrito_icono = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "shopping_cart_badge"))
    )
    assert carrito_icono.text == "1", f"Contador carrito debería ser '1', pero se encontró '{carrito_icono.text}'"

    # Ir al carrito
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    WebDriverWait(driver, 10).until(EC.url_contains("/cart.html"))

    # Verificar producto en carrito
    producto_en_carrito = driver.find_elements(By.CLASS_NAME, "cart_item")
    assert len(producto_en_carrito) > 0, "Carrito vacío, no se agregó producto."

    # Mostrar nombre
    nombre_producto = producto_en_carrito[0].find_element(By.CLASS_NAME, "inventory_item_name").text
    print(f"Producto en el carrito: {nombre_producto}")

    # Screenshot
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    driver.save_screenshot(f"reports/carrito_ok_{timestamp}.png")
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from utils.helpers import login

def test_login_exitoso(driver):
    """Verifica que un usuario válido pueda iniciar sesión correctamente en saucedemo.com."""
    
    driver.get("https://www.saucedemo.com")
    
    # Espera explícita para campo de usuario
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "user-name"))
    )
    
    # Login usando helper
    login(driver)

    # Validar redirección a /inventory.html
    WebDriverWait(driver, 10).until(EC.url_contains("/inventory.html"))
    assert "/inventory.html" in driver.current_url, "No se redirigió correctamente a la página de inventario."
    
    # Validar título
    titulo = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "title"))
    ).text
    assert titulo == "Products", f"Se esperaba 'Products', se encontró '{titulo}'"
    
    # Screenshot
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    driver.save_screenshot(f"reports/login_exitoso_{timestamp}.png")
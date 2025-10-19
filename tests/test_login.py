import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from utils.helpers import login

@pytest.fixture
def driver():
    """Fixture para inicializar y cerrar el navegador."""
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

def test_login_exitoso(driver):
    """Verifica que un usuario válido pueda iniciar sesión correctamente en saucedemo.com."""
    driver.get("https://www.saucedemo.com")

    # Espera explícita para campo de usuario
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "user-name"))
    )

    # Ingresar credenciales válidas
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    # Validar redirección a /inventory.html
    WebDriverWait(driver, 10).until(EC.url_contains("/inventory.html"))
    assert "/inventory.html" in driver.current_url, "No se redirigió correctamente a la página de inventario."

    # Validar que el título sea "Products"
    titulo = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "title"))
    ).text
    assert titulo == "Products", f"El título esperado era 'Products', pero se encontró '{titulo}'"

    # Evidencia opcional (screenshot)
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    driver.save_screenshot(f"reports/login_exitoso_{timestamp}.png")

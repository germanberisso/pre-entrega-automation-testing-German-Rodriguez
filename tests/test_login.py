from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_login_exitoso():
    # Inicializar ChromeDriver
    driver = webdriver.Chrome()  # Asegurate que ChromeDriver esté en PATH o en drivers/
    driver.maximize_window()
    
    try:
        # Navegar a la página de login
        driver.get("https://www.saucedemo.com")

        # Espera explícita para el campo de usuario
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "user-name"))
        )

        # Ingresar credenciales
        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()

        # Validar que se redirige a /inventory.html
        WebDriverWait(driver, 10).until(
            EC.url_contains("/inventory.html")
        )

        # Validar que el título de la página sea "Products"
        titulo = driver.find_element(By.CLASS_NAME, "title").text
        assert titulo == "Products", f"El título esperado era 'Products', pero se encontró '{titulo}'"

    finally:
        driver.quit()
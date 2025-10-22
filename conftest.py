import pytest
from selenium import webdriver
from utils.helpers import login

@pytest.fixture
def driver():
    """Inicializa y cierra el navegador para cada test."""
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.fixture
def login_in_driver(driver):
    """Realizar login antes de cada test que lo requiera."""
    login(driver)  # ejecuta el helper que hace login
    return driver
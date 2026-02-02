import datetime
import os

import pytest
import pyodbc
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
from pathlib import Path

#Cargar las variable de entorno al iniciar
load_dotenv()


def pytest_addoption(parser):
    parser.addoption("--url", action="store", default="https://qa-env.nyl.com", help="URL del ambiente a testear")


@pytest.fixture(scope="session")
def base_url(request):
    return request.config.getoption("--url")


# Modifica tu fixture de driver para que use la URL
@pytest.fixture(scope="function")
def driver(base_url):
    print(f"\n--- Iniciando WebDriver en: {base_url} ---")
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # El driver navega automáticamente antes de entregar el control al test
    driver.get(base_url)

    yield driver

    print("\n--- Cerrando WebDriver ---")
    driver.quit()


# FIXTURE: Configuración del Navegador
# @pytest.fixture(scope="function")
# def driver():
#     print("\n--- Iniciando WebDriver ---")
#     options = webdriver.ChromeOptions()
#     options.add_argument("--start-maximized")
#     # options.add_argument("--headless") # Descomentar para CI/CD
#
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
#
#     yield driver  # Aquí es donde el test se ejecuta
#
#     print("\n--- Cerrando WebDriver ---")
#     driver.quit()


# FIXTURE: Conexión a SQL Server (Data Integrity)
@pytest.fixture(scope="session")
def db_connection():
    print("\n--- Estableciendo conexión a SQL Server ---")
    conn_str = (
        "Driver={SQL Server};"
        "Server=TU_SERVIDOR;"
        "Database=TU_DB;"
        "Trusted_Connection=yes;"
    )
    conn = pyodbc.connect(conn_str)

    yield conn

    print("\n--- Cerrando conexión DB ---")
    conn.close()


# HOOK: Captura de pantalla automática en fallo para Allure
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook para interceptar el resultado de cada fase del test (setup, call, teardown).
    """
    outcome = yield
    rep = outcome.get_result()

    # Solo actuamos si el test falla durante la ejecución ('call')
    if rep.when == "call" and rep.failed:
        mode = "a" if os.path.exists("failures.txt") else "w"
        try:
            # Buscamos la fixture 'driver' en el test actual
            if "driver" in item.funcargs:
                web_driver = item.funcargs["driver"]

                # Crear carpeta de capturas si no existe
                output_dir = Path("screenshots")
                output_dir.mkdir(exist_ok=True)

                # Nombre de archivo: test_nombre_20240101_1200.png
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                file_name = f"{item.name}_{timestamp}.png"
                file_path = output_dir / file_name

                web_driver.save_screenshot(str(file_path))
                print(f"\n[ERROR] Captura de pantalla guardada en: {file_path}")

        except Exception as e:
            print(f"\n[ADVERTENCIA] No se pudo tomar la captura: {e}")
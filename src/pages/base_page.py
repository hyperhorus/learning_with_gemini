import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self._wait = WebDriverWait(self.driver, 10)  # Timeout estándar de 10s
        self.url = driver.current_url

    @allure.step("Buscando elemento {locator}")
    def find_element(self, locator):
        """Wrapper robusto con espera explícita."""
        try:
            return self._wait.until(EC.presence_of_element_located(locator))
        except TimeoutException:
            print(f"\n[ERROR] Elemento no encontrado en el tiempo previsto: {locator}")
            raise

    @allure.step("Hacer click el elemento {locator}")
    def click(self, locator):
        """Espera a que sea clicable y ejecuta."""
        element = self._wait.until(EC.element_to_be_clickable(locator))
        element.click()

    @allure.step("Escribir '{texto}' en {locator}")
    def write(self, locator, text):
        """Limpia el campo antes de escribir (Buenas prácticas)."""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    @allure.step("Obtener texto de {locator}")
    def get_text(self, locator):
        """Extrae texto para aserciones de validación."""
        return self.find_element(locator).text

    @allure.step("Verificar que {locator} sea visible")
    def is_visible(self, locator):
        """Retorna Booleano, ideal para validaciones rápidas."""
        try:
            return self._wait.until(EC.visibility_of_element_located(locator)).is_displayed()
        except:
            return False

    @allure.step("Entrar al iframe {iframe_locator}")
    def switch_to_iframe(self, iframe_locator):
        """Espera y cambia el contexto al iframe."""
        self._wait.until(EC.frame_to_be_available_and_switch_to_it(iframe_locator))

    @allure.step("Salir del iframe")
    def switch_to_default_content(self):
        """Vuelve a la página principal (Fuera del iframe)."""
        self.driver.switch_to.default_content()

    @allure.step("Cambiar a la nueva ventana")
    def switch_to_new_window(self):
        """Cambia el foco a la última pestaña/ventana abierta."""
        self._wait.until(lambda d: len(d.window_handles) > 1)
        self.driver.switch_to.window(self.driver.window_handles[-1])

    @allure.step("Cerrar la ventana y volver a la primera       ")
    def close_current_and_return(self):
        """Cierra la ventana actual y vuelve a la primera."""
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
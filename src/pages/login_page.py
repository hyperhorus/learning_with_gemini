from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from pages.base_page import BasePage

class LoginPage(BasePage):
    # LOCALIZADORES (Encapsulados para fácil mantenimiento)
    # Usamos Selectores CSS por ser más rápidos que XPath en navegadores modernos
    SIGNIN_INPUT = (By.XPATH, "//span[normalize-space()='Sign in']")
    USER_INPUT = (By.CSS_SELECTOR, "input[name='username']")
    PASS_INPUT = (By.CSS_SELECTOR, "input[name='password']")
    LOGIN_BTN  = (By.ID, "login-button")
    ERROR_MSG  = (By.CLASS_NAME, "error-message-container")

    def __init__(self, driver):
        super().__init__(driver)
        self.base_url = driver.current_url
        self.wait = WebDriverWait(driver, 10)

    def login_to_application(self, username, password):
        """Flujo completo de login encapsulado."""
        self.click(self.SIGNIN_INPUT)
        self.write(self.USER_INPUT, username)
        self.write(self.PASS_INPUT, password)
        self.click(self.LOGIN_BTN)

    def get_error_message(self):
        """Captura errores de credenciales inválidas."""
        return self.get_text(self.ERROR_MSG)
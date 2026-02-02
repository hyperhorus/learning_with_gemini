import pytest
from src.pages.login_page import LoginPage

@pytest.mark.regression
def test_login_and_db_audit(driver, db_connection):
    # 1. Inicializar la página
    login_pg = LoginPage(driver)
    #driver.get("https://tu-app-corporativa.com/login")
    #driver.current_url()

    # 2. Ejecutar Acción en UI
    # user_test = "gllano_senior"
    # login_pg.login_to_application(user_test, "Password123!")

    # 3. Validación de Negocio (UI)
    # assert "Dashboard" in driver.title, "El login falló o no redirigió correctamente"

    # 4. VALIDACIÓN HÍBRIDA (Data Integrity en SQL Server)
    # Consultamos si se registró el log de auditoría para este usuario hoy
    # cursor = db_connection.cursor()
    # query = f"SELECT TOP 1 LastLogin FROM UsersAudit WHERE UserName = '{user_test}' ORDER BY LastLogin DESC"
    #
    # cursor.execute(query)
    # row = cursor.fetchone()
    #
    # assert row is not None, f"No se encontró registro de auditoría en DB para {user_test}"
    # print(f"Validación Exitosa. Último acceso en DB: {row[0]}")
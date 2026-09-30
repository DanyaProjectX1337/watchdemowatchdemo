from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_saucedemo_purchase_with_waits(browser, base_url):
    """Тест полного цикла покупки с использованием явных ожиданий."""
    wait = WebDriverWait(browser, timeout=10)

    # Открытие страницы
    browser.get(base_url)

    # =========================================================================
    # 1. Явные ожидания для страницы авторизации
    # =========================================================================
    user_name_input = wait.until(
        EC.visibility_of_element_located((By.ID, "user-name")),
        message="Поле ввода логина не отобразилось на странице авторизации",
    )
    password_input = wait.until(
        EC.visibility_of_element_located((By.ID, "password")),
        message="Поле ввода пароля не отобразилось на странице авторизации",
    )
    login_btn = wait.until(
        EC.element_to_be_clickable((By.ID, "login-button")),
        message="Кнопка 'Login' не стала кликабельной",
    )

    user_name_input.send_keys("standard_user")
    password_input.send_keys("secret_sauce")
    login_btn.click()

    # =========================================================================
    # 2. Явные ожидания для страницы с товарами
    # =========================================================================
    wait.until(
        EC.visibility_of_element_located((By.CLASS_NAME, "inventory_list")),
        message="Список товаров (каталог) не отобразился",
    )
    add_to_cart_btn = wait.until(
        EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack")),
        message="Кнопка добавления товара в корзину недоступна для нажатия",
    )
    add_to_cart_btn.click()

    cart_link = wait.until(
        EC.element_to_be_clickable((By.CLASS_NAME, "shopping_cart_link")),
        message="Иконка перехода в корзину не кликабельна",
    )
    cart_link.click()

    checkout_btn = wait.until(
        EC.element_to_be_clickable((By.ID, "checkout")),
        message="Кнопка 'Checkout' в корзине не кликабельна",
    )
    checkout_btn.click()

    # =========================================================================
    # 3. Явные ожидания для страницы с оформлением (ввод данных)
    # =========================================================================
    first_name = wait.until(
        EC.visibility_of_element_located((By.ID, "first-name")),
        message="Поле ввода имени покупателя не появилось",
    )
    last_name = wait.until(
        EC.visibility_of_element_located((By.ID, "last-name")),
        message="Поле ввода фамилии покупателя не появилось",
    )
    postal_code = wait.until(
        EC.visibility_of_element_located((By.ID, "postal-code")),
        message="Поле ввода индекса не появилось",
    )
    continue_btn = wait.until(
        EC.element_to_be_clickable((By.ID, "continue")),
        message="Кнопка 'Continue' не кликабельна",
    )

    first_name.send_keys("Иван")
    last_name.send_keys("Петров")
    postal_code.send_keys("101000")
    continue_btn.click()

    # =========================================================================
    # 4. Явное ожидание для страницы с оплатой товара (Overview)
    # =========================================================================
    wait.until(
        EC.visibility_of_element_located((By.CLASS_NAME, "summary_info")),
        message="Блок с деталями оплаты и доставки (summary_info) не отобразился",
    )
    finish_btn = wait.until(
        EC.element_to_be_clickable((By.ID, "finish")),
        message="Кнопка 'Finish' для подтверждения оплаты недоступна для нажатия",
    )
    finish_btn.click()

    # =========================================================================
    # 5. Явное ожидание для текста об успешной покупке
    # =========================================================================
    complete_header = wait.until(
        EC.visibility_of_element_located((By.CLASS_NAME, "complete-header")),
        message="Сообщение о завершении заказа не появилось на странице",
    )

    expected_text = "Thank you for your order!"
    assert complete_header.text == expected_text, (
        f"Ожидался текст: '{expected_text}', фактически получен: '{complete_header.text}'"
    )
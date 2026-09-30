import pytest
from selenium import webdriver


def pytest_addoption(parser):
    """Регистрация параметров запуска тестов."""
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Браузер для тестов: chrome, firefox, edge",
    )
    parser.addoption(
        "--url",
        action="store",
        default="https://www.saucedemo.com/",
        help="Базовый адрес тестируемого веб-сайта",
    )


@pytest.fixture(scope="session")
def base_url(request):
    """Фикстура получения базового адреса."""
    return request.config.getoption("--url")


@pytest.fixture
def browser(request):
    """
    Фикстура инициализации браузера.
    Критерий: Реализовано неявное ожидание с нулём в фикстуре с браузером.
    """
    browser_name = request.config.getoption("--browser").lower()
    driver = None

    if browser_name == "chrome":
        driver = webdriver.Chrome()
    elif browser_name == "firefox":
        driver = webdriver.Firefox()
    elif browser_name == "edge":
        driver = webdriver.Edge()
    else:
        raise pytest.UsageError(f"Неподдерживаемый браузер: '{browser_name}'")

    driver.maximize_window()

    # Выставляем неявное ожидание в ноль
    driver.implicitly_wait(0)

    yield driver

    driver.quit()
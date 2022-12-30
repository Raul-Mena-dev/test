import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import datetime
import os
import time


@pytest.fixture(scope='session')
def driver(request):
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--disable-dev-shm-usage')
    wd = webdriver.Chrome(service=Service(ChromeDriverManager().install()), chrome_options=chrome_options)
    wd.maximize_window()
    wd.implicitly_wait(5)
    yield wd
    wd.quit()


@pytest.fixture()
def driver2(request):
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--disable-dev-shm-usage')
    wd = webdriver.Chrome(service=Service(ChromeDriverManager().install()), chrome_options=chrome_options)
    wd.maximize_window()
    wd.implicitly_wait(5)
    yield wd
    wd.quit()


def pytest_addoption(parser):
    fecha = datetime.date.today()
    fecha = fecha - datetime.timedelta(days=1)
    parser.addoption(
        "--fecha_test", action="store", default=str(fecha),
    )


@pytest.fixture
def fecha_test(request):
    return request.config.getoption("--fecha_test")


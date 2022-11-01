import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import datetime
import os
import time


@pytest.fixture(scope='session')
def driver(request):
    wd = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    wd.maximize_window()
    wd.implicitly_wait(5)
    yield wd
    wd.quit()


@pytest.fixture()
def driver2(request):
    wd = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
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


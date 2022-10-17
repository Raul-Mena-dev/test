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


def pytest_html_report_title(report):
    x = datetime.datetime.now()
    x = x.strftime("%m-%d-%Y-%H-%M-%S")
    report.title = x




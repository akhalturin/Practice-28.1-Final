import pytest
from selenium import webdriver


@pytest.fixture
def driver():
    driver = webdriver.Chrome('C:/Desktop/chromedriver_win32/chromedriver.exe')
    driver.implicitly_wait(3)

    yield driver

    driver.quit()
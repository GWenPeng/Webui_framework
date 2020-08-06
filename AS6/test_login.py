from selenium import webdriver
from Common.readdrivers import Read_drivers

import pytest


# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
#

@pytest.mark.skip
def test_login(driver):
    """
    "browserName": "MicrosoftEdge"
    "browserName": "internet explorer"
    "browserName": "chrome"
    "browserName": "firefox"
    :return:
    """
    # browsname = input()
    # global driver
    driver = webdriver.Chrome(Read_drivers().get_driver_path("gecko"))
    # driver.get("http://10.2.180.93:8000")
    # browserName = ["MicrosoftEdge", "internet explorer", "chrome", "firefox"]
    # for browser in browserName:
    # driver = webdriver.Remote(command_executor="http://10.2.180.223:15000/wd/hub",
    #                           desired_capabilities={"browserName": request.config.getoption(name="--browsername")})
    try:
        # driver = webdriver.Edge()
        driver.implicitly_wait(60)
        driver.get("http://10.2.180.93:8000")
        el = driver.find_element_by_css_selector('input[placeholder="请输入账号"]')
        el.send_keys("admin")
        el.is_displayed()
    finally:
        driver.quit()

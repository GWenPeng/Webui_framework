# coding=utf-8
from selenium import webdriver
from functools import wraps
import os
import allure
import time



#
# class Screen_shot(object):
#     def __init__(self, Driver):
#         # self.driver = webdriver.Chrome()
#         self.driver = Driver
#         print(Driver)
#
#     def __call__(self, f):
#         def inner(*args, **kwargs):
#             try:
#                 print(f, type(f))
#                 print(".........................")
#
#                 print(*args, type(*args))
#                 print("........................")
#
#                 return f(*args, **kwargs)
#             except Exception:
#                 nowTime = time.strftime("%Y_%m_%d_%H_%M_%S")
#                 print("....................")
#                 print(self.driver)
#                 print("...................")
#                 self.driver.get_screenshot_as_file("C:\\Users\\gu.wenpeng\\PycharmProjects\\webconsoleuitest"
#                                                    "\\screen_shot\\%s.png" % nowTime)
#                 with open("C:\\Users\\gu.wenpeng\\PycharmProjects\\webconsoleuitest\\screen_shot\\%s.png" % nowTime,
#                           mode='rb') as file:
#                     file = file.read()
#                     allure.attach(file, "错误截图", allure.attachment_type.PNG)
#                 raise
#
#         return inner


def screenshot(driver):
    def sceen_decorator(a_func):
        @wraps(a_func)
        def get_picture(*args, **kwargs):
            try:
                return a_func(*args, **kwargs)
            except Exception:
                nowTime = time.strftime("%Y_%m_%d_%H_%M_%S")
                father_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                print("....................")
                print(driver)
                print("...................")
                driver.get_screenshot_as_file(father_path + "/screen_shot/%s.png" % nowTime)
                with open(father_path + "/screen_shot/%s.png" % nowTime,
                          mode='rb') as file:
                    file = file.read()
                    allure.attach(file, "错误截图", allure.attachment_type.PNG)
                raise

        return get_picture

    return sceen_decorator


class ScreenShot:
    def __init__(self, Driver):
        self.driver = Driver

    # def screen(self):
    #     nowTime = time.strftime("%Y_%m_%d_%H_%M_%S")
    #     father_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    #     self.driver.get_screenshot_as_file(father_path + "/screen_shot/%s.png" % nowTime)
    #     with open(father_path + "/screen_shot/%s.png" % nowTime, mode='rb') as file:
    #         file = file.read()
    #         allure.attach(file, "错误截图", allure.attachment_type.PNG)

    def __call__(self, name):
        nowTime = time.strftime("%Y_%m_%d_%H_%M_%S")
        father_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.driver.get_screenshot_as_file(father_path + "/screen_shot/%s.png" % nowTime)
        with open(father_path + "/screen_shot/%s.png" % nowTime, mode='rb') as file:
            file = file.read()
            allure.attach(file, "异常截图名称：" + name, allure.attachment_type.PNG)

# driver = webdriver.Chrome("../Drivers/chromedriver.exe")
#
#
# class Test_aa:
#     # @pytest.fixture(scope="function")
#     # def setup(self,driver):
#     #     driver.get("http://10.2.180.93:8000")
#
#     @pytest.fixture(scope="function")
#     def teardown(self, driver):
#         yield
#         driver.quit()
#
#     @screenshot(driver)
#     def test_as6(self, teardown):
#         driver.get("http://10.2.180.93:8000")
#         driver.implicitly_wait(30)
#         el = driver.find_element_by_css_selector(
#             "input._-_-_-_-node_modules--anyshare-console-lib-LoginConsole-styles-view"
#             "---input-login22")
#         el.click()
#         el.clear()
#         el.send_keys("admin")

# if __name__ == '__main__':
#     driver = webdriver.Chrome("../Drivers/chromedriver.exe")
#     driver.get("http://10.2.180.93:8000")
#     time.sleep(10)
#
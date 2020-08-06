from selenium import webdriver
from Common.mysqlconnect import DB_connect

import allure


class ClientLoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.el_username = "//input[@placeholder='请输入账号']"  # 账号输入框
        self.el_pwd = "//input[@placeholder='请输入密码']"  # 密码输入框
        self.el_submit = "//span[text()='登 录']"  # 登录按钮
        self.el_code_input = "//input[@placeholder='请输入验证码']"  # 验证码输入框
        self.el_check_button = "//span[text()='立即验证']"  # 立即验证按钮
        self.el_quick_start_cancel = "//h1[text()='欢迎使用']/../div[1]"  # 快速入门关闭按钮

    @allure.step("客户端登录")
    def login(self, username, pwd):
        self.driver.find_element_by_xpath(self.el_username).send_keys(username)
        self.driver.find_element_by_xpath(self.el_pwd).send_keys(pwd)
        self.driver.find_element_by_xpath(self.el_submit).click()


if __name__ == '__main__':
    pass

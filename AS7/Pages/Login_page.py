from selenium import webdriver
from Common.mysqlconnect import DB_connect
import allure
import time


class Login_page:
    def __init__(self, driver):
        self.driver = driver
        # self.driver = webdriver.Chrome()
        self.el_username = 'input[placeholder="请输入账号"]'  # 账号输入框
        self.el_password = 'input[type="password"][placeholder="请输入密码"]'  # 密码输入框
        self.el_vcode = 'input[placeholder="请输入验证码"]'
        self.el_submit = 'button[type="submit"]'  # 登录按钮
        self.el_login = '//button/span[text()="登 录"]'  # oauth认证跳转按钮

    @allure.step("登录AS7")
    def login(self, username, password):
        """

        :param username:
        :param password:
        :return:
        """
        self.driver.implicitly_wait(20)
        self.driver.maximize_window()
        el_bt = self.driver.find_element_by_xpath(self.el_login)  # oath登录认证按钮
        el_bt.click()
        if self.driver.desired_capabilities["browserName"] == "Safari":
            time.sleep(5)
            wins = self.driver.window_handles
            self.driver.switch_to.window(wins[-1])
        el = self.driver.find_element_by_css_selector(self.el_username)
        el.send_keys(username)
        ps = self.driver.find_element_by_css_selector(self.el_password)
        ps.send_keys(password)
        try:
            el_vcode = self.driver.find_element_by_css_selector(self.el_vcode)
            el_vcode.send_keys(self.get_code())
        except Exception as e:
            print("没有验证码输入框", e)
        el_confirm = self.driver.find_element_by_css_selector(self.el_submit)
        el_confirm.click()

    @allure.step("获取图形验证码")
    def get_code(self):
        host = self.driver.current_url.split('//')[-1].split('/')[0]
        f_vode = DB_connect(host=host).select_one(
            "SELECT f_vcode FROM sharemgnt_db.`t_vcode` ORDER BY f_createtime DESC LIMIT 1;")
        return f_vode[0]


if __name__ == '__main__':
    # Login_page().login(username="admin", password="eisoo.cn")
    print(Login_page.get_code())

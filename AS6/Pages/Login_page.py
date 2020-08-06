from selenium import webdriver
import time


class Login_page:
    def __init__(self, driver):
        self.driver = driver
        # self.driver=webdriver.Chrome()
        self.el_username = 'input[placeholder="请输入账号"]'  # 账号输入框
        self.el_password = 'input[type="password"][placeholder="请输入密码"]'  # 密码输入框
        self.el_submit = 'button[type="submit"]'  # 登录按钮
        # self.el_submit = '//*[@id="index"]/div/div[2]/div/div/div[2]/div[3]/form/div[3]/button'  # 登录按钮

    def login(self, username, password):
        """

        :param username:
        :param password:
        :return:
        """
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()
        el = self.driver.find_element_by_css_selector(self.el_username)
        el.send_keys(username)
        ps = self.driver.find_element_by_css_selector(self.el_password)
        ps.send_keys(password)
        # time.sleep(5)
        el_confirm = self.driver.find_element_by_css_selector(self.el_submit)
        el_confirm.click()


if __name__ == '__main__':
    # Login_page().login(username="admin", password="eisoo.cn")
    pass

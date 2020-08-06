# coding=utf-8
from selenium import webdriver
import allure
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from Common.screenshot import ScreenShot
from selenium.webdriver.support import expected_conditions as ec


class Domain_mgnt_home_page(object):
    """
    文档域管理首页
    """

    def __init__(self, driver):
        self.driver = driver
        # self.driver = webdriver.Chrome()
        self.el_Domain_module = "//a[span[text()='文档域管理']]"  # 文档域管理一级TAB栏
        self.el_right_security = '//span[text()="安全管理"]/../../following-sibling::li[1]/a/span[text()="文档域管理"]'  # 安全管理右侧元素
        self.el_left_Operations = '//span[text()="运营管理"]/../../preceding-sibling::li[1]/a/span[text()="文档域管理"]'  # 运营管理左侧元素
        self.el_domain_tab = "div#main>div>div>div:nth-child(2)>div"  # 文档域侧边栏 css
        self.el_domain_mgnt = "div#main>div>div>div:nth-child(2)>div>div>ul>li:nth-child(1)"  # 文档域域管理选项
        # self.el_policy_sync = "div#main>div>div>div:nth-child(2)>div>div>ul>li:nth-child(2)"  # 策略同步选项
        # self.el_policy_sync = "//li[span[text()='策略同步']]"
        self.el_policy_sync = "//span[text()='策略同步']"
        self.el_windows_cancel = '//button/span[text()="取消"]'  # 关闭弹窗
        self.el_windows_confirm = '//button/span[text()="确定"]'

    @allure.step("返回文档域首页")
    def return_domain_home_page(self):
        # try:
            WebDriverWait(self.driver, 30).until(ec.visibility_of_element_located((By.XPATH, self.el_Domain_module)))
            self.driver.find_element_by_xpath(self.el_Domain_module).click()
        # except Exception:
        #
        #     raise

    @allure.step("定位到策略同步")
    def policy_sync(self):
        # WebDriverWait(self.driver, 60).until(
        #     ec.visibility_of_element_located((By.CSS_SELECTOR, self.el_Domain_module)))
        # self.driver.find_element_by_css_selector(self.el_Domain_module).click()
        # self.return_domain_home_page()
        # WebDriverWait(self.driver, 60).until(
        #     ec.visibility_of_element_located((By.CSS_SELECTOR, self.el_policy_sync)))
        # self.driver.find_element_by_css_selector(self.el_policy_sync).click()
        # try:
            WebDriverWait(self.driver, 60).until(ec.visibility_of_element_located((By.XPATH, self.el_policy_sync)))
            element = self.driver.find_element_by_xpath(self.el_policy_sync)
            self.driver.execute_script("$(arguments[0]).click()", element)
        # except Exception:
        #
        #     raise

    @allure.step("关闭弹窗")
    def close_windows(self):
        try:
            element_cancel = WebDriverWait(self.driver, 10).until(
                ec.visibility_of_element_located((By.XPATH, self.el_windows_cancel)))
            element_confirm = WebDriverWait(self.driver, 10).until(
                ec.visibility_of_element_located((By.XPATH, self.el_windows_confirm)))
            if not element_cancel and not element_confirm:
                pass
            else:
                element_cancel.click()
        except Exception as e:
            print("弹窗不存在!", e)

from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class Home_page:
    def __init__(self, driver):
        self.driver = driver
        self.el_organizations = "//a[span[text()='组织管理']]"
        self.el_Security = "//a[span[text()='安全管理']]"
        self.el_Domains = "//a[span[text()='文档域管理']]"
        self.el_Operations = "//a[span[text()='运营管理']]"
        self.el_LogsAudit = "//a[span[text()='审计管理']]"
        self.el_organizations_words = "//div[@id='head']/div/div/div/ul[1]/li[1]/a/span"
        self.el_security_words = "//div[@id='head']/div/div/div/ul[1]/li[2]/a/span"
        self.el_domains_words = "//div[@id='head']/div/div/div/ul[1]/li[3]/a/span"
        self.el_operations_words = "//div[@id='head']/div/div/div/ul[1]/li[4]/a/span"
        self.el_logsaudit_words = "//div[@id='head']/div/div/div/ul[1]/li[5]/a/span"
        self.el_domains_list = "//*[@id='main']/div/div/div[2]/div[2]/div/ul/li"    # 文档域侧边栏栏目
        self.el_admin = "//span[text()='admin']"  # 右上角admin按钮
        self.el_login_out = "//span[text()='退出']"  # 退出按钮

    def login_out(self):
        WebDriverWait(self.driver, 120).until(
            ec.visibility_of(self.driver.find_element_by_xpath(self.el_admin)))
        ActionChains(self.driver).move_to_element(self.driver.find_element_by_xpath(self.el_admin)).perform()
        WebDriverWait(self.driver, 120).until(
            ec.visibility_of(self.driver.find_element_by_xpath(self.el_login_out)))
        self.driver.find_element_by_xpath(self.el_login_out).click()

if __name__ == '__main__':
    # Login_page().login(username="admin", password="eisoo.com")
    pass
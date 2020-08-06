import pytest
import allure
import time
from AS7.Pages.Domain_mgnt.domain_mgnt_home_page import Domain_mgnt_home_page
from AS7.Pages.Domain_mgnt.domain_mgnt_page import Domain_mgnt_page
from AS7.Pages.Domain_mgnt.CommonDocDomain import CommonDocDomain
from Common.screenshot import ScreenShot
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By


class Test_add_domain_check(object):
    @allure.testcase("CaseID:5692 文档域管理--添加子域--该文档域为当前域 ")
    @pytest.mark.ni
    @pytest.mark.normal
    def test_add_selfaschild(self, driver, request, get_domain):
        # try:
            # 获取当前IP
            host = request.config.getoption("--host")
            ssh_host = host.split('//')[1].split(':')[0]  # 举例：ssh_host = 10.2.176.176
            dmhp = Domain_mgnt_home_page(driver=driver)
            dmp = Domain_mgnt_page(driver)
            # driver.implicitly_wait(40)
            # 定位至文档域管理界面
            dmhp.return_domain_home_page()
            # 点击[添加文档域]
            WebDriverWait(driver, 60).until(
                ec.visibility_of_element_located((By.CSS_SELECTOR, dmp.el_add_domain)))
            driver.find_element_by_css_selector(dmp.el_add_domain).click()
            # 等待添加文档域弹窗显示
            WebDriverWait(driver, 60).until(
                ec.visibility_of_element_located((By.XPATH, dmp.el_add_domain_title)))
            # 添加自己为子域，输入自己的IP
            domainname = driver.find_element_by_css_selector(dmp.el_domain_name_input)
            domainname.click()
            domainname.send_keys(ssh_host)
            # 输入appid和appkey
            appid = driver.find_element_by_css_selector(dmp.el_appid_input)
            appkey = driver.find_element_by_css_selector(dmp.el_appkey_input)
            appid.click()
            appkey.click()
            appid.send_keys("1")
            appkey.send_keys("1")
            # 点击[确定]按钮，校验报错
            driver.find_element_by_css_selector(dmp.el_confirm).click()
            WebDriverWait(driver, 60).until(
                ec.visibility_of_element_located((By.XPATH, dmp.el_addself_aschild)))
            errword = driver.find_element_by_xpath(dmp.el_addself_aschild).text
            assert errword == "您不能添加当前域为子域。"
            # 点击取消，去除用例影响
            driver.find_element_by_css_selector(dmp.el_cancel).click()
        # except Exception:

        #     Domain_mgnt_home_page(driver).close_windows()
        #     raise

    @allure.testcase("CaseID:5676 文档域管理--添加平级域-该文档域为当前域 ")
    @pytest.mark.ni
    @pytest.mark.normal
    def test_add_selfasparallel(self, driver, request):
        # try:
            # 获取当前IP
            host = request.config.getoption("--host")
            ssh_host = host.split('//')[1].split(':')[0]  # 举例：ssh_host = 10.2.176.176
            dmp = Domain_mgnt_page(driver)
            # 点击[添加文档域]
            WebDriverWait(driver, 60).until(
                ec.visibility_of_element_located((By.CSS_SELECTOR, dmp.el_add_domain)))
            driver.find_element_by_css_selector(dmp.el_add_domain).click()
            # 等待添加文档域弹窗显示
            WebDriverWait(driver, 60).until(
                ec.visibility_of_element_located((By.XPATH, dmp.el_add_domain_title)))
            # 选择添加平级域
            driver.find_element_by_css_selector(dmp.el_input_parallel_domain).click()
            WebDriverWait(driver, 60).until(
                ec.visibility_of_element_located((By.CSS_SELECTOR, dmp.el_domain_name_parallel)))
            # 添加自己为平级域，输入平级域信息
            domainname = driver.find_element_by_css_selector(dmp.el_domain_name_parallel)
            domainname.click()
            domainname.send_keys(ssh_host)
            # 点击[确定]，校验报错
            driver.find_element_by_css_selector(dmp.el_confirm).click()
            WebDriverWait(driver, 60).until(
                ec.visibility_of_element_located((By.XPATH, dmp.el_addself_asparallel)))
            errword = driver.find_element_by_xpath(dmp.el_addself_asparallel).text
            assert errword == "您不能添加当前域为平级域。"
            # 点击取消，去除用例影响
            driver.find_element_by_css_selector(dmp.el_cancel).click()
        # except Exception:
        #
        #     Domain_mgnt_home_page(driver).close_windows()
        #     raise

    @pytest.fixture(scope="function")
    def add_child(self, driver, request, get_domain):
        host = request.config.getoption("--host")
        ssh_host = host.split('//')[1].split(':')[0]  # 举例：ssh_host = 10.2.176.176
        father_domain = get_domain["father_domain"]
        # father_domain添加当前域为子域
        domainuuid = CommonDocDomain().addRelationDomain(httphost=father_domain, host=ssh_host)
        yield father_domain
        dmhp = Domain_mgnt_home_page(driver)
        CommonDocDomain().delRelationDomain(host=father_domain, uuid=domainuuid)
        driver.find_element_by_xpath("//a[span[text()='组织管理']]").click()
        dmhp.return_domain_home_page()

    @allure.testcase("CaseID:5675 文档域管理--添加平级域-该文档域为当前域父域 ")
    @pytest.mark.ni
    @pytest.mark.normal
    def test_addfather_asparallel(self, driver, add_child):
        # try:
            dmhp = Domain_mgnt_home_page(driver)
            dmp = Domain_mgnt_page(driver)
            father_domain = add_child
            driver.find_element_by_xpath("//a[span[text()='组织管理']]").click()
            dmhp.return_domain_home_page()
            time.sleep(2)
            # driver.implicitly_wait(15)
            # 点击[添加文档域]
            WebDriverWait(driver, 60).until(
                ec.visibility_of_element_located((By.CSS_SELECTOR, dmp.el_add_domain)))
            driver.find_element_by_css_selector(dmp.el_add_domain).click()
            # 等待添加文档域弹窗显示
            WebDriverWait(driver, 60).until(
                ec.visibility_of_element_located((By.XPATH, dmp.el_add_domain_title)))
            WebDriverWait(driver, 60).until(
                ec.visibility_of_element_located((By.CSS_SELECTOR, dmp.el_domain_name_parallel)))
            # 添加父域为平级域，输入父域信息
            domainname = driver.find_element_by_css_selector(dmp.el_domain_name_parallel)
            domainname.click()
            domainname.send_keys(father_domain)
            # 点击[确定]，校验是否添加成功
            driver.find_element_by_css_selector(dmp.el_confirm).click()
            WebDriverWait(driver, 60).until(
                ec.visibility_of_element_located((By.XPATH, dmp.el_list_domain_name)))
            parallelname = driver.find_element_by_xpath(dmp.el_list_domain_name).text
            assert parallelname == father_domain
            # 删除平级域
            driver.find_element_by_css_selector(dmp.el_delete_button).click()
            driver.find_element_by_xpath(dmp.el_delete_confirm).click()
        # except Exception:
        #
        #     Domain_mgnt_home_page(driver).close_windows()
        #     raise

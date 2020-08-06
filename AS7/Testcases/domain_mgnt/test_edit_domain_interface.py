# coding=utf-8
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from AS7.Pages.Domain_mgnt.domain_mgnt_home_page import Domain_mgnt_home_page
from AS7.Pages.Domain_mgnt.domain_mgnt_page import Domain_mgnt_page
from selenium.webdriver.common.action_chains import ActionChains
from Common.parse_data import do_excel
import allure
import pytest
import time

from Common.screenshot import ScreenShot


@pytest.mark.wq_suite
class Test_EditChildDomain_Interface:
    @allure.step("清除数据")
    @pytest.fixture(scope="function")
    def fun(self, driver, get_domain):
        host = get_domain["parallel_domain"]
        # 添加子域
        Domain_mgnt_home_page(driver=driver).return_domain_home_page()
        Domain_mgnt_page(driver=driver).add_domain(domain_name=host, appid="admin", appkey="eisoo",
                                                   domain_type="child", direct_mode=False,
                                                   is_submit=True)
        yield
        # 删除子域
        Domain_mgnt_page(driver=driver).delete_domain_by_name(domain_name=host)
        time.sleep(2)

    @allure.testcase("caseid：5418--编辑子域--页面检查")
    @pytest.mark.high
    def test_interface_check(self, driver, get_domain, fun):
        # try:
            el_edit = Domain_mgnt_page(driver)
            domain_info = Domain_mgnt_page(driver).get_domain_info()
            WebDriverWait(driver, 60).until(
                ec.visibility_of_element_located((By.XPATH, el_edit.el_edit_domain)))
            driver.find_element_by_xpath(el_edit.el_edit_domain).click()
            WebDriverWait(driver, 60).until(
                ec.visibility_of_element_located((By.XPATH, el_edit.el_edit_h1)))
            # 断言域类型
            domain_type = driver.find_element_by_xpath(el_edit.el_edit_type).text
            assert domain_type == domain_info[1]
            # 断言域名输入框信息以及输入框状态
            domain_name_input = driver.find_element_by_css_selector(el_edit.el_domain_name_input)
            domain_name = domain_name_input.get_attribute('value')
            assert domain_name == domain_info[0]   # 断言域名默认信息
            # domain_name_class = domain_name_input.get_attribute('class')
            # assert domain_name_class.split("-")[-1] == "disabled"
            domain_name_status = domain_name_input.is_enabled()
            assert domain_name_status == False
            # 断言端口输入框信息
            domain_port = driver.find_element_by_xpath(el_edit.el_edit_port).get_attribute('value')
            assert domain_port == "443"
            # 断言APP ID输入框信息
            domain_appid = driver.find_element_by_xpath(el_edit.el_edit_appid).get_attribute('value')
            assert domain_appid == "admin"
            # 断言APP Key输入框信息
            domain_key = driver.find_element_by_xpath(el_edit.el_edit_appkey).get_attribute('value')
            assert domain_key == "eisoo"
            # 关闭编辑子域弹窗
            driver.find_element_by_xpath(el_edit.el_edit_cancel).click()
            time.sleep(2)
        # except Exception:
        #
        #     Domain_mgnt_home_page(driver).close_windows()

    @allure.testcase("caseid: 5420--编辑子域--APP ID && Key为空气泡提示")
    @pytest.mark.high
    def test_idkey_tips(self, driver, fun):
        # try:
            # 进入编辑子域弹窗
            el_edit = Domain_mgnt_page(driver)
            WebDriverWait(driver, 60).until(
                ec.visibility_of_element_located((By.XPATH, el_edit.el_edit_domain)))
            driver.find_element_by_xpath(el_edit.el_edit_domain).click()
            WebDriverWait(driver, 60).until(
                ec.visibility_of_element_located((By.XPATH, el_edit.el_edit_h1)))
            # APP ID输入框为空
            id_name = driver.find_element_by_css_selector(el_edit.el_appid_input)
            Domain_mgnt_page(driver).clear_input(id_name)
            driver.find_element_by_xpath(el_edit.el_edit_confirm).click()
            id_name.click()
            appid_hint = driver.find_element_by_xpath(el_edit.el_domain_appid_hint)
            action = ActionChains(driver=driver)
            action.move_to_element(appid_hint).perform()
            appid_text = driver.find_element_by_xpath(el_edit.el_prot_null_hint).text
            assert appid_text == "此输入项不允许为空。"

            # APP Key输入框为空
            key_name = driver.find_element_by_css_selector(el_edit.el_appkey_input)
            Domain_mgnt_page(driver).clear_input(key_name)
            driver.find_element_by_xpath(el_edit.el_edit_confirm).click()
            key_name.click()
            appkey_hint = driver.find_element_by_xpath(el_edit.el_domain_appkey_hint)
            action2 = ActionChains(driver=driver)
            action2.move_to_element(appkey_hint).perform()
            appkey_text = driver.find_element_by_xpath(el_edit.el_prot_null_hint).text
            assert appkey_text == "此输入项不允许为空。"

            # 关闭编辑子域弹窗
            driver.find_element_by_xpath(el_edit.el_edit_cancel).click()
            time.sleep(2)
        # except Exception:
        #
        #     Domain_mgnt_home_page(driver).close_windows()
    @allure.testcase("caseid: 5419--编辑子域--端口气泡提示")
    @pytest.mark.high
    def test_port_tipes(self, driver, get_domain, fun):
        # try:
            el_edit = Domain_mgnt_page(driver)
            WebDriverWait(driver, 60).until(
                ec.visibility_of_element_located((By.XPATH, el_edit.el_edit_domain)))
            driver.find_element_by_xpath(el_edit.el_edit_domain).click()
            WebDriverWait(driver, 60).until(
                ec.visibility_of_element_located((By.XPATH, el_edit.el_edit_h1)))
            port_name = driver.find_element_by_css_selector(el_edit.el_port_input)
            Domain_mgnt_page(driver).clear_input(port_name)
            driver.find_element_by_xpath(el_edit.el_edit_confirm).click()
            port_name.click()
            port_hint = driver.find_element_by_css_selector(el_edit.el_domain_port_hint)
            action3 = ActionChains(driver=driver)
            action3.move_to_element(port_hint).perform()
            port_text = driver.find_element_by_xpath(el_edit.el_prot_null_hint).text
            assert port_text == "此输入项不允许为空。"
            data = do_excel(filename='add_policy.xlsx', sheetname='文档域', minrow=2, maxrow=5, mincol=1, maxcol=3)
            print(data[0][0])
            # 输入端口为65536，点击【确定】，气泡提示
            driver.find_element_by_xpath(el_edit.el_edit_port).send_keys(data[0][0])
            driver.find_element_by_xpath(el_edit.el_edit_confirm).click()
            port_name.click()
            port_hints = driver.find_element_by_css_selector(el_edit.el_domain_port_hint)
            action4 = ActionChains(driver=driver)
            action4.move_to_element(port_hints).perform()
            message = driver.find_element_by_xpath(el_edit.el_prot_range_hint).text
            assert message == "端口号必须是 1~65535 之间的整数。"
            # 关闭编辑子域弹窗
            driver.find_element_by_xpath(el_edit.el_edit_cancel).click()
            time.sleep(2)
        # except Exception:
        #
        #     Domain_mgnt_home_page(driver).close_windows()
        #     raise
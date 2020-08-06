# coding=utf-8
from AS7.Pages.Domain_mgnt.domain_mgnt_home_page import Domain_mgnt_home_page
from AS7.Pages.Domain_mgnt.domain_mgnt_page import Domain_mgnt_page
from AS7.Pages.Domain_mgnt.doc_policy_page import doc_policy_page
from Common.parse_data import do_excel
from Common.screenshot import ScreenShot
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

# from Common.screenshot import Screen_shot
from Common.mysqlconnect import DB_connect
from Common.thrift_client import Thrift_client
from ShareMgnt import ncTShareMgnt

import pytest
import allure
import time


class TestRemoveBindingSuccess:

    @pytest.fixture(scope="function")
    def clear_data(self, request):
        yield
        host = request.config.getoption(name="--host")
        host = host.split('//')[1].split(':')[0]
        db = DB_connect(host=host)

        delete_sql = "delete from domain_mgnt.t_relationship_domain where f_domain_type = 'child'"
        delete_policy_sql = "delete from domain_mgnt.t_policy_tpls where f_name = '上海爱数'"
        update_domian = "update domain_mgnt.t_domain_self set f_type = 'parallel' "
        db.delete(delete_policy_sql)  # 删除策略
        # db.delete(delete_sql)  # 删除子域
        # db.update(update_domian)  # 恢复主域身份

    @allure.testcase("caseid:5442,文档域管理--解除绑定成功")
    @pytest.mark.high
    @pytest.mark.jt_suite
    def test_remove_binding_success(self, driver, get_domain, clear_data):
        # try:
            Domain_mgnt_home_page(driver).return_domain_home_page()  # 进入文档域管理
            time.sleep(3)
            Domain_mgnt_page(driver).add_domain(domain_name=get_domain['replace_domain'], appid='1', appkey='1')  # 添加子域
            Domain_mgnt_home_page(driver).policy_sync()  # 进入策略同步
            time.sleep(3)
            doc_policy_page(driver).add_policy(policy_name='上海爱数')  # 新增策略
            doc_policy_page(driver).apply_domain(domain_name=get_domain['replace_domain'])  # 策略绑定子域
            time.sleep(3)
            Domain_mgnt_home_page(driver).return_domain_home_page()  # 进入文档域管理
            time.sleep(3)
            Domain_mgnt_page(driver).remove_binding_by_index()  # 解除绑定
            time.sleep(3)
            assert Domain_mgnt_page(driver).get_domain_name_by_index(1, 4) == "---"  # 断言策略配置为“---”
            Domain_mgnt_page(driver).delete_domain()  # 删除子域
            Domain_mgnt_home_page(driver).policy_sync()  # 进入策略同步
            time.sleep(3)
            doc_policy_page(driver).delete_policy("上海爱数")  # 删除策略
        # except Exception:
        #
        #     Domain_mgnt_home_page(driver).close_windows()
        #     raise

    @allure.testcase("caseid: 5431--文档域管理--未配置文档库和策略--删除文档域")
    @pytest.mark.high
    @pytest.mark.wq
    def test_delete_domain(self, driver, get_domain):
        # try:
            host = get_domain['parallel_domain']
            domain = Domain_mgnt_page(driver)
            Domain_mgnt_home_page(driver).return_domain_home_page()
            Domain_mgnt_page(driver).add_domain(domain_name=host, domain_type='parallel')
            info = Domain_mgnt_page(driver).get_domain_info()
            assert info == [host, "平级域", "非直连", "---"]
            WebDriverWait(driver, 60).until(
                ec.visibility_of_element_located((By.CSS_SELECTOR, domain.el_delete_button)))
            driver.find_element_by_css_selector(domain.el_delete_button).click()
            WebDriverWait(driver, 60).until(
                ec.visibility_of_element_located((By.XPATH, domain.el_delete_domain_title)))
            hint_text = driver.find_element_by_xpath(domain.el_delete_domain_hint).text
            assert hint_text == '您确定要删除选中的文档域吗？'
            driver.find_element_by_xpath(domain.el_delete_cancel).click()
            driver.find_element_by_css_selector(domain.el_delete_button).click()
            driver.find_element_by_xpath(domain.el_delete_confirm).click()
            time.sleep(2)
        # except Exception:
        #
        #     Domain_mgnt_home_page(driver).close_windows()
        #     raise

    # @allure.testcase("caseid: 5969--文档域管理--删除平级域--目标域连接失败")
    # @pytest.mark.normal
    # @pytest.mark.wq
    # def test_delete_parallel(self, driver, get_domain):
    #     host = get_domain['parallel_domain']
    #     Domain_mgnt_home_page(driver).return_domain_home_page()
    #     Domain_mgnt_page(driver).add_domain(domain_name=host, domain_type='parallel', direct_mode=True, appid=11, appkey=22)
    #     time.sleep(3)
    #     # 目标域连接失败--删除域失败




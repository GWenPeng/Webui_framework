# coding=utf-8
from AS7.Pages.Domain_mgnt.domain_mgnt_home_page import Domain_mgnt_home_page
from AS7.Pages.Domain_mgnt.doc_policy_page import doc_policy_page
from AS7.Pages.Domain_mgnt.CommonDocDomain import CommonDocDomain
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from Common.screenshot import ScreenShot
from Common.NetworkDelay import NETWORKDELAY
from Common.mysqlconnect import DB_connect
import pytest
import allure
import time


class Test_policy_mgnt:
    """
    策略管理
    """

    @allure.step("新增策略")
    @pytest.fixture(scope="function")
    def add_policy(self, request):
        """

        :return:
        """
        host = request.config.getoption(name="--host")
        host = host.split('//')[1].split(':')[0]
        uuid = CommonDocDomain().addPolicy(httphost=host, content=[], name="这是一条子域策略")
        yield
        CommonDocDomain().deletepolicy(httphost=host, PolicyUUID=uuid)

    @allure.step("设置本域类型为子域")
    @pytest.fixture(scope="function")
    def set_self_child_domain(self, get_domain, request, driver, add_policy):
        host = request.config.getoption(name="--host")
        host = host.split('//')[1].split(':')[0]
        # f_domain = get_domain["father_domain"]
        uuid = CommonDocDomain().addRelationDomain(httphost=get_domain["father_domain"], host=host)
        yield
        CommonDocDomain().delRelationDomain(host=get_domain["father_domain"], uuid=uuid)
        Domain_mgnt_home_page(driver=driver).return_domain_home_page()
        time.sleep(1)

    @pytest.mark.gwp
    @pytest.mark.normal
    @allure.testcase("5541, 策略同步--删除策略配置（子域登录）")
    def test_policy_child_domain_check(self, driver, set_self_child_domain):
        """

        :return:
        """
        # try:
        Domain_mgnt_home_page(driver=driver).return_domain_home_page()
        dmhg = Domain_mgnt_home_page(driver)
        time.sleep(1)
        driver.find_element_by_xpath(dmhg.el_policy_sync).click()
        dpg = doc_policy_page(driver)
        WebDriverWait(driver, timeout=10.0).until(
            ec.visibility_of_element_located((By.XPATH, '//span[text()="这是一条子域策略"]')))
        is_disabled = driver.find_element_by_xpath(dpg.el_add_policy_bt).get_property("disabled")
        assert is_disabled is True
        is_edit_disabled = driver.find_element_by_css_selector(dpg.el_edit_policy_bt).get_property("disabled")
        assert is_edit_disabled is True
        policy_name = driver.find_element_by_css_selector(dpg.el_policy_list_name).text
        assert policy_name == "这是一条子域策略"

        driver.find_element_by_xpath(dpg.el_delete_policy).click()
        WebDriverWait(driver, timeout=10.0).until(
            ec.visibility_of_element_located((By.XPATH, dpg.el_delete_policy_pop)))
        driver.find_element_by_xpath(dpg.el_del_confirm_bt).click()
        time.sleep(1)

        # except Exception:
        #
        #     Domain_mgnt_home_page(driver).close_windows()
        #     raise

    @allure.step("创建策略")
    @pytest.fixture(scope="function")
    def create_policy(self, request):
        """

        :return:
        """
        host = request.config.getoption(name="--host")
        host = host.split('//')[1].split(':')[0]
        policy_uuid_list = []
        for index in range(20):
            policy_uuid = CommonDocDomain().addPolicy(httphost=host, name="PolicyName" + str(index))
            policy_uuid_list.append(policy_uuid)
        yield
        for uuid in policy_uuid_list:
            CommonDocDomain().deletepolicy(httphost=host, PolicyUUID=uuid)

    @allure.step("创建更多策略")
    @pytest.fixture(scope="function")
    def create_more_policy(self, request):
        """

        :return:
        """
        host = request.config.getoption(name="--host")
        host = host.split('//')[1].split(':')[0]
        policy_uuid_list = []
        for index in range(60):
            policy_uuid = CommonDocDomain().addPolicy(httphost=host, name="PolicyName" + str(index))
            policy_uuid_list.append(policy_uuid)
        yield
        for uuid in policy_uuid_list:
            CommonDocDomain().deletepolicy(httphost=host, PolicyUUID=uuid)

    @pytest.mark.gwp
    @pytest.mark.normal
    @allure.testcase("5683, 策略配置分页显示检查")
    def test_policy_by_page_check(self, driver, create_policy):
        """

        :param driver:
        :return:
        """
        # try:
        Domain_mgnt_home_page(driver=driver).return_domain_home_page()
        dmhg = Domain_mgnt_home_page(driver)
        dpg = doc_policy_page(driver)
        time.sleep(1)
        driver.find_element_by_xpath(dmhg.el_policy_sync).click()
        time.sleep(2)
        up_disabled = driver.find_element_by_xpath(dpg.el_up_page_icon).get_property("disabled")
        first_disabled = driver.find_element_by_xpath(dpg.el_first_page_icon).get_property("disabled")
        next_disabled = driver.find_element_by_xpath(dpg.el_next_page_icon).get_property("disabled")
        last_disabled = driver.find_element_by_xpath(dpg.el_last_page_icon).get_property("disabled")
        assert up_disabled is True
        assert first_disabled is True
        assert next_disabled is True
        assert last_disabled is True
        # except Exception:

        #     Domain_mgnt_home_page(driver).close_windows()
        #     raise

    @pytest.mark.gwp
    @pytest.mark.normal
    @allure.testcase("5683, 策略配置分页显示检查")
    @allure.testcase("5684, 文档域策略同步--搜索策略配置--清除搜索关键字")
    def test_policy_by_more_page_check(self, driver, create_more_policy):
        # try:
            Domain_mgnt_home_page(driver=driver).return_domain_home_page()
            dmhg = Domain_mgnt_home_page(driver)
            dpg = doc_policy_page(driver)
            time.sleep(1)
            driver.find_element_by_xpath(dmhg.el_policy_sync).click()
            # driver.find_element_by_xpath(dpg.el_page_input).send_keys("2")
            time.sleep(1)
            driver.find_element_by_xpath(dpg.el_next_page_icon).click()
            time.sleep(1)
            driver.find_element_by_xpath(dpg.el_next_page_icon).click()
            time.sleep(1)
            el_page_input = driver.find_element_by_xpath(dpg.el_page_input)
            assert el_page_input.get_attribute("value") == '3'
            el_page_count = driver.find_element_by_xpath(dpg.el_page_count)
            assert el_page_count.text == "显示 41 - 60 条，共 60 条"
            driver.find_element_by_xpath(dpg.el_up_page_icon).click()
            time.sleep(1)
            assert el_page_input.get_attribute("value") == '2'
            assert el_page_count.text == "显示 21 - 40 条，共 60 条"
            dpg.clear_input(el_page_input)
            el_page_input.send_keys("1")
            el_page_input.click()
            time.sleep(1)
            assert el_page_input.get_attribute("value") == "1"
            assert el_page_count.text == "显示 1 - 20 条，共 60 条"
            driver.find_element_by_xpath(dpg.el_last_page_icon).click()
            time.sleep(1)
            assert el_page_input.get_attribute("value") == "3"
            assert el_page_count.text == "显示 41 - 60 条，共 60 条"
            up_disabled = driver.find_element_by_xpath(dpg.el_up_page_icon).get_property("disabled")
            first_disabled = driver.find_element_by_xpath(dpg.el_first_page_icon).get_property("disabled")
            next_disabled = driver.find_element_by_xpath(dpg.el_next_page_icon).get_property("disabled")
            last_disabled = driver.find_element_by_xpath(dpg.el_last_page_icon).get_property("disabled")
            assert up_disabled is False
            assert first_disabled is False
            assert next_disabled is True
            assert last_disabled is True
            driver.find_element_by_xpath(dpg.el_first_page_icon).click()
            time.sleep(1)
            assert el_page_input.get_attribute("value") == "1"
            assert el_page_count.text == "显示 1 - 20 条，共 60 条"
            up_disabled = driver.find_element_by_xpath(dpg.el_up_page_icon).get_property("disabled")
            first_disabled = driver.find_element_by_xpath(dpg.el_first_page_icon).get_property("disabled")
            next_disabled = driver.find_element_by_xpath(dpg.el_next_page_icon).get_property("disabled")
            last_disabled = driver.find_element_by_xpath(dpg.el_last_page_icon).get_property("disabled")
            assert up_disabled is True
            assert first_disabled is True
            assert next_disabled is False
            assert last_disabled is False

            dpg.clear_input(el_page_input)
            el_page_input.send_keys("2")
            el_page_input.click()
            time.sleep(1)
            driver.find_element_by_xpath(dpg.el_policy_search).send_keys("无效关键字")
            WebDriverWait(driver, timeout=10.0).until(
                ec.visibility_of_element_located((By.XPATH, dpg.el_policy_search_empty)))
            WebDriverWait(driver, timeout=10.0).until(
                ec.visibility_of_element_located((By.XPATH, dpg.el_list_no_search_results)))
            driver.find_element_by_xpath(dpg.el_policy_search_empty).click()
            time.sleep(1)
            driver.find_element_by_xpath(dpg.el_policy_search).send_keys("PolicyName59")
            WebDriverWait(driver, timeout=10.0).until(
                ec.visibility_of_element_located((By.XPATH, dpg.el_policy_search_empty)))
            assert driver.find_element_by_xpath(dpg.el_policy_first).text == "PolicyName59"
            assert el_page_count.text == "显示 1 - 1 条，共 1 条"
            driver.find_element_by_xpath(dpg.el_policy_search_empty).click()
            time.sleep(1)
            assert driver.find_element_by_xpath(dpg.el_policy_first).text == "PolicyName0"
            assert el_page_input.get_attribute("value") == "1"
            assert el_page_count.text == "显示 1 - 20 条，共 60 条"
        # except Exception:

        #     Domain_mgnt_home_page(driver).close_windows()
        #     raise

    @allure.step("添加子域，应用策略")
    @pytest.fixture(scope="function")
    def add_child_bound_policy(self, driver, request, get_domain):
        """

        :return:
        """
        # try:
        host = request.config.getoption(name="--host")
        host = host.split('//')[1].split(':')[0]
        # f_domain = get_domain["father_domain"]
        uuid = CommonDocDomain().addRelationDomain(httphost=host, host=get_domain["replace_domain"])  # 添加子域

        Domain_mgnt_home_page(driver=driver).return_domain_home_page()
        dmhg = Domain_mgnt_home_page(driver)
        dpg = doc_policy_page(driver)
        time.sleep(1)

        driver.find_element_by_xpath(dmhg.el_policy_sync).click()
        driver.find_element_by_xpath(dpg.el_add_policy).click()
        driver.find_element_by_xpath(dpg.el_policy_name).send_keys("禁用登录web客户端策略")
        driver.find_element_by_xpath(dpg.el_restricted_client_login).click()
        WebDriverWait(driver, timeout=10.0).until(
            ec.visibility_of_element_located((By.XPATH, dpg.el_enable_restricted_client_login)))
        driver.find_element_by_xpath(dpg.el_enable_restricted_client_login).click()
        driver.find_element_by_xpath(dpg.el_web_client_option).click()
        driver.find_element_by_xpath(dpg.el_confirm_button).click()
        time.sleep(2)
        dpg.apply_domain(domain_name=get_domain["replace_domain"])
        time.sleep(3)
        # except Exception:

        #     Domain_mgnt_home_page(driver).close_windows()
        #     raise
        yield
        res = CommonDocDomain().getBoundPolicyChild(httphost=host, ChildDomainUUID=uuid)
        print(res)
        CommonDocDomain().delboundPolicy(httphost=host, PolicyUUID=res["id"], ChildDomainUUID=uuid)
        CommonDocDomain().delRelationDomain(host=host, uuid=uuid)
        CommonDocDomain().deletepolicy(httphost=host, PolicyUUID=res["id"])
        DB_connect(host=get_domain["replace_domain"]).update('UPDATE sharemgnt_db.t_sharemgnt_config set f_value="0" '
                                                             'where f_key="forbid_ostype";')
        Domain_mgnt_home_page(driver=driver).return_domain_home_page()
        time.sleep(10)

    @pytest.mark.gwp
    @pytest.mark.normal
    @allure.testcase("5614,  文档域策略同步--去勾选限制web客户端登录--用户登录 ")
    def test_policy_login_web(self, driver, add_child_bound_policy, get_domain):
        """

        :param driver:
        :param add_child_bound_policy：
        :return:
        """
        db = DB_connect(host=get_domain["replace_domain"])
        result = db.select_one('SELECT f_value from sharemgnt_db.t_sharemgnt_config where f_key="forbid_ostype";')
        print(result)
        assert result[0] == "64"

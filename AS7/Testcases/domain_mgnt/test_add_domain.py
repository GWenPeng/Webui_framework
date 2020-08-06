# coding=utf-8
from AS7.Pages.Domain_mgnt.domain_mgnt_home_page import Domain_mgnt_home_page
from AS7.Pages.Domain_mgnt.domain_mgnt_page import Domain_mgnt_page
from AS7.Pages.Domain_mgnt.CommonDocDomain import CommonDocDomain
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from Common.screenshot import ScreenShot
from Common.NetworkDelay import NETWORKDELAY
import pytest
import allure
import time


# @pytest.fixture(scope="function")
# def refresh(driver):
#     driver.refresh()


class Test_add_domain:
    @pytest.mark.gwp
    @pytest.mark.normal
    @allure.testcase("5464,文档域管理--添加子域--该文档域为父域")
    def test_parallel_add_father_domain(self, driver, get_domain):
        # try:
            Domain_mgnt_home_page(driver=driver).return_domain_home_page()
            Dgp = Domain_mgnt_page(driver=driver)
            Dgp.add_domain(domain_name=get_domain["father_domain"], appid="appid", appkey="appkey",
                           domain_type="child", direct_mode=True,
                           is_submit=True, port="443")
            # time.sleep(10)
            msg = driver.find_element_by_xpath(Dgp.el_error_msg_add_fdomain).text
            assert msg == "该文档域已是父域，不允许添加为子域。"
            driver.find_element_by_css_selector(Dgp.el_cancel).click()
        # except Exception:
        #
        #     Domain_mgnt_home_page(driver).close_windows()
        #     raise

    @allure.step("设置本域类型为子域")
    @pytest.fixture(scope="function")
    def set_self_child_domain(self, get_domain, request, driver):
        host = request.config.getoption(name="--host")
        host = host.split('//')[1].split(':')[0]
        # f_domain = get_domain["father_domain"]
        uuid = CommonDocDomain().addRelationDomain(httphost=get_domain["father_domain"], host=host)
        yield
        CommonDocDomain().delRelationDomain(host=get_domain["father_domain"], uuid=uuid)

    @pytest.mark.gwp
    @pytest.mark.normal
    @allure.testcase("5403,文档域管理--子域添加文档域--界面检查")
    def test_child_domain_check(self, driver, set_self_child_domain):
        # try:
            dmp = Domain_mgnt_page(driver=driver)
            dmhp = Domain_mgnt_home_page(driver=driver)
            dmhp.return_domain_home_page()
            time.sleep(1)
            driver.find_element_by_xpath(dmhp.el_policy_sync).click()
            time.sleep(1)
            driver.find_element_by_css_selector(dmhp.el_domain_mgnt).click()
            WebDriverWait(driver, 20).until(
                ec.visibility_of_element_located((By.XPATH, "//div[contains(text(),'当前文档域已被')]")))
            WebDriverWait(driver, 30, 1).until(
                ec.element_to_be_clickable((By.CSS_SELECTOR, dmp.el_add_domain)))
            driver.find_element_by_css_selector(dmp.el_add_domain).click()
            child_domain_class = driver.find_element_by_css_selector(dmp.el_child_domain).get_attribute("class")
            assert child_domain_class.split("-")[-1] == "disabled"
            parallel_domain_checked = driver.find_element_by_css_selector(dmp.el_input_parallel_domain).get_property(
                "checked")
            assert parallel_domain_checked is True
            driver.find_element_by_css_selector(dmp.el_cancel).click()
        # except Exception:
        #
        #     Domain_mgnt_home_page(driver).close_windows()
        #     raise

    @pytest.mark.gwp
    @pytest.mark.high
    @allure.testcase("5366,文档域管理--添加文档域--取消 ")
    def test_add_domain_cancel(self, driver, get_domain):
        # try:
            dmp = Domain_mgnt_page(driver=driver)
            dmhp = Domain_mgnt_home_page(driver=driver)
            dmhp.return_domain_home_page()
            time.sleep(1)
            driver.find_element_by_xpath(dmhp.el_policy_sync).click()
            time.sleep(1)
            driver.find_element_by_css_selector(dmhp.el_domain_mgnt).click()
            dmp.add_domain(domain_name="", appid="appid", appkey="appkey", is_submit=True)
            driver.find_element_by_css_selector(dmp.el_domain_name_input).click()
            warn_text = driver.find_element_by_xpath(dmp.el_domain_name_warn).text
            assert warn_text == "此输入项不允许为空。"
            driver.find_element_by_xpath(dmp.el_windows_x).click()
            WebDriverWait(driver, timeout=10.0).until(
                ec.invisibility_of_element_located((By.CSS_SELECTOR, dmp.el_windows)))
            dmp.add_domain(domain_name=get_domain["child_domain"], appkey="app_key", appid="app_id", is_submit=False)
            WebDriverWait(driver, timeout=10.0).until(
                ec.invisibility_of_element_located((By.CSS_SELECTOR, dmp.el_windows)))
        # except Exception:
        #
        #     Domain_mgnt_home_page(driver).close_windows()
        #     raise

    @pytest.fixture(scope="function")
    def clear_domain(self, driver, get_domain):
        yield
        dmp1 = Domain_mgnt_page(driver=driver)
        dmp1.delete_domain(index=1)
        time.sleep(1)
        dmp1.delete_domain(index=1)
        time.sleep(1)
        dmp1.delete_domain(index=1)

    @pytest.mark.gwp
    @pytest.mark.high
    @allure.testcase("5410,文档域管理--子域添加文档域--添加成功")
    @allure.testcase("5408,文档域管理--子域添加文档域--重复添加")
    def test_child_add_domain_success(self, driver, get_domain, set_self_child_domain, clear_domain):
        # try:
            dmp = Domain_mgnt_page(driver=driver)
            dmhp = Domain_mgnt_home_page(driver=driver)
            dmhp.return_domain_home_page()
            time.sleep(1)
            driver.find_element_by_xpath(dmhp.el_policy_sync).click()
            time.sleep(1)
            driver.find_element_by_css_selector(dmhp.el_domain_mgnt).click()
            WebDriverWait(driver, 20).until(
                ec.visibility_of_element_located((By.XPATH, "//div[contains(text(),'当前文档域已被')]")))
            dmp.add_domain(domain_name="child.eisoo.cn", domain_type="parallel", direct_mode=False)
            assert dmp.get_domain_name_by_index(1) == "child.eisoo.cn"
            dmp.add_domain(domain_name=get_domain["parallel_domain"], domain_type="parallel", direct_mode=True,
                           appkey="app_key",
                           appid="app_id")
            WebDriverWait(driver, 30).until(ec.visibility_of_element_located(
                (By.XPATH, dmp.el_list_domain_name + "[text()='" + get_domain["parallel_domain"] + "']")))
            assert dmp.get_domain_name_by_index(1) == get_domain["parallel_domain"]
            assert dmp.get_domain_name_by_index(2) == "child.eisoo.cn"
            dmp.add_domain(domain_name="father.eisoo.cn", domain_type="parallel", direct_mode=True, appkey="app_key",
                           appid="app_id")
            WebDriverWait(driver, 30).until(ec.visibility_of_element_located(
                (By.XPATH, dmp.el_list_domain_name + '[text()="father.eisoo.cn"]')))
            assert dmp.get_domain_name_by_index(1) == "father.eisoo.cn"
            dmp.add_domain(domain_name="father.eisoo.cn", domain_type="parallel", direct_mode=True, appkey="app_key",
                           appid="app_id")
            assert driver.find_element_by_xpath(dmp.el_error_msg_repet).text == "该文档域已存在，不允许重复添加。"
            driver.find_element_by_css_selector(dmp.el_cancel).click()
            dmp.add_domain(domain_name=get_domain["parallel_domain"], domain_type="parallel", direct_mode=True,
                           appkey="app_key",
                           appid="app_id")
            assert driver.find_element_by_xpath(dmp.el_error_msg_repet).text == "该文档域已存在，不允许重复添加。"
            driver.find_element_by_css_selector(dmp.el_cancel).click()
        # except Exception:
        #
        #     Domain_mgnt_home_page(driver).close_windows()
        #     raise

    @pytest.mark.gwp
    @pytest.mark.high
    @allure.testcase("5358,文档域管理--添加子域失败--域已被添加")
    def test_add_domain_ip_repeat_fail(self, driver, get_domain):
        # try:
            dmp = Domain_mgnt_page(driver=driver)
            dmhp = Domain_mgnt_home_page(driver=driver)
            dmhp.return_domain_home_page()
            time.sleep(2)
            driver.find_element_by_xpath(dmhp.el_policy_sync).click()
            time.sleep(2)
            driver.find_element_by_css_selector(dmhp.el_domain_mgnt).click()
            dmp.add_domain(domain_name=get_domain["parallel_domain"], domain_type="parallel")
            time.sleep(1)
            dmp.add_domain(domain_name=get_domain["replace_domain"], domain_type="child", appid="app_id",
                           appkey="app_key")
            time.sleep(1)
            dmp.add_domain(domain_name=get_domain["parallel_domain"], domain_type="parallel")
            WebDriverWait(driver, 30).until(ec.visibility_of_element_located(
                (By.XPATH, dmp.el_error_msg_repet)))
            assert driver.find_element_by_xpath(dmp.el_error_msg_repet).text == "该文档域已存在，不允许重复添加。"
            driver.find_element_by_css_selector(dmp.el_cancel).click()
            dmp.add_domain(domain_name=get_domain["parallel_domain"], domain_type="child", appid="app_id",
                           appkey="app_key")
            WebDriverWait(driver, 30).until(ec.visibility_of_element_located(
                (By.XPATH, dmp.el_error_msg_repet)))
            assert driver.find_element_by_xpath(dmp.el_error_msg_repet).text == "该文档域已存在，不允许重复添加。"
            driver.find_element_by_css_selector(dmp.el_cancel).click()
            time.sleep(1)
            dmp.add_domain(domain_name=get_domain["replace_domain"], domain_type="child", appid="app_id",
                           appkey="app_key")
            WebDriverWait(driver, 30).until(ec.visibility_of_element_located(
                (By.XPATH, dmp.el_error_msg_repet)))
            assert driver.find_element_by_xpath(dmp.el_error_msg_repet).text == "该文档域已存在，不允许重复添加。"
            driver.find_element_by_css_selector(dmp.el_cancel).click()
            dmp.add_domain(domain_name=get_domain["parallel_domain"], domain_type="parallel")
            WebDriverWait(driver, 30).until(ec.visibility_of_element_located(
                (By.XPATH, dmp.el_error_msg_repet)))
            assert driver.find_element_by_xpath(dmp.el_error_msg_repet).text == "该文档域已存在，不允许重复添加。"
            driver.find_element_by_css_selector(dmp.el_cancel).click()
            dmp.delete_domain(index=1)
            time.sleep(2)
            dmp.delete_domain(index=1)
            time.sleep(2)
            dmp.add_domain(domain_name="parallel.eisoo.cn", domain_type="parallel")
            time.sleep(1)
            dmp.add_domain(domain_name="replace.eisoo.cn", domain_type="child", appid="app_id", appkey="app_key")
            time.sleep(1)
            dmp.add_domain(domain_name="parallel.eisoo.cn", domain_type="parallel")
            WebDriverWait(driver, 30).until(ec.visibility_of_element_located(
                (By.XPATH, dmp.el_error_msg_repet)))
            assert driver.find_element_by_xpath(dmp.el_error_msg_repet).text == "该文档域已存在，不允许重复添加。"
            driver.find_element_by_css_selector(dmp.el_cancel).click()
            time.sleep(1)
            dmp.add_domain(domain_name="replace.eisoo.cn", domain_type="child", appid="app_id", appkey="app_key")
            WebDriverWait(driver, 30).until(ec.visibility_of_element_located(
                (By.XPATH, dmp.el_error_msg_repet)))
            assert driver.find_element_by_xpath(dmp.el_error_msg_repet).text == "该文档域已存在，不允许重复添加。"
            driver.find_element_by_css_selector(dmp.el_cancel).click()
            time.sleep(2)
            dmp.delete_domain(index=1)
            time.sleep(2)
            dmp.delete_domain(index=1)
            time.sleep(2)
            dmp.add_domain(domain_name="child.eisoo.cn", domain_type="child", appid="app_id", appkey="app_key")
            if driver.desired_capabilities["browserName"] == "Edge":
                assert driver.find_element_by_xpath(dmp.el_domain_added_warn_comm).text == "该文档域已被“" + get_domain[
                    "father_domain"] + "”添加为子域。"
            else:
                assert driver.find_element_by_xpath(dmp.el_domain_added_warn).text == "该文档域已被“" + get_domain[
                    "father_domain"] + "”添加为子域。"
            driver.find_element_by_css_selector(dmp.el_cancel).click()
            time.sleep(1)
            dmp.add_domain(domain_name=get_domain["child_domain"], domain_type="child", appid="app_id",
                           appkey="app_key")
            if driver.desired_capabilities["browserName"] == "Edge":
                assert driver.find_element_by_xpath(dmp.el_domain_added_warn_comm).text == "该文档域已被“" + get_domain[
                    "father_domain"] + "”添加为子域。"
            else:
                assert driver.find_element_by_xpath(dmp.el_domain_added_warn).text == "该文档域已被“" + get_domain[
                    "father_domain"] + "”添加为子域。"
            driver.find_element_by_css_selector(dmp.el_cancel).click()
            time.sleep(1)
        # except Exception:
        #
        #     Domain_mgnt_home_page(driver).close_windows()
        #     raise

    @pytest.fixture(scope="function")
    def del_domain(self, driver):
        yield
        dmp1 = Domain_mgnt_page(driver=driver)
        dmp1.delete_domain(index=1)
        time.sleep(1)

    @pytest.fixture(scope="function", )
    def add_delay(self, request):
        host = request.config.getoption("--host")
        host = host.split('//')[1].split(':')[0]
        NETWORKDELAY(host=host, delay_time="50").delay()
        yield
        NETWORKDELAY(host=host, delay_time="50").delete_delay()

    @pytest.mark.gwp
    @pytest.mark.high
    @allure.testcase("5365,文档域管理--添加平级域成功--直连模式(未开启加密传输)")
    def test_add_parallel_domain_direct(self, driver, del_domain, add_delay):
        # try:
            dmp = Domain_mgnt_page(driver=driver)
            dmhp = Domain_mgnt_home_page(driver=driver)
            dmhp.return_domain_home_page()
            time.sleep(2)
            driver.find_element_by_xpath(dmhp.el_policy_sync).click()
            time.sleep(2)
            driver.find_element_by_css_selector(dmhp.el_domain_mgnt).click()
            dmp.add_domain(domain_name="parallel.eisoo.cn", domain_type="parallel", direct_mode=True, appkey="app_key",
                           appid="app_id")

            assert driver.find_element_by_xpath(dmp.el_domain_added_link_warn).text == "正在连接，请稍候..."
            time.sleep(2)
            assert dmp.get_domain_name_by_index(row=1, col=1) == "parallel.eisoo.cn"
        # except Exception:
        #
        #     Domain_mgnt_home_page(driver).close_windows()
        #     raise

    @pytest.mark.gwp
    @pytest.mark.high
    @allure.testcase("5364,文档域管理--添加平级域成功--非直连模式(非加密传输）")
    def test_add_parallel_domain_indirect(self, driver, del_domain):
        # try:
            dmp = Domain_mgnt_page(driver=driver)
            dmhp = Domain_mgnt_home_page(driver=driver)
            dmhp.return_domain_home_page()
            time.sleep(2)
            driver.find_element_by_xpath(dmhp.el_policy_sync).click()
            time.sleep(2)
            driver.find_element_by_css_selector(dmhp.el_domain_mgnt).click()
            dmp.add_domain(domain_name="parallel.eisoo.cn", domain_type="parallel", direct_mode=False)
            # assert driver.find_element_by_xpath(dmp.el_domain_added_link_warn).text == "正在连接，请稍候..."
            time.sleep(2)
            assert dmp.get_domain_name_by_index(row=1, col=1) == "parallel.eisoo.cn"
        # except Exception:
        #
        #     Domain_mgnt_home_page(driver).close_windows()
        #     raise

    @pytest.mark.gwp
    @pytest.mark.high
    @allure.testcase("5350,文档域管理--入口检查")
    def test_domain_io_check(self, driver):
        # try:
            dmhp = Domain_mgnt_home_page(driver=driver)
            assert driver.find_element_by_xpath(dmhp.el_right_security).text == "文档域管理"
            assert driver.find_element_by_xpath(dmhp.el_left_Operations).text == "文档域管理"
        # except Exception:
        #
        #     Domain_mgnt_home_page(driver).close_windows()
        #     raise

    @allure.step("添加21个平级域")
    @pytest.fixture(scope="function")
    def add_parallel_domain(self, request, get_domain):
        host = request.config.getoption(name="--host")
        host = host.split('//')[1].split(':')[0]
        f_domain = get_domain["father_domain"]
        CommonDocDomain().addRelationDomain(httphost=host,
                                            host=["10.2.190.1", "10.2.190.2", "10.2.190.3", "10.2.190.4",
                                                  "10.2.190.5", "10.2.190.6", "10.2.190.7", "10.2.190.8",
                                                  "10.2.190.9", "10.2.190.10", "10.2.190.11", "10.2.190.12",
                                                  "10.2.190.13", "10.2.190.14", "10.2.190.15", "10.2.190.16",
                                                  "10.2.190.17", "10.2.190.18", "10.2.190.19", "10.2.190.20",
                                                  "10.2.190.21"], domaintype="parallel", network_type="indirect")
        yield
        CommonDocDomain().clearRelationDomain(host=host)

    @pytest.mark.gwp
    @pytest.mark.high
    @allure.testcase("5441,文档域管理--删除文档域--成功 ")
    def test_del_domain_success(self, add_parallel_domain, driver):
        # try:
            dmp = Domain_mgnt_page(driver=driver)
            dmhp = Domain_mgnt_home_page(driver=driver)
            dmhp.return_domain_home_page()
            time.sleep(2)
            driver.find_element_by_xpath(dmhp.el_policy_sync).click()
            time.sleep(2)
            driver.find_element_by_css_selector(dmhp.el_domain_mgnt).click()
            time.sleep(1)
            driver.find_element_by_xpath(dmp.el_next_page_icon).click()
            el = WebDriverWait(driver, 20).until(
                ec.visibility_of_element_located((By.XPATH, dmp.el_list_domain_name + "[text()='10.2.190.9']")))
            assert el.text == "10.2.190.9"
            count = WebDriverWait(driver, 20).until(ec.visibility_of_element_located((By.XPATH, dmp.el_page_count)))
            assert count.text == "显示 21 - 21 条，共 21 条"
            value = driver.find_element_by_xpath(dmp.el_page_input).get_attribute("value")
            assert value == "2"
            dmp.delete_domain(index=1)
            time.sleep(2)
            count = WebDriverWait(driver, 20).until(ec.visibility_of_element_located((By.XPATH, dmp.el_page_count)))
            # print(count.text)
            assert count.text == "显示 1 - 20 条，共 20 条"
            value = driver.find_element_by_xpath(dmp.el_page_input).get_attribute("value")
            assert value == "1"
        # except Exception:
        #
        #     Domain_mgnt_home_page(driver).close_windows()
        #     raise


class Test_edit_domain:
    """
        编辑文档域
        """

    @allure.step("添加文档域")
    @pytest.fixture(scope="function")
    def add_domain(self, driver):
        dmp = Domain_mgnt_page(driver=driver)
        dmhp = Domain_mgnt_home_page(driver=driver)
        dmhp.return_domain_home_page()
        time.sleep(2)
        driver.find_element_by_xpath(dmhp.el_policy_sync).click()
        time.sleep(2)
        driver.find_element_by_css_selector(dmhp.el_domain_mgnt).click()
        dmp.add_domain(domain_name="parallel.eisoo.cn", appid="app_id", appkey="app_key", domain_type="child")
        yield
        dmp.delete_domain(index=1)
        time.sleep(2)

    @pytest.mark.gwp
    @pytest.mark.high
    @allure.testcase("5886,文档域管理--编辑域失败--端口错误")
    def test_edit_domain_defeated(self, driver, add_domain):
        # try:
            dmp1 = Domain_mgnt_page(driver=driver)
            time.sleep(1)
            dmp1.edit_domain(domain_name="parallel.eisoo.cn", port="4444")
            assert driver.find_element_by_xpath(dmp1.el_domain_added_warn_comm).text.strip(" ") == "编辑失败，指定的文档域无法连接。"
            driver.find_element_by_css_selector(dmp1.el_cancel).click()
            time.sleep(1)
        # except Exception:
        #
        #     Domain_mgnt_home_page(driver).close_windows()
        #     raise


class Test_del_domain:
    """
    删除文档域
    """

    @allure.step("添加文档域")
    @pytest.fixture(scope="function")
    def add_domain(self, driver, get_domain):
        f_domain = get_domain["replace_domain"]
        dmp = Domain_mgnt_page(driver=driver)
        dmhp = Domain_mgnt_home_page(driver=driver)
        dmhp.return_domain_home_page()
        time.sleep(2)
        driver.find_element_by_xpath(dmhp.el_policy_sync).click()
        time.sleep(2)
        driver.find_element_by_css_selector(dmhp.el_domain_mgnt).click()
        dmp.add_domain(domain_name=f_domain, appid="app_id", appkey="app_key", domain_type="child")
        yield f_domain
        dmp.delete_domain()

    @allure.step("添加文档域")
    @pytest.fixture(scope="function")
    def edit_domain_port(self, driver, add_domain):
        # try:
            dmp = Domain_mgnt_page(driver=driver)
            dmp.edit_domain(domain_name=add_domain, port="8000")
            yield
            dmp.edit_domain(domain_name=add_domain, port="443")
        # except Exception :
        #
        #     Domain_mgnt_home_page(driver).close_windows()
        #     raise

    @pytest.mark.gwp
    @pytest.mark.high
    @allure.testcase("5885,文档域管理--删除子域--目标域连接失败")
    def test_del_domain_defeated(self, driver, edit_domain_port):
        """

        :param driver:
        :param edit_domain_port:
        :return:
        """
        # try:
        dmp1 = Domain_mgnt_page(driver=driver)
        dmp1.delete_domain()
        del_failed_text = driver.find_element_by_xpath(dmp1.el_delete_link_failed).text
        assert del_failed_text == "删除失败，指定的文档域无法连接。"
        driver.find_element_by_xpath(dmp1.el_delete_confirm).click()
        assert WebDriverWait(driver, timeout=10.0).until(
            ec.invisibility_of_element_located((By.XPATH, dmp1.el_delete_domain_title)))
        # except Exception:
        #
        #     Domain_mgnt_home_page(driver).close_windows()
        #     raise

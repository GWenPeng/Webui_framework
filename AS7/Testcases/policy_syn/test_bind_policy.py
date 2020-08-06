from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from AS7.Pages.Domain_mgnt.domain_mgnt_home_page import Domain_mgnt_home_page
from AS7.Pages.Domain_mgnt.domain_mgnt_page import Domain_mgnt_page
from AS7.Pages.Domain_mgnt.doc_policy_page import doc_policy_page
from AS7.Pages.Login_page import Login_page
from AS7.Pages.Domain_mgnt.CommonDocDomain import CommonDocDomain
from Common.mysqlconnect import DB_connect
from Common.screenshot import ScreenShot
import time
import allure
import pytest


class TestBindPolicy(object):

    @pytest.fixture(scope="function")
    def clear_policy(self, request,get_domain,driver):
        url = request.config.getoption(name="--host")
        host = url.split('//')[1].split(':')[0]
        DB_connect(dbname="db_domain_self", host=host).delete("DELETE FROM `t_policy_tpl_domains`")
        Domain_mgnt_home_page(driver).return_domain_home_page()
        domain_mgnt = Domain_mgnt_page(driver)
        host1 = get_domain["replace_domain"]
        domain_mgnt.add_domain(domain_name=host1, appid="1", appkey="1", domain_type="child")
        WebDriverWait(driver, 30).until(ec.invisibility_of_element_located((By.XPATH, domain_mgnt.el_add_domain_title)))
        Domain_mgnt_home_page(driver).policy_sync()
        yield
        uuid = DB_connect(dbname="db_domain_self", host=host).select_one(
                "select * FROM `t_policy_tpl_domains` LIMIT 1")
        policy_id = DB_connect(dbname="db_domain_self", host=host).select_one(
                "SELECT f_id FROM `t_policy_tpls`")
        if uuid is not None:
            status_code = CommonDocDomain().delboundPolicy(httphost=host, PolicyUUID=uuid[0], ChildDomainUUID=uuid[1])
            assert status_code == 200
        if policy_id is not None:
            DB_connect(dbname="db_domain_self", host=host).delete("DELETE FROM `t_policy_tpls`")
        CommonDocDomain().clearRelationDomain(host=host)
        CommonDocDomain().set_auth_login(httphost=host1)
        time.sleep(3)
        driver.get(url)
        Login_page(driver).login(username="admin", password="eisoo.com")

    @allure.testcase("5769 文档域策略同步--子域解绑策略--子域配置策略")
    @pytest.mark.medium
    @pytest.mark.high
    def test_unbind_policy(self, driver, request, clear_policy, get_domain):
        doc_policy = doc_policy_page(driver)
        host = get_domain["replace_domain"]
        # try:
        doc_policy.add_policy_with_auth(policy_name="上海爱数安全配置", enable=True, option="账号密码 + 图形验证码")
        doc_policy.apply_domain(domain_name=host)
        time.sleep(5)
        DB_connect(dbname="sharemgnt_db", host=host).delete("DELETE FROM `t_vcode`")
        driver.get(f'https://{host}:8000')
        Login_page(driver).login(username="admin", password="eisoo.com", host=host)
        time.sleep(3)
        driver.find_element_by_xpath(doc_policy.el_security_tab).click()
        WebDriverWait(driver, 20).until(ec.visibility_of_element_located((By.XPATH, doc_policy.el_login_auth)))
        time.sleep(3)
        assert driver.find_element_by_xpath(doc_policy.el_login_auth).text == "账号密码 + 图形验证码"
        assert driver.find_element_by_xpath(doc_policy.el_control_wrong_password).get_attribute("value") == "0"
        assert doc_policy.attribute_is_present(xpath=doc_policy.el_control_wrong_password,attribute="disabled") is True
        # 解绑文档域
        url = request.config.getoption(name="--host")
        host1 = url.split('//')[1].split(':')[0]
        uuid = DB_connect(dbname="db_domain_self", host=host1).select_one(
            "select * FROM `t_policy_tpl_domains` LIMIT 1")
        CommonDocDomain().delboundPolicy(httphost=host1, PolicyUUID=uuid[0], ChildDomainUUID=uuid[1])
        driver.refresh()
        WebDriverWait(driver,20).until(ec.visibility_of_element_located((By.XPATH,doc_policy.el_login_auth)))
        time.sleep(5)
        assert driver.find_element_by_xpath(doc_policy.el_control_wrong_password).is_enabled() is True
        # except Exception:
        #
        #     raise

    @allure.testcase("5967  配置策略--设置账号密码+动态密码登录")
    @pytest.mark.high
    @pytest.mark.gfr
    def test_restrict_client_login(self,driver,clear_policy,get_domain):
        doc_policy = doc_policy_page(driver)
        host = get_domain["replace_domain"]
        doc_policy.add_policy_with_auth(policy_name="上海爱数安全配置", enable=True, option="账号密码 + 动态密码")
        doc_policy.apply_domain(domain_name=host)
        time.sleep(5)
        driver.get(f'https://{host}')
        driver.implicitly_wait(30)
        driver.maximize_window()
        el_dynamic_pwd_input = "input[placeholder='请输入动态密码']"
        WebDriverWait(driver,20).until(ec.invisibility_of_element_located((By.XPATH,el_dynamic_pwd_input)))
        driver.get(f'https://{host}:8000')
        Login_page(driver).login(username="admin", password="eisoo.com")
        time.sleep(5)
        driver.find_element_by_xpath(doc_policy.el_security_tab).click()
        WebDriverWait(driver, 20).until(ec.visibility_of_element_located((By.XPATH, doc_policy.el_login_auth)))
        time.sleep(3)
        assert driver.find_element_by_xpath(doc_policy.el_login_auth).text == "账号密码 + 动态密码"







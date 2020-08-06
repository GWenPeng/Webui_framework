# coding=utf-8
from AS7.Pages.Domain_mgnt.CommonDocDomain import CommonDocDomain
from AS7.Pages.Domain_mgnt.doc_policy_page import doc_policy_page
from AS7.Pages.Domain_mgnt.domain_mgnt_home_page import Domain_mgnt_home_page
from AS7.Pages.Domain_mgnt.domain_mgnt_page import Domain_mgnt_page
from AS7.Pages.Login_page import Login_page
from Common.mysqlconnect import DB_connect
from Common.parse_data import do_excel
from Common.screenshot import ScreenShot
from Common.thrift_client import Thrift_client
from ShareMgnt import ncTShareMgnt
import pytest
import time
import allure


@pytest.mark.wq_suite
class TestSetPolicy:
    @allure.step("清除数据")
    @pytest.fixture(scope="function")
    def clear_data(self, driver, get_domain):
        Domain_mgnt_home_page(driver).return_domain_home_page()
        host = get_domain["replace_domain"]
        Domain_mgnt_page(driver).add_domain(domain_name=host, appid='11', appkey='22')
        yield
        # 删除子域
        Domain_mgnt_home_page(driver=driver).return_domain_home_page()
        time.sleep(3)
        Domain_mgnt_page(driver).delete_domain_by_name(domain_name=host)
        # 重置密码强度和客户端登录方式
        code = CommonDocDomain().set_password_str(httphost=host)
        assert code == 200
        code = CommonDocDomain().set_clientLogin_Options(httphost=host)
        assert code == 200
        code = CommonDocDomain().set_auth_login(httphost=host)
        assert code == 200

    @allure.testcase("caseid: 5571/5612--文档域策略同步--配置强密码登录策略策略--子域登录")
    def test_set_password_policy(self, driver, get_domain, clear_data):
        # try:
        el_policy = doc_policy_page(driver)
        host = get_domain["replace_domain"]
        Domain_mgnt_home_page(driver).policy_sync()  # 进入策略同步页面
        data = do_excel(filename='add_policy.xlsx', sheetname='策略配置', minrow=2, maxrow=2, mincol=1, maxcol=4)[0]
        print(data)
        el_policy.add_policy(policy_name=data[0], item=data[1], enable=data[2], strength='strong', length=data[3])
        el_policy.apply_domain(domain_name=host)
        time.sleep(2)
        d_new_name = el_policy.get_apply_domain_info()
        assert d_new_name == host
        # 断言强密码策略已成功应用至子域
        tc = Thrift_client(ncTShareMgnt, host=host, port="9600")
        response = tc.client.Usrm_GetPasswordConfig()
        print(response)
        assert response.strongPwdLength == 18
        el_policy.unbind_domain(domain_name=host)  # 解绑文档域
        time.sleep(3)
        el_policy.delete_policy(policy_name=data[0])  # 删除策略

    # except Exception:
    #
    #     Domain_mgnt_home_page(driver).close_windows()
    #     raise

    @allure.testcase("caseid: 5613--文档域策略同步--设置限制客户端登录--用户登录")
    @pytest.mark.high
    def test_set_restricted_client_login(self, driver, get_domain, clear_data):
        # try:
        host = get_domain["replace_domain"]
        Domain_mgnt_home_page(driver).policy_sync()  # 进入策略同步页面
        data = do_excel(filename='add_policy.xlsx', sheetname='策略配置', minrow=3, maxrow=3, mincol=1, maxcol=5)[0]
        print(data)
        el_policy = doc_policy_page(driver)
        el_policy.add_policy(policy_name=data[0], item=data[1], enable=data[2], options=data[4])  # 限制Web客户端登录
        el_policy.apply_domain(domain_name=host)
        d_new_name = el_policy.get_apply_domain_info()
        time.sleep(2)
        assert d_new_name == host
        tc = Thrift_client(ncTShareMgnt, host=host, port="9600")
        response = tc.client.GetAllOSTypeForbidLoginInfo()
        print(response)
        assert response[0].osType == 5  # 断言 限制web & android & mobile & ios客户端登录
        el_policy.unbind_domain(domain_name=host)  # 解绑文档域
        time.sleep(3)
        el_policy.delete_policy(policy_name=data[0])  # 删除策略

    # except Exception:
    #
    #     Domain_mgnt_home_page(driver).close_windows()
    #     raise

    @allure.testcase("caseid: 5573--配置策略--设置账号密码+图形验证码--子域登录")
    @allure.testcase("caseid: 5615--文档域策略同步--设置账号密码+图形验证码--登录")
    @pytest.mark.high
    def test_set_pwd_graphiccode_login(self, driver, request, get_domain, clear_data):
        # try:
        host = get_domain["replace_domain"]
        policy_page = doc_policy_page(driver)
        el_login = Login_page(driver)
        Domain_mgnt_home_page(driver).policy_sync()
        policy_page.add_policy_with_auth(policy_name="登录策略", enable=True, option="账号密码 + 图形验证码")
        policy_page.apply_domain(domain_name=host)
        time.sleep(5)
        DB_connect(dbname="sharemgnt_db", host=host).delete("DELETE FROM `t_vcode`")
        driver.get(f'https://{host}:8000')
        # 图形验证码输入为空
        Login_page(driver).login(username='admin', password='eisoo.com')
        # el_hint = "//div[text()='管理控制台']/../div[3]/div[2]"
        # el_hint_text = driver.find_element_by_xpath(el_hint).text
        # assert el_hint_text == "验证码不能为空，请重新输入。"
        # time.sleep(3)
        # # 输入正确的图形验证码
        # # f_vode = DB_connect(dbname="sharemgnt_db", host=host).select_one("SELECT f_vcode FROM `t_vcode` limit 1")
        # # time.sleep(3)
        # #         # print(f_vode[0])
        # #         # driver.find_element_by_css_selector(el_login.el_vcode).send_keys(f_vode[0])
        # time.sleep(2)
        # el_confirm = driver.find_element_by_css_selector(el_login.el_submit)
        # el_confirm.click()
        time.sleep(3)
        driver.find_element_by_xpath(policy_page.el_security_tab).click()  # 进入安全管理页面
        time.sleep(3)
        option = driver.find_element_by_xpath(policy_page.el_login_auth).text
        option_status = driver.find_element_by_xpath(
            "//span[text()='设置用户必须通过']/following-sibling::span[1]/span[1]").get_attribute('class')
        assert option == "账号密码 + 图形验证码"
        assert option_status.split("-")[-1] == 'disabled'
        url = request.config.getoption(name="--host")
        driver.get(url)
        Login_page(driver).login(username="admin", password="eisoo.com")
        Domain_mgnt_home_page(driver=driver).return_domain_home_page()
        Domain_mgnt_home_page(driver).policy_sync()
        time.sleep(2)
        policy_page.unbind_domain(domain_name=host)  # 解绑文档域
        time.sleep(2)
        policy_page.delete_policy(policy_name="登录策略")  # 删除策略
        time.sleep(2)
    # except Exception:
    #
    #     Domain_mgnt_home_page(driver).close_windows()
    #     raise

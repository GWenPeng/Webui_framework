# coding=utf-8
from AS7.Pages.Domain_mgnt.CommonDocDomain import CommonDocDomain
from AS7.Pages.Domain_mgnt.domain_mgnt_home_page import Domain_mgnt_home_page
from AS7.Pages.Domain_mgnt.domain_mgnt_page import Domain_mgnt_page
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from AS6.Pages.Login_page import Login_page
from Common.mysqlconnect import DB_connect
from Common.screenshot import ScreenShot
from Common.parse_data import do_excel
from Common.readConfig import readconfigs
import pytest
import allure
import time


class TestAddDomain:

    @allure.testcase("5697 文档域管理--添加子域(该域无子域)--添加成功")
    @pytest.mark.high
    @pytest.mark.gfr
    def test_add_domain_success(self, driver, get_domain):
        Domain_mgnt_home_page(driver).return_domain_home_page()
        domain_mgnt = Domain_mgnt_page(driver)
        host = get_domain["parallel_domain"]
        domain_mgnt.add_domain(domain_name=host, appid='1', appkey='1')
        WebDriverWait(driver, 10).until(ec.invisibility_of_element_located((By.XPATH, domain_mgnt.el_add_domain_title)))
        info = domain_mgnt.get_domain_info()
        assert info == [host, "子域", "直连", "---"]
        domain_mgnt.delete_domain()

    @allure.testcase("5846 文档域管理--添加子域--网络连接失败")
    @pytest.mark.high
    @pytest.mark.gfr
    def test_add_domain_fail(self, driver):
        info = do_excel(filename="domain_mgnt.xlsx", sheetname="提示信息", minrow=1, maxrow=1, mincol=2, maxcol=2)[0]
        Domain_mgnt_home_page(driver).return_domain_home_page()
        domain_mgnt = Domain_mgnt_page(driver)
        domain_mgnt.add_domain(domain_name="10.2.64.9", appid='1', appkey='1')
        # WebDriverWait(driver, 200).until(ec.visibility_of_element_located((By.XPATH, domain_mgnt.el_connection_tip)))
        time.sleep(60)
        text = driver.find_element_by_xpath(domain_mgnt.el_connection_fail).text
        assert text == info[0]
        driver.find_element_by_css_selector(domain_mgnt.el_cancel).click()
        WebDriverWait(driver, 10).until(ec.invisibility_of_element_located((By.XPATH, domain_mgnt.el_add_domain_title)))

    @allure.testcase("5850 文档域管理--添加平级域失败--直连模式")
    @pytest.mark.high
    @pytest.mark.gfr
    def test_add_parallel_fail(self, driver):
        info = do_excel(filename="domain_mgnt.xlsx", sheetname="提示信息", minrow=1, maxrow=1, mincol=2, maxcol=2)[0]
        Domain_mgnt_home_page(driver).return_domain_home_page()
        domain_mgnt = Domain_mgnt_page(driver)
        domain_mgnt.add_domain(domain_name="10.2.64.9", domain_type="parallel", direct_mode=True, appid='1',
                               appkey='1')
        # WebDriverWait(driver, 200).until(ec.visibility_of_element_located((By.XPATH, domain_mgnt.el_connection_tip)))
        time.sleep(60)
        text = driver.find_element_by_xpath(domain_mgnt.el_connection_fail).text
        assert text == info[0]
        driver.find_element_by_css_selector(domain_mgnt.el_cancel).click()
        WebDriverWait(driver, 10).until(ec.invisibility_of_element_located((By.XPATH, domain_mgnt.el_add_domain_title)))

    @allure.step("设置本域类型为子域")
    @pytest.fixture(scope="function")
    def set_self_child_domain(self, get_domain, request, driver):
        host = request.config.getoption(name="--host")
        host = host.split('//')[1].split(':')[0]
        uuid = CommonDocDomain().addRelationDomain(httphost=get_domain["father_domain"], host=host)
        yield
        CommonDocDomain().delRelationDomain(host=get_domain["father_domain"], uuid=uuid)

    @allure.step("设置本域为父域")
    @pytest.fixture(scope="function")
    def set_self_father_domain(self, get_domain, request, driver):
        host = request.config.getoption(name="--host")
        host = host.split('//')[1].split(':')[0]
        uuid = CommonDocDomain().addRelationDomain(httphost=host, host=get_domain["parallel_domain"])
        yield
        CommonDocDomain().delRelationDomain(host=host, uuid=uuid)

    @allure.step("设置本域为平级域")
    @pytest.fixture(scope="function")
    def set_self_parallel_domain(self, get_domain, request, ):
        host = request.config.getoption(name="--host")
        host = host.split('//')[1].split(':')[0]
        ip = get_domain["father_domain"]
        uuid = CommonDocDomain().addRelationDomain(httphost=ip, domaintype="parallel", host=host)
        yield
        CommonDocDomain().delRelationDomain(host=ip, uuid=uuid)

    @allure.testcase("5673 文档域管理--添加平级域--成功(当前域无身份)")
    @pytest.mark.high
    @pytest.mark.gfr
    def test_add_parallel_success(self, driver, get_domain):
        Domain_mgnt_home_page(driver).return_domain_home_page()
        domain_mgnt = Domain_mgnt_page(driver)
        hosts = [get_domain["parallel_domain"], get_domain["child_domain"], get_domain["father_domain"]]
        for host in hosts:
            domain_mgnt.add_domain(domain_name=host, domain_type="parallel", direct_mode=True, appid='1', appkey='1')
            WebDriverWait(driver, 10).until(
                ec.invisibility_of_element_located((By.XPATH, domain_mgnt.el_add_domain_title)))
            info = domain_mgnt.get_domain_info()
            assert info == [host, "平级域", "直连", "---"]
            domain_mgnt.delete_domain()

    @allure.testcase("5673 文档域管理--添加平级域--成功(当前域为父域)")
    @pytest.mark.high
    @pytest.mark.gfr
    def test_add_parallel_success_father(self, driver, get_domain, set_self_father_domain):
        Domain_mgnt_home_page(driver).return_domain_home_page()
        domain_mgnt = Domain_mgnt_page(driver)
        host = get_domain["replace_domain"]
        domain_mgnt.add_domain(domain_name=host, domain_type="parallel", direct_mode=True, appid='1', appkey='1')
        WebDriverWait(driver, 10).until(
            ec.invisibility_of_element_located((By.XPATH, domain_mgnt.el_add_domain_title)))
        info = domain_mgnt.get_domain_info()
        assert info == [host, "平级域", "直连", "---"]
        domain_mgnt.delete_domain_by_name(domain_name=host)

    @allure.testcase("5673 文档域管理--添加平级域--成功(当前域为子域)")
    @pytest.mark.high
    @pytest.mark.gfr
    def test_add_parallel_success_child(self, driver, get_domain, set_self_child_domain):
        Domain_mgnt_home_page(driver).return_domain_home_page()
        domain_mgnt = Domain_mgnt_page(driver)
        host = get_domain["replace_domain"]
        domain_mgnt.add_domain(domain_name=host, domain_type="parallel", direct_mode=True, appid='1', appkey='1')
        WebDriverWait(driver, 10).until(
            ec.invisibility_of_element_located((By.XPATH, domain_mgnt.el_add_domain_title)))
        info = domain_mgnt.get_domain_info()
        assert info == [host, "平级域", "直连", "---"]
        domain_mgnt.delete_domain_by_name(domain_name=host)

    @allure.testcase("5673 文档域管理--添加平级域--成功(当前域平级域)")
    @pytest.mark.high
    @pytest.mark.gfr
    def test_add_parallel_success_parallel(self, driver, get_domain, set_self_parallel_domain):
        Domain_mgnt_home_page(driver).return_domain_home_page()
        domain_mgnt = Domain_mgnt_page(driver)
        host = get_domain["replace_domain"]

        domain_mgnt.add_domain(domain_name=host, domain_type="parallel", direct_mode=True, appid='1', appkey='1')
        WebDriverWait(driver, 10).until(
            ec.invisibility_of_element_located((By.XPATH, domain_mgnt.el_add_domain_title)))
        info = domain_mgnt.get_domain_info()
        assert info == [host, "平级域", "直连", "---"]
        domain_mgnt.delete_domain_by_name(domain_name=host)

    @allure.testcase("5851 文档域管理--列表页面")
    @pytest.mark.normal
    @pytest.mark.zyl
    def test_null_domain(self, driver):
        # try:
            Domain_mgnt_home_page(driver).return_domain_home_page()
            domain_mgnt = Domain_mgnt_page(driver)
            WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.XPATH, domain_mgnt.el_list_is_null)))
            list_Info = driver.find_element_by_xpath(domain_mgnt.el_list_is_null).text
            assert list_Info == "列表为空"
        # except Exception:
        #
        #     raise

    @allure.testcase("5360 文档域管理--添加子域(该域无身份)--添加成功")
    @pytest.mark.high
    @pytest.mark.zyl
    def test_Add_domain_tip(self, driver, get_domain):
        # try:
            Domain_mgnt_home_page(driver).return_domain_home_page()
            domain_mgnt = Domain_mgnt_page(driver)
            tip = do_excel(filename="add_domain.xlsx", sheetname="提示语",
                           minrow=4, maxrow=5, mincol=2, maxcol=2)
            domain_mgnt.add_domain(domain_name='1.1.1.1', appid='1', appkey='1')
            connection_tip = driver.find_element_by_xpath(domain_mgnt.el_connection_tip).text
            WebDriverWait(driver, 30).until(ec.visibility_of_element_located((By.XPATH, domain_mgnt.el_connection_fail)))
            connection_fail = driver.find_element_by_xpath(domain_mgnt.el_connection_fail).text
            driver.find_element_by_css_selector(domain_mgnt.el_cancel).click()
            host = get_domain["parallel_domain"]
            domain_mgnt.add_domain(domain_name=host, appid='1', appkey='1')
            WebDriverWait(driver, 10).until(ec.invisibility_of_element_located((By.XPATH, domain_mgnt.el_add_domain_title)))
            info = domain_mgnt.get_domain_info()
            domain_mgnt.delete_domain()
            assert info == [host, "子域", "直连", "---"]
            assert tip[0][0] in connection_tip
            assert connection_fail == tip[1][0]
        # except Exception:
        #
        #     raise

    @allure.testcase("5433 文档域管理--删除文档域--已设置策略同步")
    @pytest.mark.high
    @pytest.mark.zyl
    def test_delete_domain(self, driver, get_domain, request):
        # try:
            host = request.config.getoption(name="--host")
            host = host.split('//')[1].split(':')[0]
            childhost = get_domain["parallel_domain"]
            # 策略绑定文档域
            policyuuid = CommonDocDomain().addPolicy(httphost=host, name="上海爱数安全策略")
            addDomainuuid = CommonDocDomain().addRelationDomain(host=childhost, httphost=host)
            CommonDocDomain().BoundPolicy(httphost=host, PolicyUUID=policyuuid, ChildDomainUUID=addDomainuuid)
            Domain_mgnt_home_page(driver).policy_sync()  # 进入策略同步
            Domain_mgnt_home_page(driver).return_domain_home_page()
            domain_mgnt = Domain_mgnt_page(driver)
            tip = do_excel(filename="add_domain.xlsx", sheetname="提示语",
                           minrow=9, maxrow=9, mincol=2, maxcol=2)
            driver.find_element_by_css_selector(domain_mgnt.el_delete_button).click()
            delete_tip = driver.find_element_by_xpath(domain_mgnt.el_delete_tip).text
            driver.find_element_by_xpath(domain_mgnt.el_delete_confirm)
            domainInfo = domain_mgnt.get_domain_info()
            # 清除策略绑定文档域
            CommonDocDomain().delboundPolicy(httphost=host, PolicyUUID=policyuuid, ChildDomainUUID=addDomainuuid)
            CommonDocDomain().deletepolicy(httphost=host, PolicyUUID=policyuuid)
            CommonDocDomain().delRelationDomain(host=host, uuid=addDomainuuid)
            time.sleep(2)
            assert delete_tip == tip[0][0]
            assert domainInfo == [childhost, '子域', '直连', '上海爱数安全策略']
        # except Exception:
        #
        #     raise

    @allure.testcase("6653 文档域管理--解除绑定--文档域连接失败")
    @pytest.mark.high
    @pytest.mark.zyl
    def test_unbind_domain_failed(self, driver, get_domain, request):
        # try:
            host = request.config.getoption(name="--host")
            host = host.split('//')[1].split(':')[0]
            childhost = get_domain["parallel_domain"]
            # 策略绑定文档域
            policyuuid = CommonDocDomain().addPolicy(httphost=host, name="上海爱数安全策略")
            addDomainuuid = CommonDocDomain().addRelationDomain(host=childhost, httphost=host)
            CommonDocDomain().BoundPolicy(httphost=host, PolicyUUID=policyuuid, ChildDomainUUID=addDomainuuid)
            Domain_mgnt_home_page(driver).policy_sync()  # 进入策略同步
            Domain_mgnt_home_page(driver).return_domain_home_page()
            domain_mgnt = Domain_mgnt_page(driver)
            tip = do_excel(filename="add_domain.xlsx", sheetname="提示语",
                           minrow=10, maxrow=11, mincol=2, maxcol=2)
            connect = DB_connect(host=host)
            sql = "update domain_mgnt.t_relationship_domain set f_host='1.1.1.1' where f_domain_type='child'"
            connect.update(sql)
            driver.find_element_by_xpath(domain_mgnt.el_untie_policy).click()
            WebDriverWait(driver, 30).until(ec.visibility_of_element_located((By.XPATH, domain_mgnt.el_untie_tip)))
            delete_tip = driver.find_element_by_xpath(domain_mgnt.el_untie_tip).text  # 解绑文档域提示
            driver.find_element_by_xpath(domain_mgnt.el_delete_confirm).click()
            WebDriverWait(driver, 30).until(ec.visibility_of_element_located((By.XPATH, domain_mgnt.el_untie_filed)))
            Unbind_tip = driver.find_element_by_xpath(domain_mgnt.el_untie_filed).text  # 获取解绑失败弹框提示
            driver.find_element_by_xpath(domain_mgnt.el_delete_confirm).click()
            sql = "update domain_mgnt.t_relationship_domain set f_host='{}' where f_domain_type='child'"
            updatesql = sql.format(childhost)
            connect.update(updatesql)
            time.sleep(2)
            # 清除策略绑定文档域
            CommonDocDomain().delboundPolicy(httphost=host, PolicyUUID=policyuuid, ChildDomainUUID=addDomainuuid)
            CommonDocDomain().deletepolicy(httphost=host, PolicyUUID=policyuuid)
            CommonDocDomain().delRelationDomain(host=host, uuid=addDomainuuid)
            Domain_mgnt_home_page(driver).policy_sync()  # 进入策略同步
            Domain_mgnt_home_page(driver).return_domain_home_page()
            time.sleep(2)
            assert delete_tip == tip[0][0]
            assert Unbind_tip == tip[1][0]
        # except Exception:
        #
        #     raise

    @pytest.fixture(scope='function')
    def add_parallel(self, request, get_domain, driver):
        host = request.config.getoption(name="--host")
        host = host.split('//')[1].split(':')[0]
        child_uuid = CommonDocDomain().addRelationDomain(httphost=host, host=get_domain["replace_domain"])
        parallel_uuid = CommonDocDomain().addRelationDomain(httphost=host, host=get_domain["parallel_domain"],
                                                            domaintype="parallel")
        yield
        CommonDocDomain().delRelationDomain(host=host, uuid=child_uuid)
        CommonDocDomain().delRelationDomain(host=host, uuid=parallel_uuid)
        Domain_mgnt_home_page(driver).policy_sync()
        Domain_mgnt_home_page(driver).return_domain_home_page()
        time.sleep(4)

    @allure.testcase("5674 文档域管理--添加平级域--重复添加")
    @pytest.mark.high
    @pytest.mark.gfr
    def test_repeat_to_add_parallel(self, driver, get_domain, add_parallel):
        # try:
            Domain_mgnt_home_page(driver).return_domain_home_page()
            domain_mgnt = Domain_mgnt_page(driver)
            domains = [get_domain["replace_domain"], get_domain["parallel_domain"]]
            tip = do_excel(filename="add_domain.xlsx", sheetname="提示语",
                           minrow=12, maxrow=12, mincol=2, maxcol=2)
            for host in domains:
                domain_mgnt.add_domain(domain_name=host, domain_type="parallel")
                WebDriverWait(driver, 20).until(
                    ec.visibility_of_element_located((By.XPATH, domain_mgnt.el_error_msg_repet)))
                driver.find_element_by_xpath(domain_mgnt.el_error_msg_repet).text == tip[0][0]
                driver.find_element_by_css_selector(domain_mgnt.el_cancel).click()
                WebDriverWait(driver, 20).until(
                    ec.invisibility_of_element_located((By.XPATH, domain_mgnt.el_add_domain_title)))
        # except Exception:
        #
        #     raise

    @allure.testcase("5414 文档域管理--列表检查")
    @pytest.mark.normal
    @pytest.mark.zyl
    def test_domains_list(self, driver, get_domain):
        # try:
            Domain_mgnt_home_page(driver).return_domain_home_page()
            domain_mgnt = Domain_mgnt_page(driver)
            time.sleep(2)
            domain_title = domain_mgnt.get_title_info()
            host = get_domain["parallel_domain"]
            domain_mgnt.add_domain(domain_name=host, appid='1', appkey='1')
            WebDriverWait(driver, 10).until(ec.invisibility_of_element_located((By.XPATH, domain_mgnt.el_add_domain_title)))
            info = domain_mgnt.get_domain_info()
            domain_mgnt.delete_domain()
            # 添加平级域直连模式
            domain_mgnt.add_domain(domain_name=host, domain_type='parallel', direct_mode=False, is_submit=True)
            WebDriverWait(driver, 30).until(
                ec.visibility_of_element_located((By.XPATH, domain_mgnt.el_edit_domain)))
            parallel_info = domain_mgnt.get_domain_info()
            domain_mgnt.delete_domain()
            assert domain_title == ['域名', '域类型', '连接方式', '策略配置', '操作']
            assert info == [host, "子域", "直连", "---"]
            assert parallel_info == [host, "平级域", "非直连", "---"]
        # except Exception:
        #
        #     raise

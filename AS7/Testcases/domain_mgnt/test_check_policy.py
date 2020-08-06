from AS7.Pages.Domain_mgnt.domain_mgnt_home_page import Domain_mgnt_home_page
from AS7.Pages.Domain_mgnt.domain_mgnt_page import Domain_mgnt_page
from AS7.Pages.Domain_mgnt.CommonDocDomain import CommonDocDomain
from AS7.Pages.Domain_mgnt.doc_policy_page import doc_policy_page
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from Common.screenshot import ScreenShot
import pytest
import allure
import time


class Test_check_policy:
    @pytest.fixture(scope="function")
    def set_child_domain(self, driver, get_domain, request):
        host = request.config.getoption(name="--host")
        host = host.split('//')[1].split(':')[0]
        # 新增策略
        policyuuid = CommonDocDomain().addPolicy(httphost=host, name="上海爱数安全策略ni")
        # 当前域添加replace_domain为子域
        domainuuid = CommonDocDomain().addRelationDomain(httphost=host, host=get_domain["replace_domain"])
        CommonDocDomain().BoundPolicy(httphost=host, PolicyUUID=policyuuid, ChildDomainUUID=domainuuid)
        yield
        CommonDocDomain().delboundPolicy(httphost=host, PolicyUUID=policyuuid, ChildDomainUUID=domainuuid)
        CommonDocDomain().deletepolicy(httphost=host, PolicyUUID=policyuuid)
        CommonDocDomain().delRelationDomain(host=host, uuid=domainuuid)
        # 增加刷新，回到文档域管理界面
        driver.find_element_by_xpath("//a[span[text()='组织管理']]").click()
        Domain_mgnt_home_page(driver=driver).return_domain_home_page()

    @allure.testcase("caseid:5502  策略同步--策略配置列表项检查（父域登录）")
    @pytest.mark.ni
    @pytest.mark.normal
    def test_check_fatherdomain_poliystatus(self, driver, get_domain, set_child_domain):
        # try:
            driver.find_element_by_xpath("//a[span[text()='组织管理']]").click()
            Domain_mgnt_home_page(driver=driver).return_domain_home_page()
            Domain_mgnt_home_page(driver=driver).policy_sync()
            dpg = doc_policy_page(driver)
            WebDriverWait(driver, 60).until(
                ec.visibility_of_element_located((By.XPATH, dpg.el_policy_first)))
            # 获取策略首行名称
            words = dpg.get_policy_info()
            assert words == "上海爱数安全策略ni"
            # 判断[编辑]按钮一直可用
            WebDriverWait(driver, 60).until(
                ec.visibility_of_element_located((By.XPATH, dpg.el_edit_policy_enable)))
            edit_button = driver.find_element_by_xpath(dpg.el_edit_policy_enable).get_attribute("class")
            assert edit_button.split("-")[-1] != "disabled"
            # 判断[删除]按钮一直可用
            WebDriverWait(driver, 60).until(
                ec.visibility_of_element_located((By.XPATH, dpg.el_delete_policy_enable)))
            delete_button = driver.find_element_by_xpath(dpg.el_delete_policy_enable).get_attribute("class")
            assert delete_button.split("-")[-1] != "disabled"
            # 判断[添加文档域]按钮是否可用
            WebDriverWait(driver, 60).until(
                ec.visibility_of_element_located((By.XPATH, dpg.el_add_domain_enable)))
            adddomain_button = driver.find_element_by_xpath(dpg.el_add_domain_enable).get_attribute("class")
            assert adddomain_button.split("-")[-1] != "disabled"
            # 判断绑定文档域列表显示信息
            WebDriverWait(driver, 60).until(
                ec.visibility_of_element_located((By.XPATH, dpg.el_apply_domain_first)))
            domain_name = dpg.get_apply_domain_info()  # 获取策略绑定文档域首行名称
            assert domain_name == get_domain["replace_domain"]
            # 判断文档域列表删除按钮一直可用
            deletedomain_button = driver.find_element_by_xpath(dpg.el_unbind_domain_enable).get_attribute("class")
            assert deletedomain_button.split("-")[-1] != "disabled"
        # except Exception:
        #
        #     Domain_mgnt_home_page(driver).close_windows()
        #     raise

    @pytest.fixture(scope="function")
    def set_father_domain(self, driver, get_domain, request):
        host = request.config.getoption(name="--host")
        host = host.split('//')[1].split(':')[0]
        # 新增策略
        policyuuid = CommonDocDomain().addPolicy(httphost=host, name="上海爱数安全策略ni")
        # father_domain添加当前AS为子域
        domainuuid = CommonDocDomain().addRelationDomain(httphost=get_domain["father_domain"], host=host)
        yield
        CommonDocDomain().deletepolicy(httphost=host, PolicyUUID=policyuuid)
        CommonDocDomain().delRelationDomain(host=get_domain["father_domain"], uuid=domainuuid)
        # 增加刷新步骤，清除脏数据
        driver.find_element_by_xpath("//a[span[text()='组织管理']]").click()
        Domain_mgnt_home_page(driver=driver).return_domain_home_page()

    @allure.testcase("caseid:5503  策略同步--策略配置列表项检查（子域登录）")
    @pytest.mark.ni
    @pytest.mark.normal
    def test_check_childdomain_poliystatus(self, driver, set_father_domain):
        # try:
            driver.find_element_by_xpath("//a[span[text()='组织管理']]").click()
            Domain_mgnt_home_page(driver=driver).return_domain_home_page()
            Domain_mgnt_home_page(driver=driver).policy_sync()
            dpg = doc_policy_page(driver)
            time.sleep(5)
            # 判断[添加策略配置]按钮灰化
            WebDriverWait(driver, 60).until(
                ec.visibility_of_element_located((By.XPATH, dpg.el_add_policy_enable)))
            add_button = driver.find_element_by_xpath(dpg.el_add_policy_enable).get_attribute("class")
            assert add_button.split("-")[-1] == "disabled"
            # 判断策略列表第一项是否为原先添加的策略
            WebDriverWait(driver, 60).until(
                ec.visibility_of_element_located((By.XPATH, dpg.el_policy_first)))
            policy_name = driver.find_element_by_xpath(dpg.el_policy_first).text
            assert policy_name == "上海爱数安全策略ni"
            # 判断策略列表[编辑]按钮灰化
            WebDriverWait(driver, 60).until(
                ec.visibility_of_element_located((By.XPATH, dpg.el_edit_policy_enable)))
            edit_button = driver.find_element_by_xpath(dpg.el_edit_policy_enable).get_attribute("class")
            assert edit_button.split("-")[-1] == "disabled"
            # 判断策略列表[删除]按钮一直可用
            WebDriverWait(driver, 60).until(
                ec.visibility_of_element_located((By.XPATH, dpg.el_delete_policy_enable)))
            delete_button = driver.find_element_by_xpath(dpg.el_delete_policy_enable).get_attribute("class")
            assert delete_button.split("-")[-1] != "disabled"
            # 判断[添加文档域]按钮不可用
            WebDriverWait(driver, 60).until(
                ec.visibility_of_element_located((By.XPATH, dpg.el_add_domain_enable)))
            deletedomain_button = driver.find_element_by_xpath(dpg.el_add_domain_enable).get_attribute("class")
            assert deletedomain_button.split("-")[-1] == "disabled"
        # except Exception:
        #
        #     Domain_mgnt_home_page(driver).close_windows()
        #     raise

    @pytest.fixture(scope="function")
    def set_bind_domain(self, driver, get_domain, request):
        host = request.config.getoption(name="--host")
        host = host.split('//')[1].split(':')[0]
        # 新增策略
        policyuuid = CommonDocDomain().addPolicy(httphost=host, name="上海爱数安全策略ni")
        # 当前域添加replace_domain为子域
        domainuuid = CommonDocDomain().addRelationDomain(httphost=host, host=get_domain["replace_domain"])
        # 策略和子域绑定
        CommonDocDomain().BoundPolicy(httphost=host, PolicyUUID=policyuuid, ChildDomainUUID=domainuuid)
        yield host, policyuuid
        CommonDocDomain().deletepolicy(httphost=host, PolicyUUID=policyuuid)
        CommonDocDomain().delRelationDomain(host=host, uuid=domainuuid)
        WebDriverWait(driver, 30).until(
            ec.visibility_of_element_located((By.CSS_SELECTOR, Domain_mgnt_home_page(driver).el_domain_mgnt)))
        driver.find_element_by_css_selector(Domain_mgnt_home_page(driver).el_domain_mgnt).click()

    @allure.testcase("caseid:5531  策略同步--解绑文档域成功")
    @pytest.mark.ni
    @pytest.mark.normal
    def test_check_unbineddomain(self, driver, set_bind_domain):
        # try:
            driver.find_element_by_xpath("//a[span[text()='组织管理']]").click()
            host = set_bind_domain[0]
            policyuuid = set_bind_domain[1]
            Domain_mgnt_home_page(driver=driver).return_domain_home_page()
            Domain_mgnt_home_page(driver=driver).policy_sync()
            dpg = doc_policy_page(driver)
            # 点击删除按钮
            WebDriverWait(driver, 60).until(
                ec.visibility_of_element_located((By.XPATH, dpg.el_unbind_domain)))
            driver.find_element_by_xpath(dpg.el_unbind_domain).click()
            # 点击提示框中[确定]按钮
            WebDriverWait(driver, 20).until(
                ec.visibility_of_element_located((By.XPATH, doc_policy_page(driver).el_applydomain_hinticon)))
            driver.find_element_by_xpath(doc_policy_page(driver).is_submit).click()
            time.sleep(3)
            # 调用“获取已绑定子文档域”接口，验证此时策略无绑定子域
            child_domain = CommonDocDomain().getPolicyChildDomainList(httphost=host, policyuuid=policyuuid)
            assert child_domain["count"] == 0
            domain = driver.find_elements_by_xpath(dpg.el_apply_domain_first)
            assert len(domain) == 0
        # except Exception:
        #
        #     Domain_mgnt_home_page(driver).close_windows()
        #     raise

    @pytest.fixture(scope="function")
    def edit_child_infomation(self, driver, get_domain, request):
        host = request.config.getoption(name="--host")
        host = host.split('//')[1].split(':')[0]  # 获取当前运行环境IP
        # 当前域添加replace_domain为子域
        domainuuid = CommonDocDomain().addRelationDomain(httphost=host, host=get_domain["replace_domain"])
        yield host, domainuuid
        CommonDocDomain().delRelationDomain(host=host, uuid=domainuuid)
        driver.find_element_by_xpath("//a[span[text()='组织管理']]").click()
        Domain_mgnt_home_page(driver=driver).return_domain_home_page()

    @allure.testcase("caseid:5669 文档域管理--编辑子域--点击[取消]")
    @pytest.mark.ni
    @pytest.mark.high
    def test_edit_child_information(self, driver, edit_child_infomation):
        # try:
            driver.find_element_by_xpath("//a[span[text()='组织管理']]").click()
            Domain_mgnt_home_page(driver=driver).return_domain_home_page()
            # 点击[编辑]按钮
            WebDriverWait(driver, 60).until(
                ec.visibility_of_element_located((By.XPATH, Domain_mgnt_page(driver).el_edit_domain)))
            driver.find_element_by_xpath(Domain_mgnt_page(driver).el_edit_domain).click()
            # 等待编辑文档域弹框出现
            WebDriverWait(driver, 60).until(
                ec.visibility_of_element_located((By.XPATH, Domain_mgnt_page(driver).el_edit_h1)))
            # 同时编辑端口/id/key
            host = edit_child_infomation[0]
            domainuuid = edit_child_infomation[1]
            if host != '10.2.181.170':
                driver.find_element_by_xpath(Domain_mgnt_page(driver).el_edit_port).send_keys(Keys.CONTROL, 'a')  # 编辑端口
                driver.find_element_by_xpath(Domain_mgnt_page(driver).el_edit_port).send_keys('111')
                driver.find_element_by_xpath(Domain_mgnt_page(driver).el_edit_appid).send_keys(Keys.CONTROL, 'a')  # 编辑id
                driver.find_element_by_xpath(Domain_mgnt_page(driver).el_edit_appid).send_keys('222')
                driver.find_element_by_xpath(Domain_mgnt_page(driver).el_edit_appkey).send_keys(Keys.CONTROL, 'a')  # 编辑key
                driver.find_element_by_xpath(Domain_mgnt_page(driver).el_edit_appkey).send_keys('333')
            else:
                driver.find_element_by_xpath(Domain_mgnt_page(driver).el_edit_port).send_keys(Keys.COMMAND, 'a')
                driver.find_element_by_xpath(Domain_mgnt_page(driver).el_edit_port).send_keys(Keys.COMMAND, Keys.DELETE)
                driver.find_element_by_xpath(Domain_mgnt_page(driver).el_edit_port).send_keys('111')
                driver.find_element_by_xpath(Domain_mgnt_page(driver).el_edit_appid).send_keys(Keys.COMMAND, 'a')
                driver.find_element_by_xpath(Domain_mgnt_page(driver).el_edit_appid).send_keys(Keys.COMMAND, Keys.DELETE)
                driver.find_element_by_xpath(Domain_mgnt_page(driver).el_edit_appid).send_keys('222')
                driver.find_element_by_xpath(Domain_mgnt_page(driver).el_edit_appkey).send_keys(Keys.COMMAND, 'a')
                driver.find_element_by_xpath(Domain_mgnt_page(driver).el_edit_appkey).send_keys(Keys.COMMAND, Keys.DELETE)
                driver.find_element_by_xpath(Domain_mgnt_page(driver).el_edit_appkey).send_keys('333')
            driver.find_element_by_xpath(Domain_mgnt_page(driver).el_edit_cancel).click()
            child_info = CommonDocDomain().getRelationDomain(host=host, uuid=domainuuid)
            assert child_info["port"] == 443
            assert child_info["app_id"] == "admin"
            assert child_info["app_key"] == "eisoo.cn"
            WebDriverWait(driver, 60).until(
                ec.visibility_of_element_located((By.XPATH, Domain_mgnt_page(driver).el_edit_domain)))
            driver.find_element_by_xpath(Domain_mgnt_page(driver).el_edit_domain).click()
            WebDriverWait(driver, 60).until(
                ec.visibility_of_element_located((By.XPATH, Domain_mgnt_page(driver).el_edit_h1)))
            driver.find_element_by_xpath(Domain_mgnt_page(driver).el_edit_confirm).click()
            child_info = CommonDocDomain().getRelationDomain(host=host, uuid=domainuuid)
            assert child_info["port"] == 443
            assert child_info["app_id"] == "admin"
            assert child_info["app_key"] == "eisoo.cn"
        # except Exception:
        #
        #     Domain_mgnt_home_page(driver).close_windows()
        #     raise

    @allure.testcase("5545 策略同步--文档域管理页面检查")
    @pytest.mark.normal
    @pytest.mark.zyl
    def test_untie_domain(self, driver, get_domain, request):
        # try:
            host = request.config.getoption(name="--host")
            host = host.split('//')[1].split(':')[0]
            childhost = get_domain["parallel_domain"]
            # 策略绑定文档域
            policyuuid = CommonDocDomain().addPolicy(httphost=host, name="上海爱数安全策略")
            addDomainuuid = CommonDocDomain().addRelationDomain(host=childhost, httphost=host)
            CommonDocDomain().BoundPolicy(httphost=host, PolicyUUID=policyuuid, ChildDomainUUID=addDomainuuid)
            Domain_mgnt_home_page(driver).return_domain_home_page()
            Domain_mgnt_home_page(driver).policy_sync()
            Domain_mgnt_home_page(driver).return_domain_home_page()
            dp = Domain_mgnt_page(driver)
            WebDriverWait(driver, 30).until(ec.visibility_of_element_located((By.XPATH, dp.el_list_policy_name)))
            policy_name_info = driver.find_element_by_xpath(dp.el_list_policy_name).text
            untie_buttion_true = driver.find_element_by_xpath(dp.el_untie_policy).is_displayed()
            CommonDocDomain().delboundPolicy(httphost=host, PolicyUUID=policyuuid, ChildDomainUUID=addDomainuuid)
            Domain_mgnt_home_page(driver).policy_sync()
            Domain_mgnt_home_page(driver).return_domain_home_page()
            WebDriverWait(driver, 30).until(ec.visibility_of_element_located((By.XPATH, dp.el_list_policy_name)))
            policy_name = driver.find_element_by_xpath(dp.el_list_policy_name).text
            untie_buttion_false = dp.isElement(dp.el_untie_policy)
            CommonDocDomain().deletepolicy(httphost=host, PolicyUUID=policyuuid)
            CommonDocDomain().delRelationDomain(host=host, uuid=addDomainuuid)
            Domain_mgnt_home_page(driver).policy_sync()
            Domain_mgnt_home_page(driver).return_domain_home_page()
            assert policy_name_info == "上海爱数安全策略"
            assert untie_buttion_true is True
            assert policy_name == "---"
            assert untie_buttion_false is False
        # except Exception:
        #
        #     raise

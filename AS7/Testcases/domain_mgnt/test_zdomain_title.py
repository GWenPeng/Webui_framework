from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from Common.screenshot import ScreenShot
from Common.ssh_client import SSHClient
from Common.mysqlconnect import DB_connect
from AS7.Pages.Login_page import Login_page
from AS7.Pages.Home_page import Home_page
from AS7.Pages.Domain_mgnt.domain_mgnt_home_page import Domain_mgnt_home_page
from AS7.Pages.Domain_mgnt.CommonDocDomain import CommonDocDomain
from AS7.Pages.Domain_mgnt.doc_policy_page import doc_policy_page
import pytest
import allure
import time
from selenium.common.exceptions import *


@pytest.fixture(scope="class")
def separation_of_powers(driver, request):
    host = request.config.getoption("--host")
    ssh_host = host.split('//')[1].split(':')[0]  # 举例：ssh_host = 10.2.176.176
    admin_host = 'http://' + ssh_host + ':8000'
    # 开启三权分立
    sh = SSHClient(host=ssh_host)
    sh.command("cd /sysvol/apphome/app/ThriftAPI/gen-py-tmp/ShareMgnt; "
               "./ncTShareMgnt-remote -h localhost:9600 Usrm_SetTriSystemStatus True")
    time.sleep(4)  # 等待4s，使配置生效
    yield ssh_host, admin_host
    # 关闭三权分立
    sh = SSHClient(host=ssh_host)
    sh.command("cd /sysvol/apphome/app/ThriftAPI/gen-py-tmp/ShareMgnt;"
               "./ncTShareMgnt-remote -h localhost:9600 Usrm_SetTriSystemStatus False")
    # 关闭三权分立后，重新登录控制台，清除三权分立影响
    time.sleep(5)
    driver.get(admin_host)
    # 登陆系统管理员
    Login_page(driver=driver).login(username='admin', password='eisoo.com')


class Test_separate_power_domaintitle:
    @allure.testcase("CaseID:5452 文档域管理--三权分立")
    @pytest.mark.ni
    @pytest.mark.high
    def test_separate_power_admintitle(self, driver, separation_of_powers):
        # try:
            admin_host = separation_of_powers[1]
            # 重新获取控制台登陆页面，用以登陆不同管理员
            driver.get(admin_host)
            # 登陆系统管理员
            Login_page(driver=driver).login(username='admin', password='eisoo.com')
            WebDriverWait(driver, 10).until(
                ec.invisibility_of_element_located((By.XPATH, Home_page(driver).el_logsaudit_words)))
            WebDriverWait(driver, 60).until(
                ec.visibility_of_element_located((By.XPATH, Home_page(driver).el_organizations)))
            # 断言三权分立--系统管理员可视tab页
            title_element1 = driver.find_element_by_xpath(Home_page(driver).el_organizations_words)
            contens1 = title_element1.text
            assert contens1 == "组织管理"
            title_element2 = driver.find_element_by_xpath(Home_page(driver).el_security_words)
            contens2 = title_element2.text
            assert contens2 == "安全管理"
            title_element3 = driver.find_element_by_xpath(Home_page(driver).el_domains_words)
            contens3 = title_element3.text
            assert contens3 == "文档域管理"
            title_element4 = driver.find_element_by_xpath(Home_page(driver).el_operations_words)
            contens4 = title_element4.text
            assert contens4 == "运营管理"
        # except Exception:
        #     #
        #     Domain_mgnt_home_page(driver).close_windows()
        #     raise

    @pytest.fixture(scope="function")
    def add_child_domain(self, driver, request, get_domain):
        host = request.config.getoption("--host")
        ssh_host = host.split('//')[1].split(':')[0]  # 举例：ssh_host = 10.2.176.176
        admin_host = 'http://' + ssh_host + ':8000'
        # 新增策略
        policyuuid = CommonDocDomain().addPolicy(httphost=ssh_host, name="上海爱数安全策略ni")
        # 当前域添加replace_domain为子域
        domainuuid = CommonDocDomain().addRelationDomain(httphost=ssh_host, host=get_domain["replace_domain"])
        yield admin_host, policyuuid
        CommonDocDomain().delboundPolicy(httphost=ssh_host, PolicyUUID=policyuuid, ChildDomainUUID=domainuuid)
        CommonDocDomain().deletepolicy(httphost=ssh_host, PolicyUUID=policyuuid)
        CommonDocDomain().delRelationDomain(host=ssh_host, uuid=domainuuid)
        # 安全管理员可视组织管理tab页，增加刷新，去除脏数据
        driver.find_element_by_xpath("//a[span[text()='组织管理']]").click()
        Domain_mgnt_home_page(driver=driver).return_domain_home_page()

    @allure.testcase("caseid:6821 文档域策略同步--三权分立绑定文档域成功")
    @pytest.mark.ni
    @pytest.mark.high
    def test_separate_bind_domainsuccess(self, driver, get_domain, add_child_domain, separation_of_powers):
        # try:
            admin_host = add_child_domain[0]
            # 重新获取登陆页面，登陆安全管理员
            driver.get(admin_host)
            Login_page(driver=driver).login(username='security', password='eisoo.com')
            # 切换至策略同步
            Domain_mgnt_home_page(driver=driver).return_domain_home_page()
            # 点击[添加文档域]按钮
            WebDriverWait(driver, 30).until(
                ec.visibility_of_element_located((By.XPATH, doc_policy_page(driver).el_add_domain)))
            time.sleep(5)
            driver.find_element_by_xpath(doc_policy_page(driver).el_add_domain).click()
            # 等待添加文档域弹窗显示
            WebDriverWait(driver, 80).until(
                ec.visibility_of_element_located((By.XPATH, doc_policy_page(driver).el_add_domain_title)))
            domain_name = get_domain["replace_domain"]
            driver.implicitly_wait(60)
            # 点击第一个子域绑定
            WebDriverWait(driver, 60).until(
                ec.visibility_of_element_located((By.XPATH, doc_policy_page(driver).el_child_domain_location)))
            driver.find_element_by_xpath(doc_policy_page(driver).el_child_domain_location).click()
            # 断言子域A出现在“已选”列表
            WebDriverWait(driver, 60).until(
                ec.visibility_of_element_located((By.CSS_SELECTOR, doc_policy_page(driver).el_first_binded_domain)))
            binded_name = driver.find_element_by_css_selector(doc_policy_page(driver).el_first_binded_domain).text
            assert binded_name == domain_name
            # 断言子域A后[删除]按钮可用
            x_button = driver.find_element_by_xpath(doc_policy_page(driver).el_x).is_enabled()
            assert x_button == True
            # 断言添加文档域[清空]按钮可用
            clear_button = driver.find_element_by_xpath(doc_policy_page(driver).el_clear_button).is_enabled()
            assert clear_button == True
            # 断言添加文档域[确定]按钮可用
            submit_button = driver.find_element_by_xpath(doc_policy_page(driver).el_submit_button).is_enabled()
            assert submit_button == True
            # 点击[确定]，绑定子域成功后，界面检查
            driver.find_element_by_xpath(doc_policy_page(driver).el_submit_button).click()
            time.sleep(5)
            # 断言弹窗消失--查找添加文档域界面[取消]按钮，一定时间找不到，执行后续
            try:
                WebDriverWait(driver, 15).until(
                    ec.visibility_of_element_located((By.XPATH, doc_policy_page(driver).el_clear_button)))
            except TimeoutException:
                # 调用“获取已绑定子文档域”接口验证绑定正确，添加文档域列表存在子域A
                host = separation_of_powers[0]
                policyuuid = add_child_domain[1]
                binded_domain = CommonDocDomain().getPolicyChildDomainList(httphost=host, policyuuid=policyuuid)
                domain = binded_domain["data"][0]["host"]
                assert domain == domain_name
                WebDriverWait(driver, 60).until(
                    ec.visibility_of_element_located((By.XPATH, doc_policy_page(driver).el_apply_domain_first)))
                first_binded_domain = driver.find_element_by_xpath(doc_policy_page(driver).el_apply_domain_first).text
                assert first_binded_domain == domain_name
                # 断言添加文档域列表[x]按钮可用
                first_unbinded_button = driver.find_element_by_xpath(
                    doc_policy_page(driver).el_unbind_domain_enable).is_enabled()
                assert first_unbinded_button == True
            else:
                print("you are error!!")
        # except Exception:
        #
        #     Domain_mgnt_home_page(driver).close_windows()
        #     raise

    @pytest.fixture(scope='function')
    def many_child_domain(self, driver, get_domain, request):
        host = request.config.getoption("--host")
        ssh_host = host.split('//')[1].split(':')[0]
        # 新增策略
        policyuuid = CommonDocDomain().addPolicy(httphost=ssh_host, name="上海爱数安全策略ni")
        # 当前域添加replace_domain为子域
        domainuuid = CommonDocDomain().addRelationDomain(httphost=ssh_host, host=get_domain["replace_domain"])
        # 构造30个子域数据并绑定
        db = DB_connect(host=ssh_host)
        for child_domain in range(30):
            sql = "insert into domain_mgnt.t_relationship_domain " \
                  "values('{}','{}',443,'','','child','direct','admin','eisoo.com',now())"
            domainId = "9b04d18d-6c15-45a6-8c8c-6b8dc67" + str(child_domain)
            domain = "docdomain.com" + str(child_domain)
            domainSql = sql.format(domainId, domain)
            db.insert(domainSql)
        for bind_domain in range(30):
            policyId = policyuuid
            domainId = "9b04d18d-6c15-45a6-8c8c-6b8dc67" + str(bind_domain)
            insertDomain = "insert into domain_mgnt.t_policy_tpl_domains values('{}','{}')"
            domainSqls = insertDomain.format(policyId, domainId)
            db.insert(domainSqls)
        db.close()
        yield
        CommonDocDomain().delboundPolicy(httphost=ssh_host, PolicyUUID=policyuuid, ChildDomainUUID=domainuuid)
        CommonDocDomain().delRelationDomain(host=ssh_host, uuid=domainuuid)
        db = DB_connect(host=ssh_host)
        db.delete("delete from domain_mgnt.t_relationship_domain")
        db.delete("delete from domain_mgnt.t_policy_tpl_domains")
        db.close()
        CommonDocDomain().deletepolicy(httphost=ssh_host, PolicyUUID=policyuuid)
        # 安全管理员可视组织管理tab页，增加刷新，去除脏数据
        driver.find_element_by_xpath("//a[span[text()='组织管理']]").click()
        Domain_mgnt_home_page(driver=driver).return_domain_home_page()

    @allure.testcase("caseid:6821 文档域策略同步--三权分立绑定文档域成功--列表翻页检查")
    @pytest.mark.ni
    @pytest.mark.high
    def test_many_childdomain(self, driver, get_domain, many_child_domain, separation_of_powers):
        # try:
            replace_domain = get_domain["replace_domain"]
            # 上条用例已登录安全管理员，无需再次登录
            driver.find_element_by_xpath("//a[span[text()='组织管理']]").click()
            Domain_mgnt_home_page(driver=driver).return_domain_home_page()
            # 点击添加文档域[下一页]按钮，翻至第二页
            driver.implicitly_wait(30)
            WebDriverWait(driver, 60).until(
                ec.visibility_of_element_located((By.XPATH, doc_policy_page(driver).el_domain_next_page_icon)))
            driver.find_element_by_xpath(doc_policy_page(driver).el_domain_next_page_icon).click()
            driver.find_element_by_xpath(doc_policy_page(driver).el_domain_next_page_icon).click()
            time.sleep(3)
            # 点击[添加文档域]按钮
            WebDriverWait(driver, 60).until(
                ec.visibility_of_element_located((By.XPATH, doc_policy_page(driver).el_add_domain)))
            driver.find_element_by_xpath(doc_policy_page(driver).el_add_domain).click()
            # 等待弹窗显示
            WebDriverWait(driver, 60).until(
                ec.visibility_of_element_located((By.XPATH, doc_policy_page(driver).el_add_domain_title)))
            driver.implicitly_wait(60)
            # 子域A出现在列表顶部，点击绑定
            WebDriverWait(driver, 60).until(
                ec.visibility_of_element_located((By.XPATH, doc_policy_page(driver).el_child_domain_location)))
            driver.find_element_by_xpath(doc_policy_page(driver).el_child_domain_location).click()
            # 点击添加弹窗确定按钮，等待绑定成功
            WebDriverWait(driver, 60).until(
                ec.visibility_of_element_located((By.CSS_SELECTOR, doc_policy_page(driver).el_first_binded_domain)))
            driver.find_element_by_xpath(doc_policy_page(driver).el_submit_button).click()
            time.sleep(5)
            # 断言列表回到第一页
            WebDriverWait(driver, 60).until(
                ec.visibility_of_element_located((By.XPATH, doc_policy_page(driver).el_binded_domain_page_input)))
            page_value = driver.find_element_by_xpath(
                doc_policy_page(driver).el_binded_domain_page_input).get_attribute(
                "value")
            assert page_value == '1'
            # 断言子域A出现在列表顶部
            WebDriverWait(driver, 60).until(
                ec.visibility_of_element_located((By.XPATH, doc_policy_page(driver).el_apply_domain_first)))
            child_domain = driver.find_element_by_xpath(doc_policy_page(driver).el_apply_domain_first).text
            assert child_domain == replace_domain
        # except Exception:
        #
        #     Domain_mgnt_home_page(driver).close_windows()
        #     raise

    @pytest.fixture(scope='function')
    def many_one_domain(self, driver, get_domain, request):
        host = request.config.getoption("--host")
        ssh_host = host.split('//')[1].split(':')[0]
        # 新增策略
        policyuuid = CommonDocDomain().addPolicy(httphost=ssh_host, name="上海爱数安全策略ni")
        # 当前域添加replace_domain为子域
        domainuuid = CommonDocDomain().addRelationDomain(httphost=ssh_host, host=get_domain["replace_domain"])
        # 策略绑定子域
        CommonDocDomain().BoundPolicy(httphost=ssh_host, PolicyUUID=policyuuid, ChildDomainUUID=domainuuid)
        yield
        CommonDocDomain().delboundPolicy(httphost=ssh_host, PolicyUUID=policyuuid, ChildDomainUUID=domainuuid)
        CommonDocDomain().delRelationDomain(host=ssh_host, uuid=domainuuid)
        CommonDocDomain().deletepolicy(httphost=ssh_host, PolicyUUID=policyuuid)
        # 安全管理员可视组织管理tab页，增加刷新，去除脏数据
        driver.find_element_by_xpath("//a[span[text()='组织管理']]").click()
        Domain_mgnt_home_page(driver=driver).return_domain_home_page()

    @allure.testcase("caseid:6822 文档域策略同步--三权分立解绑文档域成功")
    @pytest.mark.ni
    @pytest.mark.normal
    def test_one_childdomain(self, driver, get_domain, many_one_domain, separation_of_powers):
        # try:
            driver.find_element_by_xpath("//a[span[text()='组织管理']]").click()
            Domain_mgnt_home_page(driver=driver).return_domain_home_page()
            # 点击解绑按钮
            WebDriverWait(driver, 60).until(
                ec.visibility_of_element_located((By.XPATH, doc_policy_page(driver).el_unbind_domain)))
            driver.find_element_by_xpath(doc_policy_page(driver).el_unbind_domain).click()
            # 等待确定解绑弹窗显示
            WebDriverWait(driver, 60).until(
                ec.visibility_of_element_located((By.XPATH, doc_policy_page(driver).el_unbind_domain_tip)))
            driver.find_element_by_xpath(doc_policy_page(driver).el_unbind_domain_confirm).click()
            # 确认绑定列表不存在文档域A
            try:
                WebDriverWait(driver, 15).until(
                    ec.visibility_of_element_located((By.XPATH, doc_policy_page(driver).el_apply_domain_first)))
            except TimeoutException:
                pass
        # except Exception:
        #
        #     Domain_mgnt_home_page(driver).close_windows()
        #     raise

    @allure.testcase("CaseID:5678 文档域策略同步--三权分立")
    @pytest.mark.zyl
    @pytest.mark.high
    def test_separate_power_policy(self, request, driver):
        # try:
            host = request.config.getoption("--host")
            ssh_host = host.split('//')[1].split(':')[0]
            # 开启三权分立
            sh = SSHClient(host=ssh_host)
            sh.command("cd /sysvol/apphome/app/ThriftAPI/gen-py-tmp/ShareMgnt; "
                       "./ncTShareMgnt-remote -h localhost:9600 Usrm_SetTriSystemStatus True")
            # 安全管理员登录
            driver.get(host)
            Login_page(driver=driver).login(username='security', password='eisoo.com')
            hp = Home_page(driver)
            WebDriverWait(driver, 30).until(
                ec.visibility_of_element_located((By.XPATH, hp.el_organizations)))
            Security_organizations_title = driver.find_element_by_xpath(hp.el_organizations).text
            Security_sy_title = driver.find_element_by_xpath(hp.el_Security).text
            Security_domains_title = driver.find_element_by_xpath(hp.el_Domains).text
            Security_LogsAudit_title = driver.find_element_by_xpath(hp.el_LogsAudit).text
            dp = Domain_mgnt_home_page(driver=driver)
            dp.return_domain_home_page()
            domains_title = driver.find_element_by_xpath(hp.el_domains_list).text
            assert Security_organizations_title == "组织管理"
            assert Security_sy_title == "安全管理"
            assert Security_domains_title == "文档域管理"
            assert Security_LogsAudit_title == "审计管理"
            assert domains_title == "策略同步"
            # 系统管理员admin登录
            driver.get(host)
            Login_page(driver=driver).login(username='admin', password='eisoo.com')
            home = Home_page(driver)
            WebDriverWait(driver, 30).until(
                ec.visibility_of_element_located((By.XPATH, home.el_organizations)))
            admin_organizations_title = driver.find_element_by_xpath(home.el_organizations).text
            admin_domains_title = driver.find_element_by_xpath(home.el_Domains).text
            admin_operations_title = driver.find_element_by_xpath(home.el_Operations).text
            dp = Domain_mgnt_home_page(driver=driver)
            dp.return_domain_home_page()
            domains_titles = driver.find_element_by_xpath(home.el_domains_list).text
            assert admin_organizations_title == "组织管理"
            assert admin_domains_title == "文档域管理"
            assert admin_operations_title == "运营管理"
            assert domains_titles == "文档域管理"
            # 审计管理员登录
            driver.get(host)
            Login_page(driver=driver).login(username='audit', password='eisoo.com')
            audit_home = Home_page(driver)
            WebDriverWait(driver, 30).until(
                ec.visibility_of_element_located((By.XPATH, audit_home.el_LogsAudit)))
            audit_title = driver.find_element_by_xpath(audit_home.el_LogsAudit).text
            assert audit_title == "审计管理"
            # 关闭三权分立
            sh = SSHClient(host=ssh_host)
            sh.command("cd /sysvol/apphome/app/ThriftAPI/gen-py-tmp/ShareMgnt;"
                       "./ncTShareMgnt-remote -h localhost:9600 Usrm_SetTriSystemStatus False")
            driver.get(host)
            Login_page(driver=driver).login(username='admin', password='eisoo.com')
            # 返回初始页面
            Domain_mgnt_home_page(driver=driver).return_domain_home_page()
        # except Exception:
        #
        #     raise

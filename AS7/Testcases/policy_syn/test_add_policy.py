# coding=utf-8
from AS7.Pages.Domain_mgnt.doc_policy_page import doc_policy_page
from AS7.Pages.Domain_mgnt.domain_mgnt_home_page import Domain_mgnt_home_page
from AS7.Pages.Domain_mgnt.domain_mgnt_page import Domain_mgnt_page
from AS7.Pages.Login_page import Login_page
from AS7.Pages.Domain_mgnt.CommonDocDomain import CommonDocDomain
from Common.parse_data import do_excel
from Common.http_request import Http_client
from Common.ssh_client import SSHClient
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from Common.mysqlconnect import DB_connect
import pytest
import allure
import time


class Test_separate_power_add_policy:
    @pytest.fixture(scope='function')
    def clean_environment(self, driver, request):
        host = request.config.getoption("--host")
        global ssh_host
        ssh_host = host.split('//')[1].split(':')[0]
        url_host = 'https://' + ssh_host + ':443'
        admin_host = 'https://' + ssh_host + ':8000'
        # 开启三权分立
        sh = SSHClient(host=ssh_host)
        sh.command("cd /sysvol/apphome/app/ThriftAPI/gen-py-tmp/ShareMgnt;"
                   " ./ncTShareMgnt-remote -h localhost:9600 Usrm_SetTriSystemStatus True")
        # 等待4秒后刷新页面
        time.sleep(4)
        yield admin_host
        # 关闭三权分立
        sh = SSHClient(host=ssh_host)
        sh.command("cd /sysvol/apphome/app/ThriftAPI/gen-py-tmp/ShareMgnt;"
                   "./ncTShareMgnt-remote -h localhost:9600 Usrm_SetTriSystemStatus False")
        time.sleep(4)
        # 删除策略
        get_client = Http_client()
        get_url = "%s/api/document-domain-management/v1/policy-tpl" % (url_host)
        get_client.get(url=get_url,
                       params="{\"limit\":\"20\",\"start\":\"0\"}",
                       header="{\"Content-Type\":\"application/json\"}")
        response = get_client.jsonResponse['data']
        for id in response:
            policyid = id['id']
            del_client = Http_client()
            del_url = "%s/api/document-domain-management/v1/policy-tpl/%s" % (url_host, policyid)
            del_client.delete(url=del_url, header='{"Content-Type":"application/json"}')
        # 关闭三权分立后，重新获取页面登录
        driver.get(admin_host)
        Login_page(driver=driver).login(username='admin', password='eisoo.com')
        Domain_mgnt_home_page(driver=driver).return_domain_home_page()

    @allure.testcase("CaseID:6820 文档域策略同步--三权分立添加策略配置成功")
    @pytest.mark.ni
    @pytest.mark.normal
    def test_separate_power_add_policy(self, driver, clean_environment):
        # try:
            admin_host = clean_environment
            # 再次获取控制台登录页面，登录安全管理员
            driver.get(admin_host)
            Login_page(driver=driver).login(username='security', password='eisoo.com')
            # 读取excle 数据，但读取数据为列表中包含元组
            policyname = []
            data = do_excel(filename="ni.xlsx",
                            sheetname="test_separate_power_add_policy", minrow=1, maxrow=6, mincol=1, maxcol=1)
            for name in data:
                policyname.append(name[0])
            # 定位到策略同步
            Domain_mgnt_home_page(driver=driver).return_domain_home_page()
            for name in policyname:
                doc_policy_page(driver=driver).add_policy(name)
            # 判断新增策略弹窗关闭
            time.sleep(1)
            element = driver.find_elements_by_xpath("//span[text()='登录策略']")
            assert len(element) == 0
            # 判断第一行元素是否为最后添加项
            WebDriverWait(driver, 60).until(
                ec.visibility_of_element_located((By.XPATH, "//span[text()='shanghai安全策略']")))
            first_name = driver.find_element_by_xpath(doc_policy_page(driver).el_policy_first).text
            assert first_name == 'shanghai安全策略'
            # 判断第一行是否被选中
            global ssh_host
            if ssh_host != "10.2.181.170":
                classname = driver.find_element_by_xpath(doc_policy_page(driver).el_policy_first_selected).get_attribute("class")
                selected = classname.split('-')[43]
                assert selected == 'selectable'
            else:
                classname = driver.find_element_by_xpath(doc_policy_page(driver).el_policy_first_selected).get_attribute("class")
                selected = classname.split('-')[43]
                assert 'selectable' in selected
            # 判断显示列表为空
            WebDriverWait(driver, 60).until(
                ec.visibility_of_element_located((By.XPATH, doc_policy_page(driver).el_list_is_null)))
            display = driver.find_element_by_xpath(doc_policy_page(driver).el_list_is_null).is_displayed()
            assert display == True
            # 判断添加文档域按钮可用
            enabled = driver.find_element_by_xpath(doc_policy_page(driver).el_add_domain).is_enabled()
            assert enabled == True
        # except Exception:
        #
        #     Domain_mgnt_home_page(driver).close_windows()
        #     raise

    @allure.step("添加策略")
    @pytest.fixture(scope="function")
    def add_policy(self,request):
        host = request.config.getoption(name="--host")
        host = host.split('//')[1].split(':')[0]
        uuids = []
        for i in range(1,51):
            uuid = CommonDocDomain().addPolicy(httphost=host,name="新增策略"+str(i))
            uuids.append(uuid)
        for i in range(1,12):
            uuid = CommonDocDomain().addPolicy(httphost=host, name="add_policy" + str(i))
            uuids.append(uuid)
        yield
        for id in uuids:
            CommonDocDomain().deletepolicy(httphost=host,PolicyUUID=id)

    @allure.testcase("5682 文档域策略同步--删除策略配置--策略配置分页显示"
                     "5696 文档域策略同步--搜索结果页--新建策略配置")
    @pytest.mark.normal
    @pytest.mark.gfr
    def test_search_page_operate_policy(self,request,driver,add_policy):
        Domain_mgnt_home_page(driver).return_domain_home_page()
        Domain_mgnt_home_page(driver).policy_sync()
        policy_mgnt = doc_policy_page(driver)
        time.sleep(3)
        assert driver.find_element_by_xpath(policy_mgnt.el_page_count).text == "显示 1 - 20 条，共 61 条"
        search_input = driver.find_element_by_xpath(policy_mgnt.el_page_input)
        Domain_mgnt_page(driver).clear_input(search_input)
        search_input.send_keys("4")
        WebDriverWait(driver,10).until(ec.visibility_of_element_located((By.XPATH,policy_mgnt.el_policy_first)))
        policy_mgnt.delete_policy(policy_name="新增策略9")
        time.sleep(2)
        assert driver.find_element_by_xpath(policy_mgnt.el_page_input).get_attribute("value") == "3"
        # 5696 新建策略配置
        policy_mgnt.add_policy(policy_name="登录策略")
        time.sleep(2)
        try:
            assert driver.find_element_by_xpath(policy_mgnt.el_page_input).get_attribute("value") == "1"
            assert policy_mgnt.get_policy_info() == "登录策略"
            driver.refresh()
            driver.set_page_load_timeout(30)
            WebDriverWait(driver,20).until(ec.visibility_of_element_located((By.XPATH,policy_mgnt.el_add_policy)))
            assert policy_mgnt.get_policy_info() == "add_policy1"
            Domain_mgnt_page(driver).clear_input(driver.find_element_by_xpath(policy_mgnt.el_page_input))
            driver.find_element_by_xpath(policy_mgnt.el_page_input).send_keys("4")
            policy_mgnt.delete_policy(policy_name="登录策略")
        except Exception:
            host = request.config.getoption(name="--host")
            host = host.split('//')[1].split(':')[0]
            uuid = DB_connect(dbname="db_domain_self",host=host).select_one("SELECT f_id FROM `t_policy_tpls` WHERE f_name = '登录策略'")
            CommonDocDomain().deletepolicy(httphost=host,PolicyUUID=uuid[0])
            raise

    @allure.testcase("5540 策略同步--删除策略配置--策略配置不存在")
    @pytest.mark.normal
    @pytest.mark.gfr
    def test_delete_not_exits_policy(self,driver,request):
        host = request.config.getoption(name="--host")
        host = host.split('//')[1].split(':')[0]
        uuid = CommonDocDomain().addPolicy(httphost=host, name="新增策略被删除的策略")
        try:
            Domain_mgnt_home_page(driver).return_domain_home_page()
            Domain_mgnt_home_page(driver).policy_sync()
            time.sleep(4)
            CommonDocDomain().deletepolicy(httphost=host, PolicyUUID=uuid)
            policy_mgnt = doc_policy_page(driver)
            el_name = f"//td[div[div[div[span[text()='新增策略被删除的策略']]]]]/following-sibling::td/div/div/div[2]/button"
            driver.find_element_by_xpath(el_name).click()
            time.sleep(2)
            assert driver.find_element_by_xpath(policy_mgnt.el_list_is_null).text == "列表为空"
        except Exception:
            CommonDocDomain().deletepolicy(httphost=host, PolicyUUID=uuid)
            raise

    @allure.testcase("5536 策略同步--文档域不存在--解绑文档域失败")
    @pytest.mark.normal
    @pytest.mark.zyl
    def test_untie_domain_failed(self, driver, get_domain, request):
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
            doc_mgnt = doc_policy_page(driver)
            time.sleep(2)
            # 解绑文档域
            CommonDocDomain().delboundPolicy(httphost=host, PolicyUUID=policyuuid, ChildDomainUUID=addDomainuuid)
            doc_mgnt.unbind_domain(domain_name=childhost)
            time.sleep(2)
            list_Info = driver.find_element_by_xpath(doc_mgnt.el_list_is_null).text
            # 清除策略绑定文档域
            CommonDocDomain().deletepolicy(httphost=host, PolicyUUID=policyuuid)
            CommonDocDomain().delRelationDomain(host=host, uuid=addDomainuuid)
            Domain_mgnt_home_page(driver).return_domain_home_page()
            time.sleep(1)
            assert list_Info == "列表为空"
        # except Exception:
        #
        #     raise

    @allure.testcase("5493 策略同步--入口检查")
    @pytest.mark.normal
    @pytest.mark.zyl
    def test_check_policy_entrance(self, driver):
        # try:
            Domain_mgnt_home_page(driver).return_domain_home_page()
            Domain_mgnt_home_page(driver).policy_sync()
            doc_mgnt = doc_policy_page(driver)
            WebDriverWait(driver, 30).until(ec.visibility_of_element_located((By.XPATH, doc_mgnt.el_add_policy)))
            policy_button_status = driver.find_element_by_xpath(doc_mgnt.el_add_policy_enable).is_enabled()
            policy_search_status = driver.find_element_by_xpath(doc_mgnt.el_policy_search).is_enabled()
            domain_button_status = driver.find_element_by_xpath(doc_mgnt.el_add_domain_enable).is_enabled()
            domain_search_status = driver.find_element_by_xpath(doc_mgnt.el_applylist_search).is_enabled()
            list_Info_first = driver.find_element_by_xpath(doc_mgnt.el_list_is_null).text
            list_Info_last = driver.find_element_by_xpath(doc_mgnt.el_list_null).text
            assert list_Info_first == "列表为空"
            assert list_Info_last == "列表为空"
            assert policy_button_status is True
            assert policy_search_status is True
            assert domain_button_status is False
            assert domain_search_status is False
        # except Exception:
        #
        #     Domain_mgnt_home_page(driver).close_windows()
        #     raise

    @allure.testcase("5565 策略同步--策略项检查--beta")
    @pytest.mark.normal
    @pytest.mark.ni
    def test_policy_popups_check(self, driver):
        # try:
            # 切换页面，刷新信息
            WebDriverWait(driver, 30).until(
                ec.visibility_of_element_located((By.XPATH, "//a[span[text()='组织管理']]")))
            driver.find_element_by_xpath("//a[span[text()='组织管理']]").click()
            Domain_mgnt_home_page(driver=driver).return_domain_home_page()
            Domain_mgnt_home_page(driver).policy_sync()
            # 点击[添加策略配置]按钮
            dpp = doc_policy_page(driver)
            WebDriverWait(driver, 60).until(
                ec.visibility_of_element_located((By.XPATH, dpp.el_add_policy)))
            driver.find_element_by_xpath(dpp.el_add_policy).click()
            # 定位登录策略元素
            WebDriverWait(driver, 60).until(
                ec.visibility_of_element_located((By.XPATH, dpp.el_popups_sidebar)))
            sidebar_status = driver.find_element_by_xpath(dpp.el_popups_sidebar).get_attribute("class")
            sidebar_status = sidebar_status.split(" ")[-1]
            # 断言登录策略默认选中
            assert sidebar_status == "skin-color"
            # 判断依次显示的策略名称正确
            name = ["密码强度", "限制客户端登录", "双因子认证"]
            policy_body = dpp.el_policy_body
            for i in range(1, 4):
                # 获取依次的策略名称
                every_policy_name = policy_body + '/div[%d]' % i + '/div[1]/div[1]'
                get_name = driver.find_element_by_xpath(every_policy_name).text
                assert get_name == name[i - 1]
            # 判断每个策略都不展开
            for i in range(1, 4):
                # 获取margin-top数值判断展开，0px为展开
                every_policy_name = policy_body + '/div[%d]' % i + '/div[2]/div[1]'
                ifopen = driver.find_element_by_xpath(every_policy_name).get_attribute("style")
                assert ifopen != "margin-top: 0px;"
            assert ec.element_to_be_clickable((By.XPATH, dpp.el_confirm_button))
            assert ec.element_to_be_clickable((By.XPATH, dpp.el_cancel_button))
            driver.find_element_by_xpath(dpp.el_cancel_button).click()
            driver.find_element_by_xpath("//a[span[text()='组织管理']]").click()
            Domain_mgnt_home_page(driver=driver).return_domain_home_page()
        # except Exception:
        #
        #     Domain_mgnt_home_page(driver).close_windows()
        #     raise

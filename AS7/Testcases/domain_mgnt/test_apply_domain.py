# coding=utf-8
from selenium.webdriver.support.wait import WebDriverWait
from AS7.Pages.Domain_mgnt.CommonDocDomain import CommonDocDomain
from AS7.Pages.Domain_mgnt.domain_mgnt_home_page import Domain_mgnt_home_page
from AS7.Pages.Domain_mgnt.domain_mgnt_page import Domain_mgnt_page
from AS7.Pages.Domain_mgnt.doc_policy_page import doc_policy_page
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from Common.mysqlconnect import DB_connect
from Common.parse_data import do_excel
import allure
import pytest
import time

from Common.screenshot import ScreenShot


@pytest.mark.wq_suite
class Test_Apply_Domain:

    @allure.step("子域解除策略绑定")
    @pytest.fixture(scope="function")
    def clear_applydomain(self, driver, request, get_domain):
        host = request.config.getoption(name="--host")
        host = host.split('//')[1].split(':')[0]
        childhost = get_domain["parallel_domain"]
        ChildDomainUUID = CommonDocDomain().addRelationDomain(httphost=host, host=childhost, domaintype="child")  # 添加子域
        PolicyUUID = CommonDocDomain().addPolicy(httphost=host, name="上海爱数安全策略")  # 添加策略

        yield
        CommonDocDomain().delboundPolicy(httphost=host, PolicyUUID=PolicyUUID, ChildDomainUUID=ChildDomainUUID)  # 子域解除策略绑定
        CommonDocDomain().clearRelationDomain(host=host)  # 解绑子域
        CommonDocDomain().deletepolicy(httphost=host, PolicyUUID=PolicyUUID)  # 删除策略
        Domain_mgnt_home_page(driver=driver).return_domain_home_page()  # 返回文档域管理界面
        time.sleep(2)


    @allure.testcase("5514--策略绑定文档域成功")
    @pytest.mark.high
    def test_policy_add_domain(self, driver, get_domain, clear_applydomain):
        # try:
            host = get_domain["parallel_domain"]
            el_apply = doc_policy_page(driver)
            Domain_mgnt_home_page(driver=driver).return_domain_home_page()   # 进入文档域管理界面
            Domain_mgnt_home_page(driver).policy_sync()  # 进入策略同步页面
            # # 获取配据置策略数
            # data = do_excel(filename='add_policy.xlsx', sheetname='策略配置', minrow=2, maxrow=2, mincol=1, maxcol=3)[0]
            # print(data)
            # 新增策略校验列表是否新增策略成功
            # doc_policy_page(driver).add_policy(policy_name=data[0], item=data[1])
            # p_new_name = doc_policy_page(driver).get_policy_info()
            # print(p_new_name)
            # assert p_new_name == data[0]
            # 策略绑定文档域成功
            doc_policy_page(driver).apply_domain(domain_name=host)
            d_new_name = doc_policy_page(driver).get_apply_domain_info()
            time.sleep(2)
            print(d_new_name)
            assert d_new_name == host
            # doc_policy_page(driver).unbind_domain(domain_name=host)  # 解绑文档域
            # time.sleep(3)
            # doc_policy_page(driver).delete_policy(policy_name=data[0])  # 删除策略
        # except Exception:
        #
        #     Domain_mgnt_home_page(driver).close_windows()
        #     raise

    @allure.step("添加子域和策略")
    @pytest.fixture(scope="function")
    def clear_PolicyAndDomain(self, driver, request, get_domain):
        host = request.config.getoption(name="--host")
        host = host.split('//')[1].split(':')[0]
        childhost = get_domain["parallel_domain"]
        CommonDocDomain().addRelationDomain(httphost=host, host=childhost, domaintype="child")  # 添加子域
        PolicyUUID = CommonDocDomain().addPolicy(httphost=host, name="上海爱数安全策略")  # 添加策略

        yield
        CommonDocDomain().clearRelationDomain(host=host)  # 解绑子域
        CommonDocDomain().deletepolicy(httphost=host, PolicyUUID=PolicyUUID)  # 删除策略
        Domain_mgnt_home_page(driver=driver).return_domain_home_page()  # 返回文档域管理界面
        time.sleep(2)

    @allure.testcase("caseid: 5506--策略绑定文档域弹窗检查")
    @pytest.mark.normal
    def test_apply_domain_interface_check(self, driver, get_domain, clear_PolicyAndDomain):
        # try:
            host = get_domain["parallel_domain"]
            el_apply = doc_policy_page(driver)
            Domain_mgnt_home_page(driver=driver).return_domain_home_page()  # 进入文档域管理界面
            time.sleep(2)
            Domain_mgnt_home_page(driver).policy_sync()  # 进入策略同步页面
            # data = do_excel(filename='add_policy.xlsx', sheetname='策略配置', minrow=2, maxrow=2, mincol=1, maxcol=3)[0]
            # doc_policy_page(driver).add_policy(policy_name=data[0], item=data[1])
            WebDriverWait(driver, 60).until(
               ec.element_to_be_clickable((By.XPATH, el_apply.el_add_domain_enable)))   # 等待添加文档域按钮可用
            driver.find_element_by_xpath(el_apply.el_add_domain).click()
            time.sleep(2)
            # 已选列表为空时，【清空】、【确定】按钮灰化
            el_clear_class = driver.find_element_by_xpath(el_apply.el_clear_button).get_attribute('class')
            assert el_clear_class.split("-")[-1] == "disabled"
            el_submit_class = driver.find_element_by_xpath(el_apply.el_submit_button).get_attribute('class')
            assert el_submit_class.split("-")[-1] == "disabled"
            # 搜索框的placeholder为搜索
            el_plac = driver.find_element_by_xpath(el_apply.el_applypop_search).get_attribute('placeholder')
            print(el_plac)
            assert el_plac == "搜索"

            '''
            已选列表不为空时的交互
            '''
            el_child = f"//a[span[@title='{host}']]"
            driver.find_element_by_xpath(el_child).click()
            time.sleep(2)
            # 点击【清空】按钮，列表为空
            driver.find_element_by_xpath(el_apply.el_clear_button).click()
            # 点击【x】
            driver.find_element_by_xpath(el_child).click()
            driver.find_element_by_xpath(el_apply.el_x).click()

            driver.find_element_by_xpath(el_apply.el_cancel).click()
            # doc_policy_page(driver).delete_policy(policy_name=data[0])  # 删除策略
        # except Exception:
        #
        #     Domain_mgnt_home_page(driver).close_windows()
        #     raise

    @allure.step("添加17个子域")
    @pytest.fixture(scope="function")
    def add_child_domain(self, driver, request):
        host = request.config.getoption(name="--host")
        host = host.split('//')[1].split(':')[0]
        db = DB_connect(host=host)
        # 添加子域
        for i in range(2):
            for j in range(6):
                sql = "insert into domain_mgnt.t_relationship_domain values('{}','{}',443,'','','child','','admin','eisoo.com',now())"
                print(str(i) + str(j))
                domainId = "9b04d18d-6c15-45a6-8c8c-6b8dc67" + str(i) + str(j)
                if i == 0:
                    domain_ip = "10.2.64." + str(i) + str(j)
                    domainSql = sql.format(domainId, domain_ip)
                    db.insert(domainSql)
                else:
                    domain_name = "child_domain" + str(i) + str(j)
                    domainSql = sql.format(domainId, domain_name)
                    db.insert(domainSql)
        # 添加一条策略
        insertDomain = "insert into domain_mgnt.t_policy_tpls values('1738f57a-dae5-400c-962d-5d6c691143d6','上海爱数安全策略','[]',now())"
        db.insert(insertDomain)
        for i in range(2):
            for j in range(6):
                policyId = "1738f57a-dae5-400c-962d-5d6c691143d6"
                domainId = "9b04d18d-6c15-45a6-8c8c-6b8dc67" + str(i) + str(j)
                insertDomain = "insert into domain_mgnt.t_policy_tpl_domains values('{}','{}')"
                domainSqls = insertDomain.format(policyId, domainId)
                db.insert(domainSqls)
        yield
        del_applydomain_sql = "delete from domain_mgnt.t_policy_tpl_domains where f_tpl_id = '1738f57a-dae5-400c-962d-5d6c691143d6'"
        del_childdomain_sql = "delete from domain_mgnt.t_relationship_domain where f_app_id = 'admin'"
        del_policy_sql = "delete from domain_mgnt.t_policy_tpls where f_name = '上海爱数安全策略'"
        db.delete(del_applydomain_sql)  # 解绑子域
        db.delete(del_policy_sql)  # 删除策略
        db.delete(del_childdomain_sql)  # 删除子域
        db.close()
        Domain_mgnt_home_page(driver=driver).return_domain_home_page()
        Domain_mgnt_home_page(driver).policy_sync()
        Domain_mgnt_home_page(driver=driver).return_domain_home_page()

    @allure.testcase("caseid：5530--策略配置--绑定文档域弹窗--搜索")
    @pytest.mark.normal
    @pytest.mark.wq
    def test_ApplyDomain_PopWind_search(self, driver, add_child_domain):
        # try:
            Domain_mgnt_home_page(driver).return_domain_home_page()
            Domain_mgnt_home_page(driver).policy_sync()
            el_apply = doc_policy_page(driver)
            WebDriverWait(driver, 60).until(
                ec.element_to_be_clickable((By.XPATH, el_apply.el_add_domain_enable)))
            driver.find_element_by_xpath(el_apply.el_add_domain_enable).click()
            time.sleep(3)
            assert doc_policy_page(driver).get_apply_domain_poplist_count() == 12
            # 检查搜索框
            search_input = driver.find_element_by_xpath(el_apply.el_applypop_search)
            WebDriverWait(driver, 60).until(
                ec.visibility_of_element_located((By.XPATH, el_apply.el_applypop_search)))
            el_plac = search_input.get_attribute('placeholder')
            assert el_plac == "搜索"
            # 输入无效关键字进行搜索
            search_input.send_keys("wang")
            input_keywords = search_input.get_attribute('value')
            assert input_keywords == "wang"
            time.sleep(2)
            WebDriverWait(driver, 60).until(
               ec.element_to_be_clickable((By.XPATH, el_apply.el_applypop_search_empty)))
            hint_text = driver.find_element_by_xpath(el_apply.el_applypop_search_empty).text
            assert hint_text == "抱歉，没有找到符合条件的结果"
            time.sleep(2)
            driver.find_element_by_xpath(el_apply.el_applypop_search_x).click()
            input_keywords = search_input.get_attribute('value')
            assert input_keywords != "wang"
            # 输入有效关键字进行搜索
            search_input.send_keys("64")
            time.sleep(3)
            assert doc_policy_page(driver).get_apply_domain_poplist_count() == 6
            driver.find_element_by_xpath(el_apply.el_applypop_search_x).click()
            search_input.send_keys("child")
            time.sleep(3)
            assert doc_policy_page(driver).get_apply_domain_poplist_count() == 6
            driver.find_element_by_xpath(el_apply.el_cancel).click()
        # except Exception:
        #
        #     Domain_mgnt_home_page(driver).close_windows()
        #     raise

    @allure.testcase("caseid: 5670--策略配置--绑定文档域--搜索")
    @pytest.mark.normal
    @pytest.mark.wq
    def test_ApplyDomain_List_search(self, driver, add_child_domain):
        # try:
            el_apply = doc_policy_page(driver)
            Domain_mgnt_home_page(driver).return_domain_home_page()
            Domain_mgnt_home_page(driver).policy_sync()
            time.sleep(3)
            search_input = driver.find_element_by_xpath(el_apply.el_applylist_search)
            plac_text = search_input.get_attribute('placeholder')
            assert plac_text == '搜索'
            # 输入无效关键字搜索
            search_input.send_keys('wang')
            search_keywords = search_input.get_attribute('value')
            assert search_keywords == 'wang'
            time.sleep(2)
            WebDriverWait(driver, 60).until(
               ec.element_to_be_clickable((By.XPATH, el_apply.el_applylist_search_empty)))
            list_text = driver.find_element_by_xpath(el_apply.el_applylist_search_empty).text
            assert list_text == '抱歉，没有找到符合条件的结果'
            driver.find_element_by_xpath(el_apply.el_applylist_search_x).click()
            time.sleep(1)
            search_keywords = search_input.get_attribute('value')
            assert search_keywords != 'wang'
            # 输入有效关键字搜索
            search_input.send_keys('64')
            time.sleep(2)
            list = driver.find_element_by_xpath(el_apply.el_apply_list)
            elements = list.find_elements_by_tag_name('tr')
            print(len(elements))
            assert len(elements) == 6
            driver.find_element_by_xpath(el_apply.el_applylist_search_x).click()
            time.sleep(1)
            search_input.send_keys('child')
            time.sleep(2)
            list = driver.find_element_by_xpath(el_apply.el_apply_list)
            elements = list.find_elements_by_tag_name('tr')
            print(len(elements))
            assert len(elements) == 6
            driver.find_element_by_xpath(el_apply.el_applylist_search_x).click()
        # except Exception:
        #
        #     Domain_mgnt_home_page(driver).close_windows()
        #     raise

    @allure.step("添加子域")
    @pytest.fixture(scope="function")
    def clear_childdomain(self, driver, request, get_domain):
        host = request.config.getoption(name="--host")
        host = host.split('//')[1].split(':')[0]
        childhost = get_domain["parallel_domain"]
        CommonDocDomain().addRelationDomain(httphost=host, host=childhost, domaintype="child")  # 添加子域

        yield
        CommonDocDomain().clearRelationDomain(host=host)  # 解绑子域
        Domain_mgnt_home_page(driver=driver).return_domain_home_page()  # 返回文档域管理界面
        time.sleep(2)

    @allure.testcase("caseid: 5520--策略配置--该文档域已绑定其他策略配置--添加文档域失败")
    @pytest.mark.high
    @pytest.mark.wq
    def test_childisbinding_bindfailure(self, driver, get_domain, clear_childdomain):
        # try:
            host = get_domain["parallel_domain"]
            applydomain = doc_policy_page(driver)
            Domain_mgnt_home_page(driver=driver).return_domain_home_page()  # 进入文档域管理界面
            Domain_mgnt_home_page(driver).policy_sync()    # 进入策略同步页面
            data = do_excel(filename='add_policy.xlsx', sheetname='策略配置', minrow=2, maxrow=3, mincol=1, maxcol=1)
            print(data)
            applydomain.add_policy(policy_name=data[0][0])
            WebDriverWait(driver, 60).until(
                ec.element_to_be_clickable((By.XPATH, applydomain.el_add_domain_enable)))
            applydomain.apply_domain(domain_name=host)
            time.sleep(2)
            print("策略绑定文档域成功！！！")
            applydomain.add_policy(policy_name=data[1][0])
            print("新增策略1成功！！！")
            applydomain.apply_domain(domain_name=host)
            WebDriverWait(driver, 60).until(
                ec.visibility_of_element_located((By.XPATH, applydomain.el_applydomain_hinticon)))
            poptext = driver.find_element_by_xpath(applydomain.el_applydomain_hinttext).text
            print(poptext)
            text = '文档域“{}”已绑定策略配置。'.format(host)
            assert poptext == text
            driver.find_element_by_xpath(applydomain.el_hintpop_confirm).click()
            driver.find_element_by_xpath(applydomain.el_cancel).click()
            # 删除策略
            applydomain.delete_policy(policy_name=data[1][0])
            applydomain.unbind_domain(domain_name=host)
            time.sleep(3)
            applydomain.delete_policy(policy_name=data[0][0])
        # except Exception:
        #
        #     Domain_mgnt_home_page(driver).close_windows()
        #     raise

    @allure.testcase("caseid: 5524--策略配置--文档域已被删除--添加文档域失败")
    @pytest.mark.high
    @pytest.mark.wq
    def test_childbedel_bindfailure(self, driver, get_domain, request):
        # try:
            # 添加子域
            Domain_mgnt_home_page(driver=driver).return_domain_home_page()
            host = request.config.getoption(name="--host")
            host = host.split('//')[1].split(':')[0]
            uuid = CommonDocDomain().addRelationDomain(httphost=host, domaintype="child",
                                                       host=get_domain["parallel_domain"])
            # 添加策略
            applydomain = doc_policy_page(driver)
            Domain_mgnt_home_page(driver).policy_sync()
            data = do_excel(filename='add_policy.xlsx', sheetname='策略配置', minrow=2, maxrow=3, mincol=1, maxcol=1)
            applydomain.add_policy(policy_name=data[0][0])
            WebDriverWait(driver, 60).until(
                ec.element_to_be_clickable((By.XPATH, applydomain.el_add_domain_enable)))
            driver.find_element_by_xpath(applydomain.el_add_domain_enable).click()
            el_child = "//a[span[@title='{}']]".format(get_domain["parallel_domain"])
            print(el_child)
            driver.find_element_by_xpath(el_child).click()
            time.sleep(2)
            # 调用接口删除子域
            CommonDocDomain().delRelationDomain(host=host, uuid=uuid)
            time.sleep(2)
            driver.find_element_by_xpath(applydomain.is_submit).click()
            # 提示“文档域XXX已不存在”
            WebDriverWait(driver, 60).until(
                ec.visibility_of_element_located((By.XPATH, applydomain.el_applydomain_hinticon)))
            poptext = driver.find_element_by_xpath(applydomain.el_applydomain_hinttext).text
            print(poptext)
            text = '文档域“{}”已不存在。'.format(get_domain["parallel_domain"])
            assert poptext == text
            driver.find_element_by_xpath(applydomain.el_hintpop_confirm).click()
            driver.find_element_by_xpath(applydomain.el_cancel).click()
            # 删除策略
            applydomain.delete_policy(policy_name=data[0][0])
            Domain_mgnt_home_page(driver=driver).return_domain_home_page()
            time.sleep(2)
        # except Exception:
        #
        #     Domain_mgnt_home_page(driver).close_windows()
        #     raise
    @allure.testcase("caseid: 5537--策略同步--策略已被删除--点击【编辑】")
    @pytest.mark.normal
    @pytest.mark.wq
    def test_edit_policy(self, driver, request):
        # try:
            policy_page = doc_policy_page(driver)
            host = request.config.getoption(name="--host")
            host = host.split('//')[1].split(':')[0]
            db = DB_connect(host=host)
            insertDomain = "insert into domain_mgnt.t_policy_tpls values('1738f57a-dae5-400c-962d-5d6c691143d6','上海爱数安全策略','[]',now())"
            db.insert(insertDomain)
            Domain_mgnt_home_page(driver=driver).return_domain_home_page()
            Domain_mgnt_home_page(driver=driver).policy_sync()
            policy_info = doc_policy_page(driver=driver).get_policy_info()
            assert policy_info == '上海爱数安全策略'
            # 删除策略
            UUID = '1738f57a-dae5-400c-962d-5d6c691143d6'
            CommonDocDomain().deletepolicy(httphost=host, PolicyUUID=UUID)
            time.sleep(2)
            # 编辑已删除的策略--toast提示
            driver.find_element_by_xpath(policy_page.el_edit_policy).click()
            WebDriverWait(driver, 20).until(
                ec.presence_of_element_located((By.XPATH, policy_page.el_edit_policy_not_exist)))  # 验证气泡提示是否出现
            text = driver.find_element_by_xpath(policy_page.el_edit_policy_not_exist).text
            print(text)
            assert text == '该策略配置已不存在。'
            list_text = driver.find_element_by_xpath(policy_page.el_list_is_null).text
            assert list_text == '列表为空'
        # except Exception:
        #
        #     Domain_mgnt_home_page(driver).close_windows()
        #     raise
    @allure.testcase("caseid: 5529--策略同步--已绑定文档域--添加文档域弹窗检查")
    @pytest.mark.high
    @pytest.mark.wq
    def test_boundpolicy_interface_check(self, driver, get_domain, clear_PolicyAndDomain):
        # try:
            host = get_domain['parallel_domain']
            policy_page = doc_policy_page(driver)
            Domain_mgnt_home_page(driver=driver).return_domain_home_page()  # 进入文档域管理界面
            time.sleep(2)
            Domain_mgnt_home_page(driver=driver).policy_sync()   # 进入策略同步页面
            # data = do_excel(filename='add_policy.xlsx', sheetname='策略配置', minrow=2, maxrow=2, mincol=1, maxcol=3)[0]
            # doc_policy_page(driver).add_policy(policy_name=data[0], item=data[1])
            # time.sleep(2)
            doc_policy_page(driver).apply_domain(domain_name=host)
            time.sleep(2)
            driver.find_element_by_xpath(policy_page.el_add_domain_enable).click()
            time.sleep(2)
            # 已选列表为空，【清空】、【确定】按钮灰化
            el_clear_class = driver.find_element_by_xpath(policy_page.el_clear_button).get_attribute('class')
            assert el_clear_class.split("-")[-1] == "disabled"
            el_submit_class = driver.find_element_by_xpath(policy_page.el_submit_button).get_attribute('class')
            assert el_submit_class.split("-")[-1] == "disabled"
            # 选择已被该策略绑定的子域
            el_child = "//a[span[@title='{}']]".format(host)
            driver.find_element_by_xpath(el_child).click()
            time.sleep(2)
            driver.find_element_by_xpath(policy_page.is_submit).click()
            # 断言列表无重复数据
            value = driver.find_element_by_xpath(policy_page.el_page_count_apply).text
            print(value)
            assert value == "显示 1 - 1 条，共 1 条"
            time.sleep(2)
            doc_policy_page(driver).unbind_domain(domain_name=host, is_submit=True)
            time.sleep(2)
            # doc_policy_page(driver).delete_policy(policy_name=data[0])  # 删除策略
        # except Exception:
        #
        #     Domain_mgnt_home_page(driver).close_windows()
        #     raise

    @allure.testcase("caseid: 5526--策略同步--文档域已被添加为平级域--添加文档域失败")
    @pytest.mark.high
    @pytest.mark.wq
    def test_applydomain_failure(self, driver, request, get_domain, clear_PolicyAndDomain):
        # try:
            host = get_domain['parallel_domain']
            policy_page = doc_policy_page(driver)
            Domain_mgnt_home_page(driver=driver).return_domain_home_page()  # 进入文档域管理界面
            time.sleep(2)
            Domain_mgnt_home_page(driver=driver).policy_sync()  # 进入策略同步页面
            # data = do_excel(filename='add_policy.xlsx', sheetname='策略配置', minrow=2, maxrow=2, mincol=1, maxcol=3)[0]
            # doc_policy_page(driver).add_policy(policy_name=data[0], item=data[1])
            time.sleep(2)
            driver.find_element_by_xpath(policy_page.el_add_domain_enable).click()
            el_child = "//a[span[@title='{}']]".format(host)
            driver.find_element_by_xpath(el_child).click()
            time.sleep(2)
            # 将子域设置为平级域
            ip = request.config.getoption(name="--host")
            ip = ip.split(":8000")[0].split("https://")[1]
            res = CommonDocDomain().getRelationDomainList(host=ip)
            uuid = res['data'][0]["id"]
            CommonDocDomain().delRelationDomain(host=ip, uuid=uuid)
            CommonDocDomain().addRelationDomain(httphost=ip, host=host, domaintype='parallel', network_type="indirect")  # 添加平级域
            time.sleep(2)
            driver.find_element_by_xpath(policy_page.is_submit).click()
            WebDriverWait(driver, 20).until(
                ec.visibility_of_element_located((By.XPATH, policy_page.el_applydomain_hinticon)))
            poptext = driver.find_element_by_xpath(policy_page.el_applydomain_hinttext).text
            print(poptext)
            text = '文档域“{}”已不存在。'.format(host)
            assert poptext == text
            driver.find_element_by_xpath(policy_page.el_hintpop_confirm).click()
            driver.find_element_by_xpath(policy_page.el_cancel).click()
            # # 删除策略
            # doc_policy_page(driver).delete_policy(policy_name=data[0])  # 删除策略
            # Domain_mgnt_home_page(driver=driver).return_domain_home_page()
            time.sleep(2)
        # except Exception:
        #
        #     Domain_mgnt_home_page(driver).close_windows()
        #     raise
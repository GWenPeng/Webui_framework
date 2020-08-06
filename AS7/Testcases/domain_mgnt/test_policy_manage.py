# coding=utf-8
from AS7.Pages.Domain_mgnt.domain_mgnt_home_page import Domain_mgnt_home_page
from AS7.Pages.Domain_mgnt.domain_mgnt_page import Domain_mgnt_page
from AS7.Pages.Domain_mgnt.doc_policy_page import doc_policy_page
from selenium.webdriver.common.action_chains import ActionChains
from AS7.Pages.Login_page import Login_page
from AS7.Pages.Client_login_page import ClientLoginPage
from AS7.Pages.Domain_mgnt.CommonDocDomain import CommonDocDomain
from AS7.Pages.Organizations.users_mgnt.users_org_mgnt_page import user_mgnt_module
from Common.parse_data import do_excel
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from Common.screenshot import ScreenShot

# from Common.screenshot import Screen_shot
from Common.mysqlconnect import DB_connect
from Common.thrift_client import Thrift_client
from ShareMgnt import ncTShareMgnt

import pytest
import allure
import time


@pytest.mark.jt_suite
class TestPolicyManage:

    @pytest.fixture(scope="function")
    def clear_data(self, request, get_domain):
        yield
        host1 = request.config.getoption(name="--host")
        host1 = host1.split('//')[1].split(':')[0]
        db = DB_connect(host=host1)

        delete_policy_sql1 = "delete from domain_mgnt.t_policy_tpls where f_name = '上海爱数'"
        delete_policy_sql2 = "delete from domain_mgnt.t_policy_tpls where f_name = 'SHANGHAI'"
        delete_policy_sql3 = "delete from domain_mgnt.t_policy_tpls where f_name = '安全策略'"
        delete_policy_sql4 = "delete from domain_mgnt.t_policy_tpls where f_name = '上海爱数安全策略'"
        db.delete(delete_policy_sql1)  # 删除策略
        db.delete(delete_policy_sql2)  # 删除策略
        db.delete(delete_policy_sql3)  # 删除策略
        db.delete(delete_policy_sql4)  # 删除策略

        select_policy = "select * from domain_mgnt.t_policy_tpls where f_name = 'SH爱数'"
        policy = db.select_one(select_policy)
        print(policy)
        if policy is not None:
            policy_data = CommonDocDomain().getPolicyIDNameByKeyword(httphost=host1, key_word="SH爱数")
            policy_id = policy_data["data"][0]["id"]  # 获取策略ID
            domain_data = CommonDocDomain().getRelationDomainList(host=host1, keyword="10.2.181.55")
            domain_id = domain_data["data"][0]["id"]  # 获取子域ID
            CommonDocDomain().delboundPolicy(httphost=host1, PolicyUUID=policy_id, ChildDomainUUID=domain_id)  # 子域解绑策略
            CommonDocDomain().deletepolicy(httphost=host1, PolicyUUID=policy_id)  # 本域删除策略
            CommonDocDomain().delRelationDomain(host=host1, uuid=domain_id)  # 本域删除子域

        host = get_domain["replace_domain"]
        db1 = DB_connect(host=host)
        select_policy = "select * from sharemgnt_db.t_user where f_login_name = 'a'"
        user_infor = db1.select_one(select_policy)
        print(user_infor)

        if user_infor is not None:
            user_id = user_infor[0]
            CommonDocDomain().close_person_doc(user_id=user_id, host=host)  # 关闭用户个人文档库
            CommonDocDomain().del_user(user_id=user_id, host=host)  # 删除用户
        update_sql = "UPDATE sharemgnt_db.t_third_party_auth SET f_enable = '0' WHERE f_app_name = '第三方集成测试'"
        db1.update(update_sql)  # 关闭第三方认证集成

    @allure.testcase("caseid:5495,添加策略配置失败--策略配置名称输入为空")
    @pytest.mark.normal
    def test_policy_name_empty(self, driver, clear_data):
        # try:
            time.sleep(3)
            Domain_mgnt_home_page(driver).return_domain_home_page()  # 进入文档域管理
            Domain_mgnt_home_page(driver).policy_sync()  # 进入策略同步
            driver.refresh()
            add_policy = doc_policy_page(driver).el_add_policy
            WebDriverWait(driver, 60).until(ec.visibility_of_element_located((
                By.XPATH, add_policy)))  # 等待新增策略按钮出现
            driver.find_element_by_xpath(add_policy).click()  # 点击新增策略按钮

            policy_name = doc_policy_page(driver).el_policy_name
            confirm_button = doc_policy_page(driver).el_confirm_button
            driver.find_element_by_xpath(confirm_button).click()  # 点击[确定]按钮
            driver.find_element_by_xpath(policy_name).click()  # 点击输入框
            policy_name_empty_hint = doc_policy_page(driver).el_policy_name_empty_hint
            hint = driver.find_element_by_xpath(policy_name_empty_hint)  # 定位气泡提示
            action = ActionChains(driver=driver)
            action.move_to_element(hint).perform()  # 鼠标悬浮提示
            hint = driver.find_element_by_xpath(policy_name_empty_hint).text
            assert hint == "此输入项不允许为空。"   # 断言气泡提示

            driver.find_element_by_xpath(policy_name).send_keys(" ")  # 策略名称输入空格
            driver.find_element_by_xpath(confirm_button).click()  # 点击确定按钮
            driver.find_element_by_xpath(policy_name).click()  # 点击输入框
            action2 = ActionChains(driver=driver)
            policy_name_empty_hint = doc_policy_page(driver).el_policy_name_empty_hint
            hint2 = driver.find_element_by_xpath(policy_name_empty_hint)
            action2.move_to_element(hint2).perform()  # 鼠标悬浮提示
            hint2 = driver.find_element_by_xpath(policy_name_empty_hint).text
            assert hint2 == "此输入项不允许为空。"  # 断言气泡提示

            cancel_button = doc_policy_page(driver).el_cancel_button
            driver.find_element_by_xpath(cancel_button).click()  # 点击【取消】按钮
            Domain_mgnt_home_page(driver).return_domain_home_page()  # 进入文档域管理
        # except Exception:
        #
        #     Domain_mgnt_home_page(driver).close_windows()
        #     raise

    @allure.testcase("caseid:5496，添加策略配置--策略配置名称已存在")
    @pytest.mark.normal
    def test_policy_name_exist(self, driver, clear_data):
        # try:
            Domain_mgnt_home_page(driver).return_domain_home_page()  # 进入文档域管理
            Domain_mgnt_home_page(driver).policy_sync()  # 进入策略同步
            add_policy = doc_policy_page(driver).el_add_policy
            WebDriverWait(driver, 60).until(ec.visibility_of_element_located((
                By.XPATH, add_policy)))  # 等待新增策略按钮出现

            doc_policy_page(driver).add_policy(policy_name='上海爱数')  # 新增策略
            time.sleep(3)
            driver.find_element_by_xpath(add_policy).click()  # 点击新增策略按钮
            policy_name = doc_policy_page(driver).el_policy_name
            driver.find_element_by_xpath(policy_name).send_keys("上海爱数")
            confirm_button = doc_policy_page(driver).el_confirm_button
            driver.find_element_by_xpath(confirm_button).click()  # 点击确定按钮
            policy_name_exist_button = doc_policy_page(driver).el_policy_name_exist_button
            exist_button = driver.find_element_by_xpath(policy_name_exist_button)
            exist_button.click()  # 点击提示弹窗确定按钮
            Domain_mgnt_page(driver).clear_input(driver.find_element_by_xpath(policy_name))  # 清空策略名称输入框
            driver.find_element_by_xpath(policy_name).send_keys("SHANGHAI")  # 策略名称输入“SHANGHAI”
            driver.find_element_by_xpath(confirm_button).click()  # 点击确定按钮
            time.sleep(2)
            policy_first = doc_policy_page(driver).el_policy_first
            first_policy_name = driver.find_element_by_xpath(policy_first).text
            assert first_policy_name == "SHANGHAI"  # 断言策略是否创建成功
            doc_policy_page(driver).delete_policy("上海爱数")
            doc_policy_page(driver).delete_policy("SHANGHAI")
            Domain_mgnt_home_page(driver).return_domain_home_page()  # 进入文档域管理
        # except Exception:
        #
        #     Domain_mgnt_home_page(driver).close_windows()
        #     raise

    @allure.testcase("caseid:5497,添加策略配置失败--策略配置名称输入不合法 ")
    @pytest.mark.normal
    def test_policy_name_illegal(self, driver, clear_data):
        # try:
            Domain_mgnt_home_page(driver).return_domain_home_page()  # 进入文档域管理
            Domain_mgnt_home_page(driver).policy_sync()  # 进入策略同步
            add_policy = doc_policy_page(driver).el_add_policy
            WebDriverWait(driver, 60).until(ec.visibility_of_element_located((
                By.XPATH, add_policy)))  # 等待新增策略按钮出现
            driver.find_element_by_xpath(add_policy).click()  # 点击新增策略按钮
            policy_name = doc_policy_page(driver).el_policy_name
            driver.find_element_by_xpath(policy_name).send_keys("&*&<>策略配置")
            confirm_button = doc_policy_page(driver).el_confirm_button
            driver.find_element_by_xpath(confirm_button).click()  # 点击确定按钮
            driver.find_element_by_xpath(policy_name).click()  # 点击输入框
            action1 = ActionChains(driver=driver)
            policy_name_illegal_hint = doc_policy_page(driver).el_policy_name_illegal_hint
            hint = driver.find_element_by_xpath(policy_name_illegal_hint)
            action1.move_to_element(hint).perform()  # 鼠标悬浮提示
            hint1 = driver.find_element_by_xpath(policy_name_illegal_hint).text
            assert hint1 == "只允许包含英文特殊字符：~!%#$@-_. ，长度范围 1~100 个字符。"  # 断言气泡提示
            Domain_mgnt_page(driver).clear_input(driver.find_element_by_xpath(policy_name))  # 清空策略名称输入框
            driver.find_element_by_xpath(policy_name).send_keys("&*&<>qqq123")
            confirm_button = doc_policy_page(driver).el_confirm_button
            driver.find_element_by_xpath(confirm_button).click()  # 点击确定按钮
            driver.find_element_by_xpath(policy_name).click()  # 点击输入框
            action2 = ActionChains(driver=driver)
            hint = driver.find_element_by_xpath(policy_name_illegal_hint)
            action2.move_to_element(hint).perform()  # 鼠标悬浮提示
            hint2 = driver.find_element_by_xpath(policy_name_illegal_hint).text
            assert hint2 == "只允许包含英文特殊字符：~!%#$@-_. ，长度范围 1~100 个字符。"  # 断言气泡提示
            Domain_mgnt_page(driver).clear_input(driver.find_element_by_xpath(policy_name))  # 清空策略名称输入框
            driver.find_element_by_xpath(policy_name).send_keys("δ")
            confirm_button = doc_policy_page(driver).el_confirm_button
            driver.find_element_by_xpath(confirm_button).click()  # 点击确定按钮
            driver.find_element_by_xpath(policy_name).click()  # 点击输入框
            action3 = ActionChains(driver=driver)
            hint = driver.find_element_by_xpath(policy_name_illegal_hint)
            action3.move_to_element(hint).perform()  # 鼠标悬浮提示
            hint3 = driver.find_element_by_xpath(policy_name_illegal_hint).text
            assert hint3 == "只允许包含英文特殊字符：~!%#$@-_. ，长度范围 1~100 个字符。"  # 断言气泡提示
            el_cancel_button = doc_policy_page(driver).el_cancel_button
            driver.find_element_by_xpath(el_cancel_button).click()  # 点击【取消】按钮
            Domain_mgnt_home_page(driver).return_domain_home_page()  # 进入文档域管理
        # except Exception:
        #
        #     Domain_mgnt_home_page(driver).close_windows()
        #     raise

    @allure.testcase("caseid:5498,文档域策略同步--未启用策略配置--添加策略配置成功 ")
    @pytest.mark.high
    def test_add_policy_success(self, driver, clear_data):
        # try:
            Domain_mgnt_home_page(driver).return_domain_home_page()  # 进入文档域管理
            Domain_mgnt_home_page(driver).policy_sync()  # 进入策略同步
            add_policy = doc_policy_page(driver).el_add_policy
            WebDriverWait(driver, 60).until(ec.visibility_of_element_located((
                By.XPATH, add_policy)))  # 等待新增策略按钮出现
            name = ["哈", "qwertyuiopasdfg12345",
                    "qwertyuiopasdfg12345qwertyuiopasdfg12345qwertyuiopasdfg12345qwertyuiopasdfg12345qwertyuiopasdfg12345",
                    "~!%#$@-_.上海爱数策略配置", "SH   123策略配置", "shanghai安全策略"]

            for i in range(0, 5):
                doc_policy_page(driver).add_policy(policy_name=name[i])  # 新增策略
                time.sleep(2)
                list_null = doc_policy_page(driver).el_list_is_null
                list_is_null = driver.find_element_by_xpath(list_null).text
                assert list_is_null == "列表为空"  # 断言列表提示
                policy_first = doc_policy_page(driver).el_policy_first
                first_policy_name = driver.find_element_by_xpath(policy_first).text
                assert first_policy_name == name[i]  # 断言策略是否创建成功
                add_domain_button = doc_policy_page(driver).el_add_domain_enable
                add_domain_button_enable = driver.find_element_by_xpath(add_domain_button).get_attribute("class")
                assert add_domain_button_enable.split("-")[-1] != "disabled"  # 断言添加文档域按钮为可用

            for n in range(0, 5):
                doc_policy_page(driver).delete_policy(name[n])  # 删除策略
            Domain_mgnt_home_page(driver).return_domain_home_page()  # 进入文档域管理
        # except Exception:
        #
        #     Domain_mgnt_home_page(driver).close_windows()
        #     raise

    @allure.testcase("caseid:5505,策略同步--添加策略配置弹窗--搜索 ")
    @pytest.mark.high
    def test_add_policy_search(self, driver, clear_data):
        # try:
            Domain_mgnt_home_page(driver).return_domain_home_page()  # 进入文档域管理
            Domain_mgnt_home_page(driver).policy_sync()  # 进入策略同步
            add_policy = doc_policy_page(driver).el_add_policy
            WebDriverWait(driver, 60).until(ec.visibility_of_element_located((
                By.XPATH, add_policy)))  # 等待新增策略按钮出现
            driver.find_element_by_xpath(add_policy).click()  # 点击新增策略按钮
            add_policy_search = doc_policy_page(driver).el_add_policy_search
            add_policy_search_value = driver.find_element_by_xpath(add_policy_search).get_attribute("value")
            assert add_policy_search_value == ""  # 断言搜索框值默认为空
            time.sleep(3)
            add_policy_search_placeholder = driver.find_element_by_xpath(add_policy_search).get_attribute("placeholder")
            assert add_policy_search_placeholder == "搜索"  # 断言搜索框内占位符
            time.sleep(3)
            driver.find_element_by_xpath(add_policy_search).send_keys("123")  # 搜索框输入关键字“123”
            time.sleep(3)
            el_search_empty = doc_policy_page(driver).el_add_policy_search_empty
            search_empty_status = driver.find_element_by_xpath(el_search_empty).get_attribute("class")
            assert search_empty_status.split("-")[-1] != "disabled"  # 断言清空按钮可用
            time.sleep(3)
            el_list_no_search_results = doc_policy_page(driver).el_list_no_search_results
            list_no_search_results = driver.find_element_by_xpath(el_list_no_search_results).text
            assert list_no_search_results == "抱歉，没有找到符合条件的结果"
            time.sleep(3)
            Domain_mgnt_page(driver).clear_input(driver.find_element_by_xpath(add_policy_search))  # 清空搜索输入框
            driver.find_element_by_xpath(add_policy_search).send_keys("密码")  # 搜索框输入关键字“密码”
            time.sleep(3)
            search_empty_status = driver.find_element_by_xpath(el_search_empty).get_attribute("class")
            assert search_empty_status.split("-")[-1] != "disabled"  # 断言清空按钮可用
            time.sleep(3)
            policy = doc_policy_page(driver).get_policy(1, "密码强度")
            policy_name = driver.find_element_by_xpath(policy).text
            assert policy_name == "密码强度"
            driver.find_element_by_xpath(add_policy_search).click()  # 清空搜索输入框
            el_cancel_button = doc_policy_page(driver).el_cancel_button
            driver.find_element_by_xpath(el_cancel_button).click()  # 点击【取消】按钮
            Domain_mgnt_home_page(driver).return_domain_home_page()  # 进入文档域管理
        # except Exception:
        #
        #     Domain_mgnt_home_page(driver).close_windows()
        #     # driver.find_element_by_xpath(doc_policy_page(driver).el_cancel_button).click()  # 点击【取消】按钮
        #     Domain_mgnt_home_page(driver).return_domain_home_page()  # 进入文档域管理
        #     raise

    @allure.testcase("caseid:5539,策略同步--删除策略配置--已绑定文档域 ")
    @pytest.mark.normal
    def test_delete_policy(self, driver, get_domain, clear_data):
        # try:
            Domain_mgnt_home_page(driver).return_domain_home_page()  # 进入文档域管理
            Domain_mgnt_page(driver).add_domain(domain_name=get_domain['replace_domain'], appid='1', appkey='1')  # 添加子域
            Domain_mgnt_home_page(driver).policy_sync()  # 进入策略同步
            time.sleep(3)
            doc_policy_page(driver).add_policy(policy_name='上海爱数')  # 新增策略
            time.sleep(3)
            doc_policy_page(driver).apply_domain(domain_name=get_domain['replace_domain'])  # 策略绑定子域
            time.sleep(3)
            doc_policy_page(driver).delete_policy_fail("上海爱数")
            Domain_mgnt_home_page(driver).return_domain_home_page()  # 进入文档域管理
            time.sleep(3)
            Domain_mgnt_page(driver).remove_binding_by_index()  # 解除绑定
            time.sleep(2)
            Domain_mgnt_page(driver).delete_domain()  # 删除子域
            time.sleep(2)
            Domain_mgnt_home_page(driver).policy_sync()  # 进入策略同步
            time.sleep(2)
            doc_policy_page(driver).delete_policy("上海爱数")  # 删除策略
        # except Exception:
        #
        #     Domain_mgnt_home_page(driver).close_windows()
        #     raise

    @allure.testcase("caseid:5667,策略同步--策略配置--搜索 ")
    @pytest.mark.normal
    def test_policy_search(self, driver, get_domain, clear_data):
        # try:
            Domain_mgnt_home_page(driver).return_domain_home_page()  # 进入文档域管理
            Domain_mgnt_home_page(driver).policy_sync()  # 进入策略同步
            time.sleep(3)
            doc_policy_page(driver).add_policy(policy_name="上海爱数")
            time.sleep(3)
            doc_policy_page(driver).add_policy(policy_name="安全策略")  # 新增策略
            policy_search_value = driver.find_element_by_xpath(doc_policy_page(driver).el_policy_search).get_attribute("value")
            assert policy_search_value == ""  # 断言输入框默认值
            policy_search_placeholder = driver.find_element_by_xpath(doc_policy_page(driver).el_policy_search).get_attribute("placeholder")
            assert policy_search_placeholder == "搜索"  # 断言搜索框内占位符
            search = driver.find_element_by_xpath(doc_policy_page(driver).el_policy_search)  # 输入无效关键字
            time.sleep(3)
            search.send_keys("123")
            time.sleep(1)
            policy_search_empty_status = driver.find_element_by_xpath(doc_policy_page(driver).el_policy_search_empty).get_attribute("class")
            assert policy_search_empty_status.split("-")[-1] != "disabled"  # 断言清空按钮可用
            time.sleep(3)
            list_no_search_results = driver.find_element_by_xpath(doc_policy_page(driver).el_list_no_search_results).text
            assert list_no_search_results == "抱歉，没有找到符合条件的结果"
            Domain_mgnt_page(driver).clear_input(driver.find_element_by_xpath(doc_policy_page(driver).el_policy_search))  # 清空搜索框
            driver.find_element_by_xpath(doc_policy_page(driver).el_policy_search).send_keys("安全")  # 输入关键字
            time.sleep(3)
            policy_name = doc_policy_page(driver).get_policy_info()
            assert policy_name == "安全策略"
            driver.find_element_by_xpath(doc_policy_page(driver).el_policy_search_empty).click()
            time.sleep(3)
            policy_search_value = driver.find_element_by_xpath(doc_policy_page(driver).el_policy_search).get_attribute(
                "value")
            assert policy_search_value == ""  # 断言输入框值
            doc_policy_page(driver).delete_policy("上海爱数")
            doc_policy_page(driver).delete_policy("安全策略")  # 删除策略
            Domain_mgnt_home_page(driver).return_domain_home_page()  # 进入文档域管理
        # except Exception:
        #
        #     Domain_mgnt_home_page(driver).close_windows()
        #     raise

    @allure.testcase("caseid:5677,文档库策略同步--编辑策略配置 ")
    @pytest.mark.normal
    def test_edit_policy(self, driver,request, get_domain, clear_data):
        host = get_domain["replace_domain"]
        # try:
        host1 = request.config.getoption(name="--host")
        host1 = host1.split('//')[1].split(':')[0]
        Domain_mgnt_home_page(driver).return_domain_home_page()  # 进入文档域管理
        Domain_mgnt_page(driver).add_domain(domain_name=get_domain['replace_domain'], appid='1', appkey='1')  # 添加子域
        Domain_mgnt_home_page(driver).policy_sync()  # 进入策略同步
        time.sleep(1)
        doc_policy_page(driver).add_policy(policy_name='上海爱数', item="pwd_strength", enable=True, strength="strong")  # 新增策略
        time.sleep(1)
        doc_policy_page(driver).apply_domain(domain_name=get_domain['replace_domain'])  # 策略绑定子域
        time.sleep(1)
        doc_policy_page(driver).edit_policy(policy_name="上海爱数", edit_policy_name="SH爱数", enable=True,
                                            item="pwd_strength")
        time.sleep(1)
        policy_name = doc_policy_page(driver).get_policy_info()
        assert policy_name == "SH爱数"
        driver.get(f'https://{host}:8000')
        Login_page(driver).login(username="admin", password="eisoo.com")  # 进入子域检查
        time.sleep(3)
        driver.find_element_by_xpath(doc_policy_page(driver).el_security_tab).click()
        time.sleep(2)
        pwd_strength_status = driver.find_element_by_xpath(doc_policy_page(driver).el_security_pwd_strength).get_attribute("disabled")
        assert pwd_strength_status == "true"
        time.sleep(2)

        driver.get(f'https://{host1}:8000')
        Login_page(driver).login(username="admin", password="eisoo.com")  # 返回本域
        Domain_mgnt_home_page(driver).return_domain_home_page()  # 进入文档域管理
        policy_data = CommonDocDomain().getPolicyIDNameByKeyword(httphost=host1, key_word="SH爱数")
        policy_id = policy_data["data"][0]["id"]  # 获取策略ID
        domain_data = CommonDocDomain().getRelationDomainList(host=host1, keyword="10.2.181.55")
        domain_id = domain_data["data"][0]["id"]  # 获取子域ID
        CommonDocDomain().delboundPolicy(httphost=host1, PolicyUUID=policy_id, ChildDomainUUID=domain_id)  # 子域解绑策略
        CommonDocDomain().deletepolicy(httphost=host1, PolicyUUID=policy_id)    # 本域删除策略
        CommonDocDomain().delRelationDomain(host=host1, uuid=domain_id)   # 本域删除子域

        # except Exception:
        #
        #     Domain_mgnt_home_page(driver).close_windows()
        #     raise

    @allure.testcase("caseid:5965，配置策略--设置账号密码+短信验证码登录 ")
    @pytest.mark.high
    def test_edit_policy_code(self, driver, request, get_domain, clear_data):
        host = get_domain["replace_domain"]
        # try:
        host1 = request.config.getoption(name="--host")
        f_host = host1.split('//')[1].split(':')[0]
        Domain_mgnt_home_page(driver).return_domain_home_page()  # 进入文档域管理
        Domain_mgnt_page(driver).add_domain(domain_name=get_domain['replace_domain'], appid='1', appkey='1')  # 添加子域
        Domain_mgnt_home_page(driver).policy_sync()  # 进入策略同步
        time.sleep(1)
        doc_policy_page(driver).add_policy_with_auth(policy_name="上海爱数", enable="enable", option="账号密码 + 短信验证码")
        time.sleep(1)
        doc_policy_page(driver).apply_domain(domain_name=get_domain['replace_domain'])  # 策略绑定子域
        time.sleep(1)
        driver.get(f'https://{host}:8000')
        Login_page(driver).login(username="admin", password="eisoo.com")  # 进入子域检查
        time.sleep(3)
        driver.find_element_by_xpath(doc_policy_page(driver).el_security_tab).click()
        time.sleep(2)
        login_select_status = driver.find_element_by_xpath(doc_policy_page(driver).el_login_select).get_attribute("class")
        assert login_select_status.split("-")[-1] == "disabled"
        login_auth = driver.find_element_by_xpath(doc_policy_page(driver).el_login_auth).text
        assert login_auth == "账号密码 + 短信验证码"
        time.sleep(2)
        driver.get(f'https://{f_host}:8000')
        Login_page(driver).login(username="admin", password="eisoo.com")  # 返回本域
        time.sleep(2)
        Domain_mgnt_home_page(driver).return_domain_home_page()  # 进入文档域管理
        Domain_mgnt_home_page(driver).policy_sync()  # 进入策略同步
        time.sleep(1)
        doc_policy_page(driver).edit_policy(policy_name="上海爱数", item="two_factor_auth", enable="enable", option="账号密码")
        time.sleep(1)
        doc_policy_page(driver).unbind_domain(domain_name=host)

        policy_data = CommonDocDomain().getPolicyIDNameByKeyword(httphost=f_host, key_word="上海爱数")
        policy_id = policy_data["data"][0]["id"]  # 获取策略ID
        domain_data = CommonDocDomain().getRelationDomainList(host=f_host, keyword=host)
        domain_id = domain_data["data"][0]["id"]  # 获取子域ID
        CommonDocDomain().deletepolicy(httphost=f_host, PolicyUUID=policy_id)  # 本域删除策略
        CommonDocDomain().delRelationDomain(host=f_host, uuid=domain_id)  # 本域删除子域
        time.sleep(2)
        Domain_mgnt_home_page(driver).return_domain_home_page()  # 进入文档域管理

        # except Exception:
        #
        #     Domain_mgnt_home_page(driver).close_windows()
        #     raise

    @pytest.mark.skip(reason='需要在客户端登陆')
    @allure.testcase("caseid:5966,文档域策略同步--设置账号密码+短信验证码--用户登录 ")
    @pytest.mark.high
    def test_edit_policy_client(self, driver, request, get_domain, clear_data):
        host = get_domain["replace_domain"]
        # try:
        host1 = request.config.getoption(name="--host")
        f_host = host1.split('//')[1].split(':')[0]
        Domain_mgnt_home_page(driver).return_domain_home_page()  # 进入文档域管理

        try:
            driver.get(f'https://{host}:8000')
            Login_page(driver).login(username="admin", password="eisoo.com")  # 进入子域
            time.sleep(3)
            user_mgnt_module(driver).create_user(username="a", showname="a", mobile="12345678912")  # 新建用户
            time.sleep(2)
            user_mgnt_module(driver).control_pwd(user_name="a", allow="not", pwd="eisoo.com")  # 管控用户密码
            db1 = DB_connect(host=host)
            third_open_sql = "UPDATE sharemgnt_db.t_third_party_auth SET f_enable = '1' WHERE f_app_name = '第三方集成测试'"
            db1.update(third_open_sql)  # 开启第三方认证集成
            time.sleep(1)

        except Exception as e:
            driver.get(f'https://{f_host}:8000')
            Login_page(driver).login(username="admin", password="eisoo.com")
            time.sleep(2)
            Domain_mgnt_home_page(driver).return_domain_home_page()  # 进入文档域管理
            raise e

        driver.get(f'https://{f_host}:8000')
        Login_page(driver).login(username="admin", password="eisoo.com")  # 返回本域
        time.sleep(2)
        Domain_mgnt_home_page(driver).return_domain_home_page()  # 进入文档域管理
        Domain_mgnt_page(driver).add_domain(domain_name=get_domain['replace_domain'], appid='1', appkey='1')  # 添加子域
        Domain_mgnt_home_page(driver).policy_sync()  # 进入策略同步
        time.sleep(1)
        doc_policy_page(driver).add_policy_with_auth(policy_name="上海爱数", enable="enable", option="账号密码 + 短信验证码")
        time.sleep(1)
        doc_policy_page(driver).apply_domain(domain_name=get_domain['replace_domain'])  # 策略绑定子域
        time.sleep(10)

        db = DB_connect(host=host)
        delete_vcode = "delete from sharemgnt_db.t_vcode"
        db.delete(delete_vcode)
        driver.get(f'https://{host}')
        ClientLoginPage(driver).login(username="a", pwd="eisoo.com")  # 登录客户端
        time.sleep(5)
        select_vcode = "select f_vcode from sharemgnt_db.t_vcode"
        code = db.select_one(select_vcode)
        print("验证码：", code)
        driver.find_element_by_xpath(ClientLoginPage(driver).el_code_input).send_keys(code[0])
        driver.find_element_by_xpath(ClientLoginPage(driver).el_check_button).click()
        time.sleep(2)
        driver.find_element_by_xpath(ClientLoginPage(driver).el_quick_start_cancel).click()

        # 清理数据
        driver.get(f'https://{f_host}:8000')
        Login_page(driver).login(username="admin", password="eisoo.com")  # 返回本域
        time.sleep(2)
        Domain_mgnt_home_page(driver).return_domain_home_page()  # 进入文档域管理
        Domain_mgnt_home_page(driver).policy_sync()  # 进入策略同步
        time.sleep(1)
        doc_policy_page(driver).edit_policy(policy_name="上海爱数", item="two_factor_auth", enable="enable",
                                            option="账号密码")
        time.sleep(1)
        doc_policy_page(driver).unbind_domain(domain_name=host)
        policy_data = CommonDocDomain().getPolicyIDNameByKeyword(httphost=f_host, key_word="上海爱数")
        policy_id = policy_data["data"][0]["id"]  # 获取策略ID
        domain_data = CommonDocDomain().getRelationDomainList(host=f_host, keyword=host)
        domain_id = domain_data["data"][0]["id"]  # 获取子域ID
        CommonDocDomain().deletepolicy(httphost=f_host, PolicyUUID=policy_id)  # 本域删除策略
        CommonDocDomain().delRelationDomain(host=f_host, uuid=domain_id)  # 本域删除子域

        select_policy = "select * from sharemgnt_db.t_user where f_login_name = 'a'"
        user_infor = db1.select_one(select_policy)
        user_id = user_infor[0]
        CommonDocDomain().close_person_doc(user_id=user_id, host=host)  # 关闭用户个人文档库
        CommonDocDomain().del_user(user_id=user_id, host=host)  # 删除用户
        third_close_sql = "UPDATE sharemgnt_db.t_third_party_auth SET f_enable = '0' WHERE f_app_name = '第三方集成测试'"
        db1.update(third_close_sql)  # 关闭第三方认证集成

        time.sleep(2)
        Domain_mgnt_home_page(driver).return_domain_home_page()  # 进入文档域管理


        #
        #     Domain_mgnt_home_page(driver).close_windows()
        #     raise





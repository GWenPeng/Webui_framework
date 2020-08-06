from AS7.Pages.Domain_mgnt.domain_mgnt_home_page import Domain_mgnt_home_page
from AS7.Pages.Domain_mgnt.domain_mgnt_page import Domain_mgnt_page
from AS7.Pages.Domain_mgnt.CommonDocDomain import CommonDocDomain
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from Common.parse_data import do_excel
from Common.screenshot import ScreenShot
import pytest
import allure
import time


class Test_check_domain:

    @allure.testcase("caseid:5354 文档域管理--添加子域--域名ip--气泡提示")
    @pytest.mark.high
    @pytest.mark.zyl
    def test_check_child_ip(self, driver):

        """
        添加子域--域名ip--气泡提示
        """
        # try:
        dp = Domain_mgnt_home_page(driver=driver)
        dp.return_domain_home_page()
        tip = do_excel(filename="add_domain.xlsx", sheetname="提示语",
                       minrow=1, maxrow=2, mincol=2, maxcol=2)
        domain_name_null = Domain_mgnt_page(driver=driver).check_domain_ip(domain_name="中文", title=tip[0],
                                                                           appid="appid",
                                                                           appkey="appkey",
                                                                           domain_type="child", direct_mode=False,
                                                                           port="443")
        assert domain_name_null == "此输入项不允许为空。"
        list_child_name = do_excel(filename="add_domain.xlsx", sheetname="域名校验",
                                   minrow=2, maxrow=6, mincol=2, maxcol=2)
        child_names = list(list_child_name)
        for name in child_names:
            error_message = Domain_mgnt_page(driver=driver).check_domain_ip(domain_name=name, title=tip[1],
                                                                            appid="appid",
                                                                            appkey="appkey",
                                                                            domain_type="child",
                                                                            direct_mode=False,
                                                                            port="443")
            assert error_message == "IP地址只能包含数字及.字符，格式形如 XXX.XXX.XXX.XXX，每段必须是 0~255 之间的整数。"
        # except Exception:
        #
        #     raise

    @allure.testcase("caseid:5362 文档域管理--添加平级域--域名气泡提示")
    @pytest.mark.high
    @pytest.mark.zyl
    def test_check_parallel_ip(self, driver):
        """
        添加子域--添加平级域--域名气泡提示
        """
        # try:
        dp = Domain_mgnt_home_page(driver=driver)
        dp.return_domain_home_page()
        tip = do_excel(filename="add_domain.xlsx", sheetname="提示语",
                       minrow=1, maxrow=3, mincol=2, maxcol=2)
        parallel_name = Domain_mgnt_page(driver=driver).check_domain_ip(domain_name=" ", title=tip[0],
                                                                        appid="appid",
                                                                        appkey="appkey",
                                                                        domain_type="parallel", direct_mode=False,
                                                                        port="443")
        assert parallel_name == "此输入项不允许为空。"
        list_parallel_name = do_excel(filename="add_domain.xlsx", sheetname="域名校验",
                                      minrow=8, maxrow=10, mincol=2, maxcol=2)
        parallel_names = list(list_parallel_name)
        for name in parallel_names:
            error_message = Domain_mgnt_page(driver=driver).check_domain_ip(domain_name=name, title=tip[2],
                                                                            appid="appid",
                                                                            appkey="appkey",
                                                                            domain_type="parallel",
                                                                            direct_mode=False,
                                                                            port="443")
            assert error_message == "域名只能包含 英文、数字 及 -. 字符，每一级不能以“-”字符开头或结尾，每一级长度必需 1~63 个字符，且总长不能超过253个字符。"
        # except Exception:
        #
        #     raise

    @pytest.fixture(scope="function")
    def set_child_domain(self, driver, get_domain, request):
        host = request.config.getoption(name="--host")
        host = host.split('//')[1].split(':')[0]
        # 使用father_domain添加当前环境为子域
        uuid = CommonDocDomain().addRelationDomain(httphost=get_domain["father_domain"], host=host)
        yield
        CommonDocDomain().delRelationDomain(host=get_domain["father_domain"], uuid=uuid)
        # 增加两步点击，刷新页面，清理数据
        driver.find_element_by_xpath("//a[span[text()='组织管理']]").click()
        Domain_mgnt_home_page(driver=driver).return_domain_home_page()

    @allure.testcase("caseid:5417 文档域管理--页面顶部提示--当前登录的域为子域检查顶部提示")
    @pytest.mark.ni
    @pytest.mark.high
    def test_check_chiledomain_title(self, driver, get_domain, set_child_domain):
        # try:
            dmp = Domain_mgnt_page(driver)
            driver.find_element_by_xpath("//a[span[text()='组织管理']]").click()
            words = "当前文档域已被 “{}” 添加为子域".format(str(get_domain["father_domain"]))
            xpath = "//div[text()='{}']".format(words)
            Domain_mgnt_home_page(driver=driver).return_domain_home_page()
            WebDriverWait(driver, 60).until(
                ec.visibility_of_element_located((By.XPATH, xpath)))
            words = driver.find_element_by_xpath(dmp.el_domain_infos).text
            assert '添加为子域' in words
        # except Exception:
        #
        #     Domain_mgnt_home_page(driver).close_windows()
        #     raise

    @allure.testcase("caseid:5417 文档域管理--页面顶部提示--当前登录的域为平级域检查顶部提示")
    @pytest.mark.ni
    @pytest.mark.high
    def test_check_paralleldomain_title(self, driver):
        # try:
            dmp = Domain_mgnt_page(driver)
            Domain_mgnt_home_page(driver=driver).return_domain_home_page()
            WebDriverWait(driver, 30).until(
                ec.visibility_of_element_located((By.XPATH, dmp.el_domain_infos)))
            words = driver.find_elements_by_xpath(dmp.el_domain_infos)
            assert len(words) == 1
        # except Exception:
        #
        #     Domain_mgnt_home_page(driver).close_windows()
        #     raise

    @pytest.fixture(scope="function")
    def set_father_domain(self, driver, get_domain, request):
        host = request.config.getoption(name="--host")
        host = host.split('//')[1].split(':')[0]
        # 添加replace_domain为子域，自身变为父域
        uuid = CommonDocDomain().addRelationDomain(host=get_domain["replace_domain"], httphost=host)
        yield
        CommonDocDomain().delRelationDomain(host=host, uuid=uuid)

    @allure.testcase("caseid:5417 文档域管理--页面顶部提示--当前登录的域为父域检查顶部提示")
    @pytest.mark.ni
    @pytest.mark.high
    def test_check_fatherdomain_title(self, driver, set_father_domain):
        # try:
            dmp = Domain_mgnt_page(driver)
            driver.find_element_by_xpath("//a[span[text()='组织管理']]").click()
            Domain_mgnt_home_page(driver=driver).return_domain_home_page()
            WebDriverWait(driver, 30).until(
                ec.visibility_of_element_located((By.XPATH, dmp.el_domain_infos)))
            words = driver.find_elements_by_xpath(dmp.el_domain_infos)
            assert len(words) == 1
        # except Exception:
        #
        #     Domain_mgnt_home_page(driver).close_windows()
        #     raise

    @pytest.fixture(scope="function")
    def set_deletechild_domain(self, driver, get_domain, request):
        host = request.config.getoption(name="--host")
        host = host.split('//')[1].split(':')[0]
        # father_domain添加当前环境为子域
        uuid = CommonDocDomain().addRelationDomain(host=host, httphost=get_domain["father_domain"])
        yield get_domain["father_domain"], uuid
        pass

    @allure.testcase("caseid:5417 文档域管理--页面顶部提示--已登录子域B，另一标签页删除该子域身份，刷新当前页面检查顶部提示")
    @pytest.mark.ni
    @pytest.mark.high
    def test_check_notchild_title(self, driver, set_deletechild_domain):
        # try:
            dmp = Domain_mgnt_page(driver)
            father_domain = set_deletechild_domain[0]
            uuid = set_deletechild_domain[1]
            driver.find_element_by_xpath("//a[span[text()='组织管理']]").click()
            Domain_mgnt_home_page(driver=driver).return_domain_home_page()
            # 去除当前环境子域身份
            CommonDocDomain().delRelationDomain(host=father_domain, uuid=uuid)
            driver.find_element_by_xpath("//a[span[text()='组织管理']]").click()
            Domain_mgnt_home_page(driver=driver).return_domain_home_page()
            WebDriverWait(driver, 30).until(
                ec.visibility_of_element_located((By.XPATH, dmp.el_domain_infos)))
            words = driver.find_elements_by_xpath(dmp.el_domain_infos)
            assert len(words) == 1
        # except Exception:
        #
        #     Domain_mgnt_home_page(driver).close_windows()
        #     raise

    @pytest.fixture(scope="function")
    def test_paralleltochild_domain(self, driver, get_domain, request):
        host = request.config.getoption(name="--host")
        host = host.split('//')[1].split(':')[0]
        yield host
        father_domain = get_domain["father_domain"]
        # 查询关系域列表
        childuuid = CommonDocDomain().getRelationDomainList(host=get_domain["replace_domain"])["data"][0]["id"]
        # 删除replace_domain和当前域父子域关系
        CommonDocDomain().delRelationDomain(host=get_domain["replace_domain"], uuid=childuuid)
        # 刷新页面，去除脏数据
        driver.find_element_by_xpath("//a[span[text()='组织管理']]").click()
        Domain_mgnt_home_page(driver=driver).return_domain_home_page()

    @allure.testcase("caseid:5417 文档域管理--页面顶部提示--已登录平级域A，另一标签页添加域A为子域，刷新当前页面检查顶部信息")
    @pytest.mark.ni
    @pytest.mark.high
    def test_paralleltochild_title(self, driver, get_domain, test_paralleltochild_domain):
        # try:
            dmp = Domain_mgnt_page(driver)
            host = test_paralleltochild_domain
            # replace_domain添加当前环境为子域
            CommonDocDomain().addRelationDomain(host=host, httphost=get_domain["replace_domain"])
            driver.find_element_by_xpath("//a[span[text()='组织管理']]").click()
            Domain_mgnt_home_page(driver=driver).return_domain_home_page()
            words = "当前文档域已被 “{}” 添加为子域".format(str(get_domain["replace_domain"]))
            xpath = "//div[text()='{}']".format(words)
            WebDriverWait(driver, 60).until(
                ec.visibility_of_element_located((By.XPATH, xpath)))
            words = driver.find_element_by_xpath(dmp.el_domain_infos).text
            assert '添加为子域' in words
        # except Exception:
        #
        #     Domain_mgnt_home_page(driver).close_windows()
        #     raise

    @allure.testcase("caseid:5355 文档域管理--添加子域--端口气泡提示")
    @pytest.mark.high
    @pytest.mark.zyl
    def test_CheckChild_Port(self, driver, get_domain):
        # try:
            dp = Domain_mgnt_home_page(driver=driver)
            dp.return_domain_home_page()
            domain_page = Domain_mgnt_page(driver=driver)
            domain_page.add_domain(domain_name="11.22.33", appid="appid", appkey="appkey",
                                   domain_type="child", direct_mode=True,
                                   is_submit=True, port="")
            driver.find_element_by_xpath(domain_page.el_domain_port_input).click()
            port_hint = driver.find_element_by_css_selector(domain_page.el_domain_port_hint)
            action = ActionChains(driver=driver)
            action.move_to_element(port_hint).perform()
            message = driver.find_element_by_xpath(domain_page.el_prot_null_hint).text
            driver.find_element_by_css_selector(domain_page.el_cancel).click()
            assert message == "此输入项不允许为空。"
            domain_page.add_domain(domain_name=get_domain["father_domain"], appid="appid", appkey="appkey",
                                   domain_type="child", direct_mode=True,
                                   is_submit=True, port="66666")
            driver.find_element_by_xpath(domain_page.el_domain_port_input).click()
            port_hint = driver.find_element_by_css_selector(domain_page.el_domain_port_hint)
            action = ActionChains(driver=driver)
            action.move_to_element(port_hint).perform()
            message = driver.find_element_by_xpath(domain_page.el_prot_range_hint).text
            driver.find_element_by_css_selector(domain_page.el_cancel).click()
            assert message == "端口号必须是 1~65535 之间的整数。"

            domain_page.add_domain(domain_name=get_domain["father_domain"], appid="appid", appkey="appkey",
                                   domain_type="child", direct_mode=True,
                                   is_submit=True, port="test")
            driver.find_element_by_xpath(domain_page.el_domain_port_input).click()
            port_hint = driver.find_element_by_css_selector(domain_page.el_domain_port_hint)
            action = ActionChains(driver=driver)
            action.move_to_element(port_hint).perform()
            message = driver.find_element_by_xpath(domain_page.el_prot_null_hint).text
            driver.find_element_by_css_selector(domain_page.el_cancel).click()
            assert message == "此输入项不允许为空。"

            domain_page.add_domain(domain_name="", appid="", appkey="",
                                   domain_type="child", direct_mode=True,
                                   is_submit=True, port="123456")

            message = driver.find_element_by_css_selector(domain_page.el_port_input).get_attribute("value")
            driver.find_element_by_css_selector(domain_page.el_cancel).click()
            assert message == "12345"
        # except Exception:
        #
        #     raise

    @allure.testcase("caseid:5357 文档域管理--添加子域--APP ID && Key气泡提示")
    @pytest.mark.high
    @pytest.mark.zyl
    def test_CheckChild_IdOrKey(self, driver, get_domain):
        # try:
            dp = Domain_mgnt_home_page(driver=driver)
            dp.return_domain_home_page()
            domain_page = Domain_mgnt_page(driver=driver)
            domain_page.add_domain(domain_name=get_domain["father_domain"], appid="", appkey="",
                                   domain_type="child", direct_mode=True,
                                   is_submit=True)
            driver.find_element_by_css_selector(domain_page.el_appid_input).click()
            appid_hint = driver.find_element_by_xpath(domain_page.el_domain_appid_hint)
            action = ActionChains(driver=driver)
            action.move_to_element(appid_hint).perform()
            appid_message = driver.find_element_by_xpath(domain_page.el_prot_null_hint).text

            driver.find_element_by_css_selector(domain_page.el_appkey_input).click()
            appkey_hint = driver.find_element_by_xpath(domain_page.el_domain_appkey_hint)
            action = ActionChains(driver=driver)
            action.move_to_element(appkey_hint).perform()
            appkey_message = driver.find_element_by_xpath(domain_page.el_prot_null_hint).text
            driver.find_element_by_css_selector(domain_page.el_cancel).click()
            assert appid_message == "此输入项不允许为空。"
            assert appkey_message == "此输入项不允许为空。"
        # except Exception:
        #
        #     raise

    @allure.testcase("caseid:5363 文档域管理--添加平级域--端口气泡提示")
    @pytest.mark.high
    @pytest.mark.zyl
    def test_CheckParallel_Port(self, driver, get_domain):
        # try:
            dp = Domain_mgnt_home_page(driver=driver)
            dp.return_domain_home_page()
            domain_page = Domain_mgnt_page(driver=driver)
            domain_page.add_domain(domain_name="11.22.33", appid="appid", appkey="appkey",
                                   domain_type="parallel", direct_mode=False,
                                   is_submit=True, port="")
            driver.find_element_by_xpath(domain_page.el_domain_port_input).click()
            port_hint = driver.find_element_by_css_selector(domain_page.el_parallel_port_hint)
            action = ActionChains(driver=driver)
            action.move_to_element(port_hint).perform()
            message = driver.find_element_by_xpath(domain_page.el_prot_null_hint).text
            driver.find_element_by_css_selector(domain_page.el_cancel).click()
            assert message == "此输入项不允许为空。"
            domain_page.add_domain(domain_name=get_domain["father_domain"], appid="appid", appkey="appkey",
                                   domain_type="parallel", direct_mode=False,
                                   is_submit=True, port="66666")
            driver.find_element_by_xpath(domain_page.el_domain_port_input).click()
            port_hint = driver.find_element_by_css_selector(domain_page.el_parallel_port_hint)
            action = ActionChains(driver=driver)
            action.move_to_element(port_hint).perform()
            message = driver.find_element_by_xpath(domain_page.el_prot_range_hint).text
            driver.find_element_by_css_selector(domain_page.el_cancel).click()
            assert message == "端口号必须是 1~65535 之间的整数。"

            domain_page.add_domain(domain_name=get_domain["father_domain"], appid="appid", appkey="appkey",
                                   domain_type="parallel", direct_mode=False,
                                   is_submit=True, port="test")
            driver.find_element_by_xpath(domain_page.el_domain_port_input).click()
            port_hint = driver.find_element_by_css_selector(domain_page.el_parallel_port_hint)
            action = ActionChains(driver=driver)
            action.move_to_element(port_hint).perform()
            message = driver.find_element_by_xpath(domain_page.el_prot_null_hint).text
            driver.find_element_by_css_selector(domain_page.el_cancel).click()
            assert message == "此输入项不允许为空。"

            domain_page.add_domain(domain_name="", appid="", appkey="",
                                   domain_type="parallel", direct_mode=False,
                                   is_submit=True, port="123456")

            message = driver.find_element_by_css_selector(domain_page.el_domain_port_parallel).get_attribute("value")
            driver.find_element_by_css_selector(domain_page.el_cancel).click()
            assert message == "12345"
        # except Exception:
        #
        #     raise

    @allure.testcase("5851 文档域管理--列表页面")
    @allure.testcase("5361 文档域管理--添加平级域--界面检查")
    @pytest.mark.normal
    @pytest.mark.gfr
    def test_check_parallel_domain(self,driver):
        # try:
            Domain_mgnt_home_page(driver).return_domain_home_page()
            domain_mgnt = Domain_mgnt_page(driver)
            WebDriverWait(driver, 20).until(ec.element_to_be_clickable((By.CSS_SELECTOR, domain_mgnt.el_add_domain)))
            assert driver.find_element_by_xpath(domain_mgnt.el_list_is_null).text == "列表为空"
            driver.find_element_by_css_selector(domain_mgnt.el_add_domain).click()
            WebDriverWait(driver,20).until(ec.visibility_of_element_located((By.XPATH,domain_mgnt.el_add_domain_title)))
            driver.find_element_by_css_selector(domain_mgnt.el_parallel_domain).click()
            driver.find_element_by_css_selector(domain_mgnt.el_domain_name_parallel).get_attribute("value") == ""
            driver.find_element_by_css_selector(domain_mgnt.el_domain_port_parallel).get_attribute("value") == 443
            direct_switch = driver.find_element_by_css_selector(domain_mgnt.el_direct_mode)
            # 开启直连模式
            direct_switch.click()
            appid = driver.find_element_by_css_selector(domain_mgnt.el_domain_appid_parallel)
            appkey = driver.find_element_by_css_selector(domain_mgnt.el_domain_appkey_parallel)
            assert appid.get_attribute("value") == ""
            assert appkey.get_attribute("value") == ""
            appid.send_keys('1')
            appkey.send_keys('1')
            # 关闭直连模式重新开启
            direct_switch.click()
            direct_switch.click()
            WebDriverWait(driver,20).until(ec.visibility_of_element_located((By.CSS_SELECTOR,domain_mgnt.el_domain_appid_parallel)))
            assert driver.find_element_by_css_selector(domain_mgnt.el_domain_appid_parallel).get_attribute("value") == "1"
            assert driver.find_element_by_css_selector(domain_mgnt.el_domain_appkey_parallel).get_attribute("value") == "1"
            driver.find_element_by_css_selector(domain_mgnt.el_cancel).click()  # 点击取消按钮
            WebDriverWait(driver,10).until(ec.invisibility_of_element_located((By.XPATH,domain_mgnt.el_add_domain_title)))
        # except Exception:
        #
        #     raise

    @allure.testcase("caseid:5672 文档域管理--添加平级域--域名为IP--气泡提示")
    @pytest.mark.high
    @pytest.mark.zyl
    def test_parallel_ip_title(self, driver):
        """
        添加子域--添加平级域--域名为IP--气泡提示
        """
        # try:
        dp = Domain_mgnt_home_page(driver=driver)
        dp.return_domain_home_page()
        tip = do_excel(filename="add_domain.xlsx", sheetname="提示语",
                       minrow=1, maxrow=3, mincol=2, maxcol=2)
        parallel_name = Domain_mgnt_page(driver=driver).check_domain_ip(domain_name="中文", title=tip[0],
                                                                        appid="appid",
                                                                        appkey="appkey",
                                                                        domain_type="parallel", direct_mode=False,
                                                                        port="443")
        assert parallel_name == "此输入项不允许为空。"
        list_child_name = do_excel(filename="add_domain.xlsx", sheetname="域名校验",
                                   minrow=2, maxrow=6, mincol=2, maxcol=2)
        parallel_names = list(list_child_name)
        for name in parallel_names:
            error_message = Domain_mgnt_page(driver=driver).check_domain_ip(domain_name=name, title=tip[1],
                                                                            appid="appid",
                                                                            appkey="appkey",
                                                                            domain_type="parallel",
                                                                            direct_mode=False,
                                                                            port="443")
            assert error_message == "IP地址只能包含数字及.字符，格式形如 XXX.XXX.XXX.XXX，每段必须是 0~255 之间的整数。"
        # except Exception:
        #
        #     raise

    @allure.testcase("caseid:5671 文档域管理--添加子域--域名不合法")
    @pytest.mark.high
    @pytest.mark.ni
    def test_addchild_domainnameerror(self,driver):
        # try:
            dmp = Domain_mgnt_page(driver)
            # 点击[添加文档域]
            WebDriverWait(driver, 60).until(
                ec.visibility_of_element_located((By.CSS_SELECTOR, dmp.el_add_domain)))
            driver.find_element_by_css_selector(dmp.el_add_domain).click()
            # 等待添加文档域弹窗显示
            WebDriverWait(driver, 60).until(
                ec.visibility_of_element_located((By.CSS_SELECTOR, dmp.el_windows)))
            # 等待APPID/APPKEY输入框可用
            WebDriverWait(driver, 60).until(
                ec.visibility_of_element_located((By.CSS_SELECTOR, dmp.el_appid_input)))
            WebDriverWait(driver, 60).until(
                ec.visibility_of_element_located((By.CSS_SELECTOR, dmp.el_appkey_input)))
            # 输入APPID和APPKEY
            driver.find_element_by_css_selector(dmp.el_appid_input).click()
            driver.find_element_by_css_selector(dmp.el_appid_input).send_keys("1")
            driver.find_element_by_css_selector(dmp.el_appkey_input).click()
            driver.find_element_by_css_selector(dmp.el_appkey_input).send_keys("1")
            # 等待域名输入框可用
            WebDriverWait(driver, 60).until(
                ec.visibility_of_element_located((By.CSS_SELECTOR, dmp.el_domain_name_input)))
            # 读取文件输入域名
            domainname = []
            errorinfo = []
            data = do_excel(filename="ni.xlsx",
                            sheetname="error_child_domainname", minrow=1, maxrow=6, mincol=1, maxcol=2)
            for tup in data:
                domainname.append(tup[0])
                errorinfo.append(tup[1])
            index = 0
            for name in domainname:
                driver.find_element_by_css_selector(dmp.el_domain_name_input_big).click()
                driver.find_element_by_css_selector(dmp.el_domain_name_input).send_keys(name)
                # 点击[确定]
                driver.find_element_by_xpath(dmp.el_edit_confirm).click()
                # 再次点击输入框获取使得错误信息显示
                driver.find_element_by_css_selector(dmp.el_domain_name_input_big).click()
                err = driver.find_element_by_xpath(dmp.el_domain_name_warn).text
                assert err == errorinfo[index]
                index = index + 1
            # 点击[取消]，关闭弹窗
            driver.find_element_by_xpath(dmp.el_edit_cancel).click()
        # except Exception:
        #
        #     Domain_mgnt_home_page(driver).close_windows()
        #     raise




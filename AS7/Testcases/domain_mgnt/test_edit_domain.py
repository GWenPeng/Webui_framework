from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from AS7.Pages.Domain_mgnt.domain_mgnt_home_page import Domain_mgnt_home_page
from AS7.Pages.Domain_mgnt.domain_mgnt_page import Domain_mgnt_page
from AS7.Pages.Domain_mgnt.CommonDocDomain import CommonDocDomain
from Common.screenshot import ScreenShot
from Common.parse_data import do_excel
from Common.NetworkDelay import NETWORKDELAY
import pytest
import allure
import time


class TestEditDomain:

    @allure.testcase("5962 文档域管理--域已被删除--点击[编辑]")
    @pytest.mark.high
    @pytest.mark.gfr
    def test_child_not_exist(self, driver, get_domain, request):
        info = do_excel(filename="domain_mgnt.xlsx", sheetname="提示信息", minrow=3, maxrow=3, mincol=2, maxcol=2)[0]
        host = get_domain["parallel_domain"]
        Domain_mgnt_home_page(driver).return_domain_home_page()
        domain_mgnt = Domain_mgnt_page(driver)
        domain_mgnt.add_domain(domain_name=host, appid="a", appkey="2")
        time.sleep(2)
        ip = request.config.getoption(name="--host")
        ip = ip.split(":8000")[0].split("https://")[1]
        res = CommonDocDomain().getRelationDomainList(host=ip)
        uuid = res['data'][0]["id"]
        CommonDocDomain().delRelationDomain(host=ip, uuid=uuid)
        time.sleep(3)
        driver.find_element_by_xpath(domain_mgnt.el_edit_domain).click()
        WebDriverWait(driver, 20).until(
            ec.presence_of_element_located((By.XPATH, domain_mgnt.el_edit_domain_not_exist)))
        text = driver.find_element_by_xpath(domain_mgnt.el_edit_domain_not_exist).text
        print(text)
        assert text == info[0]

    @allure.testcase("5425 文档域管理--编辑平级域--端口气泡提示")
    @pytest.mark.high
    @pytest.mark.gfr
    def test_port_tips(self, driver, get_domain):
        info = do_excel(filename="domain_mgnt.xlsx", sheetname="提示信息", minrow=4, maxrow=5, mincol=2, maxcol=2)
        parallel_host = get_domain["parallel_domain"]
        Domain_mgnt_home_page(driver).return_domain_home_page()
        domain_mgnt = Domain_mgnt_page(driver)
        domain_mgnt.add_domain(domain_name=parallel_host, domain_type="parallel", direct_mode=False)
        # 端口为空
        domain_mgnt.edit_domain(domain_name=parallel_host, port="", is_submit=True, direct_mode=False)
        driver.find_element_by_xpath(domain_mgnt.el_edit_port_tip).click()
        text = driver.find_element_by_xpath(domain_mgnt.el_edit_domain_port_null).text
        assert text == info[0][0]
        # 输入大于65535小于99999的整数
        data = do_excel(filename="domain_mgnt.xlsx", sheetname="编辑文档域", minrow=2, maxrow=5, mincol=1, maxcol=1)
        edit_port = driver.find_element_by_xpath(domain_mgnt.el_edit_port)
        if driver.desired_capabilities["browserName"] == "Safari":
            edit_port.send_keys(Keys.COMMAND, 'a')
            edit_port.send_keys(Keys.COMMAND, Keys.DELETE)
        else:
            edit_port.send_keys(Keys.CONTROL, 'a')
            edit_port.send_keys(Keys.DELETE)
        edit_port.send_keys(data[0][0])
        driver.find_element_by_xpath(domain_mgnt.el_edit_confirm).click()  # 点击【确定】
        driver.find_element_by_xpath(domain_mgnt.el_edit_port_tip).click()
        illegal_tip = driver.find_element_by_xpath(domain_mgnt.el_edit_domain_port_illegal).text
        assert illegal_tip == info[1][0]
        # 输入大于5位数字，第6位无法输入；输入中文英文等无法输入
        if driver.desired_capabilities["browserName"] == "Safari":
            edit_port.send_keys(Keys.COMMAND, 'a')
            edit_port.send_keys(Keys.COMMAND, Keys.DELETE)
        else:
            edit_port.send_keys(Keys.CONTROL, 'a')
            edit_port.send_keys(Keys.DELETE)
        for i in range(1, 4):
            edit_port.send_keys(data[i][0])
            value = edit_port.get_attribute("value")
            assert int(value) == 12345
        driver.find_element_by_xpath(domain_mgnt.el_edit_cancel).click()
        domain_mgnt.delete_domain()

    @pytest.fixture(scope="function")
    def add_direct_paralleldomain(self, driver, get_domain, request):
        host = request.config.getoption(name="--host")
        host = host.split('//')[1].split(':')[0]
        # 添加平级域
        uuid = CommonDocDomain().addRelationDomain(host=get_domain["parallel_domain"], domaintype="parallel",
                                                   httphost=host)
        yield host
        CommonDocDomain().delRelationDomain(host=host, uuid=uuid)
        # 刷新页面，消除脏数据
        driver.find_element_by_xpath("//a[span[text()='组织管理']]").click()
        Domain_mgnt_home_page(driver=driver).return_domain_home_page()

    @allure.testcase("Caseid:5426 文档域管理--编辑平级域--APP ID && Key气泡提示")
    @pytest.mark.ni
    @pytest.mark.high
    def test_edit_directparalleldomain(self, driver, add_direct_paralleldomain):
        # try:
            driver.find_element_by_xpath("//a[span[text()='组织管理']]").click()
            Domain_mgnt_home_page(driver=driver).return_domain_home_page()
            # 点击[编辑]按钮
            WebDriverWait(driver, 60).until(
                ec.visibility_of_element_located((By.XPATH, Domain_mgnt_page(driver).el_edit_domain)))
            driver.find_element_by_xpath(Domain_mgnt_page(driver).el_edit_domain).click()
            WebDriverWait(driver, 60).until(
                ec.visibility_of_element_located((By.XPATH, Domain_mgnt_page(driver).el_edit_h1)))
            host = add_direct_paralleldomain
            if host != '10.2.181.170':
                driver.find_element_by_xpath(Domain_mgnt_page(driver).el_edit_appid).send_keys(Keys.CONTROL, 'a')
                driver.find_element_by_xpath(Domain_mgnt_page(driver).el_edit_appid).send_keys(Keys.DELETE)
                driver.find_element_by_xpath(Domain_mgnt_page(driver).el_edit_appkey).send_keys(Keys.CONTROL, 'a')
                driver.find_element_by_xpath(Domain_mgnt_page(driver).el_edit_appkey).send_keys(Keys.DELETE)
            else:
                driver.find_element_by_xpath(Domain_mgnt_page(driver).el_edit_appid).send_keys(Keys.COMMAND, 'a')
                driver.find_element_by_xpath(Domain_mgnt_page(driver).el_edit_appid).send_keys(Keys.COMMAND,
                                                                                               Keys.DELETE)
                driver.find_element_by_xpath(Domain_mgnt_page(driver).el_edit_appkey).send_keys(Keys.COMMAND, 'a')
                driver.find_element_by_xpath(Domain_mgnt_page(driver).el_edit_appkey).send_keys(Keys.COMMAND,
                                                                                                Keys.DELETE)
            driver.find_element_by_xpath(Domain_mgnt_page(driver).el_edit_confirm).click()
            # 再次点击appid输入框，获取报错气泡
            driver.find_element_by_xpath(Domain_mgnt_page(driver).el_edit_appid).click()
            WebDriverWait(driver, 60).until(
                ec.visibility_of_element_located((By.XPATH, Domain_mgnt_page(driver).el_appid_message)))
            appid = driver.find_element_by_xpath(Domain_mgnt_page(driver).el_appid_message).text
            assert appid == "此输入项不允许为空。"
            # 再次点击appkey输入框，获取报错气泡
            driver.find_element_by_xpath(Domain_mgnt_page(driver).el_edit_appkey).click()
            WebDriverWait(driver, 60).until(
                ec.visibility_of_element_located((By.XPATH, Domain_mgnt_page(driver).el_appkey_message)))
            appkey = driver.find_element_by_xpath(Domain_mgnt_page(driver).el_appkey_message).text
            assert appkey == "此输入项不允许为空。"
            driver.find_element_by_xpath(Domain_mgnt_page(driver).el_edit_cancel).click()
        # except Exception:
        #
        #     Domain_mgnt_home_page(driver).close_windows()
        #     raise

    @pytest.fixture(scope="function")
    def add_direct_parallel_domain(self, driver, get_domain, request):
        host = request.config.getoption(name="--host")
        host = host.split('//')[1].split(':')[0]
        # 当前域添加parallel_domain为平级域
        uuid = CommonDocDomain().addRelationDomain(host=get_domain["parallel_domain"], domaintype="parallel",
                                                   httphost=host)
        yield host
        CommonDocDomain().delRelationDomain(host=host, uuid=uuid)
        WebDriverWait(driver, 60).until(
            ec.visibility_of_element_located((By.XPATH, "//a[span[text()='组织管理']]")))
        driver.find_element_by_xpath("//a[span[text()='组织管理']]").click()
        Domain_mgnt_home_page(driver=driver).return_domain_home_page()  # 定位到文档域管理

    @allure.testcase("Caseid:5427 文档域管理--编辑平级域失败--直连模式")
    @pytest.mark.ni
    @pytest.mark.high
    def test_edit_directparalleldomain_fail(self, driver, add_direct_parallel_domain):
        # try:
            WebDriverWait(driver, 60).until(
                ec.visibility_of_element_located((By.XPATH, "//a[span[text()='组织管理']]")))
            driver.find_element_by_xpath("//a[span[text()='组织管理']]").click()
            Domain_mgnt_home_page(driver=driver).return_domain_home_page()
            # 点击[编辑]按钮
            WebDriverWait(driver, 60).until(
                ec.visibility_of_element_located((By.XPATH, Domain_mgnt_page(driver).el_edit_domain)))
            driver.find_element_by_xpath(Domain_mgnt_page(driver).el_edit_domain).click()
            WebDriverWait(driver, 60).until(
                ec.visibility_of_element_located((By.XPATH, Domain_mgnt_page(driver).el_edit_h1)))  # 等待编辑文档域弹框出现
            host = add_direct_parallel_domain
            # 同时编辑端口/id/key
            if host != '10.2.181.170':
                driver.find_element_by_xpath(Domain_mgnt_page(driver).el_edit_port).send_keys(Keys.CONTROL, 'a')  # 编辑端口
                driver.find_element_by_xpath(Domain_mgnt_page(driver).el_edit_port).send_keys('443')
                driver.find_element_by_xpath(Domain_mgnt_page(driver).el_edit_appid).send_keys(Keys.CONTROL, 'a')  # 编辑id
                driver.find_element_by_xpath(Domain_mgnt_page(driver).el_edit_appid).send_keys('1')
                driver.find_element_by_xpath(Domain_mgnt_page(driver).el_edit_appkey).send_keys(Keys.CONTROL, 'a')  # 编辑key
                driver.find_element_by_xpath(Domain_mgnt_page(driver).el_edit_appkey).send_keys('1')
            else:
                driver.find_element_by_xpath(Domain_mgnt_page(driver).el_edit_port).send_keys(Keys.COMMAND, 'a')
                driver.find_element_by_xpath(Domain_mgnt_page(driver).el_edit_port).send_keys(Keys.COMMAND, Keys.DELETE)
                driver.find_element_by_xpath(Domain_mgnt_page(driver).el_edit_port).send_keys('443')
                driver.find_element_by_xpath(Domain_mgnt_page(driver).el_edit_appid).send_keys(Keys.COMMAND, 'a')
                driver.find_element_by_xpath(Domain_mgnt_page(driver).el_edit_appid).send_keys(Keys.COMMAND, Keys.DELETE)
                driver.find_element_by_xpath(Domain_mgnt_page(driver).el_edit_appid).send_keys('1')
                driver.find_element_by_xpath(Domain_mgnt_page(driver).el_edit_appkey).send_keys(Keys.COMMAND, 'a')
                driver.find_element_by_xpath(Domain_mgnt_page(driver).el_edit_appkey).send_keys(Keys.COMMAND, Keys.DELETE)
                driver.find_element_by_xpath(Domain_mgnt_page(driver).el_edit_appkey).send_keys('1')
            # 点击确定前，设置网络延迟
            network = NETWORKDELAY(host=host, delay_time=1000)
            network.delay()
            # 点击[确定]按钮
            driver.find_element_by_xpath(Domain_mgnt_page(driver).el_edit_confirm).click()
            # 再次点击输入框获取错误提示
            coninfos = driver.find_element_by_xpath(Domain_mgnt_page(driver).el_connection_tip).text
            assert coninfos == "正在连接，请稍候..."
            # 取消网络延迟
            network.delete_delay()
            # 再次点击[编辑]按钮
            WebDriverWait(driver, 240).until(
                ec.invisibility_of_element_located((By.XPATH, Domain_mgnt_page(driver).el_edit_h1)))
            driver.find_element_by_xpath(Domain_mgnt_page(driver).el_edit_domain).click()
            WebDriverWait(driver, 60).until(
                ec.visibility_of_element_located((By.XPATH, Domain_mgnt_page(driver).el_edit_h1)))  # 编辑文档域弹框title
            host = add_direct_parallel_domain
            # 编辑端口，使网络不可达
            if host != '10.2.181.170':
                driver.find_element_by_xpath(Domain_mgnt_page(driver).el_edit_port).send_keys(Keys.CONTROL, 'a')  # 编辑端口
                driver.find_element_by_xpath(Domain_mgnt_page(driver).el_edit_port).send_keys('111')
            else:
                driver.find_element_by_xpath(Domain_mgnt_page(driver).el_edit_port).send_keys(Keys.COMMAND, 'a')
                driver.find_element_by_xpath(Domain_mgnt_page(driver).el_edit_port).send_keys(Keys.COMMAND, Keys.DELETE)
                driver.find_element_by_xpath(Domain_mgnt_page(driver).el_edit_port).send_keys('111')
            driver.find_element_by_xpath(Domain_mgnt_page(driver).el_edit_confirm).click()
            WebDriverWait(driver, 60).until(
                ec.presence_of_element_located((By.XPATH, Domain_mgnt_page(driver).el_edit_connection_fail)))
            coninfos2 = driver.find_element_by_xpath(Domain_mgnt_page(driver).el_edit_connection_fail).text
            assert coninfos2 == "编辑失败，指定的文档域无法连接。"
            driver.find_element_by_xpath(Domain_mgnt_page(driver).el_edit_cancel).click()
        # except Exception:
        #
        #     Domain_mgnt_home_page(driver).close_windows()
        #     raise

    @allure.testcase("5421 文档域管理--编辑子域--点击[确定]")
    @pytest.mark.high
    @pytest.mark.zyl
    def test_Add_domain_tip(self, driver, get_domain):
        # try:
            Domain_mgnt_home_page(driver).return_domain_home_page()
            domain_mgnt = Domain_mgnt_page(driver)
            tip = do_excel(filename="add_domain.xlsx", sheetname="提示语",
                           minrow=4, maxrow=6, mincol=2, maxcol=2)
            host = get_domain["parallel_domain"]
            domain_mgnt.add_domain(domain_name=host, appid='1', appkey='1', is_submit=True)
            domain_mgnt.edit_domain(domain_name=host, port='445', is_submit=True, direct_mode=True)
            # connection_tip = driver.find_element_by_xpath(domain_mgnt.el_connection_tip).text
            WebDriverWait(driver, 30).until(
                ec.visibility_of_element_located((By.XPATH, domain_mgnt.el_edit_connection_fail)))
            connection_fail = driver.find_element_by_xpath(domain_mgnt.el_edit_connection_fail).text
            driver.find_element_by_css_selector(domain_mgnt.el_cancel).click()
            domain_mgnt.edit_domain(domain_name=host, is_submit=True, direct_mode=True)
            WebDriverWait(driver, 10).until(
                ec.invisibility_of_element_located((By.XPATH, domain_mgnt.el_add_domain_title)))
            info = domain_mgnt.get_domain_info()
            domain_mgnt.delete_domain()
            time.sleep(3)
            # assert tip[0][0] in connection_tip
            assert info == [host, "子域", "直连", "---"]
            assert connection_fail == tip[2][0]
        # except Exception:
        #
        #     raise

    @allure.testcase("5424 文档域管理--编辑平级域--页面检查")
    @pytest.mark.normal
    @pytest.mark.zyl
    def test_edit_parallel_page(self, driver, get_domain):
        # try:
            Domain_mgnt_home_page(driver).return_domain_home_page()
            domain_mgnt = Domain_mgnt_page(driver)
            host = get_domain["parallel_domain"]
            # 添加平级域非直连模式
            domain_mgnt.add_domain(domain_name=host, domain_type='parallel', direct_mode=False, is_submit=True)
            WebDriverWait(driver, 30).until(
                ec.visibility_of_element_located((By.XPATH, domain_mgnt.el_edit_domain)))
            driver.find_element_by_xpath(domain_mgnt.el_edit_domain).click()
            domain_type = driver.find_element_by_xpath(domain_mgnt.el_edit_type).text
            domain_name_status = driver.find_element_by_css_selector(domain_mgnt.el_domain_name_parallel).is_enabled()
            domain_name = driver.find_element_by_css_selector(domain_mgnt.el_domain_name_parallel).get_attribute(
                'value')
            edit_confirm_status = driver.find_element_by_xpath(domain_mgnt.el_edit_confirm).is_enabled()
            edit_cancel_status = driver.find_element_by_xpath(domain_mgnt.el_edit_cancel).is_enabled()
            driver.find_element_by_xpath(domain_mgnt.el_edit_cancel).click()
            domain_mgnt.delete_domain()
            assert domain_type == '平级域'
            assert domain_name == host
            assert domain_name_status is False
            assert edit_confirm_status is True
            assert edit_cancel_status is True
            # 添加平级域直连模式
            domain_mgnt.add_domain(domain_name=host, domain_type='parallel', direct_mode=True, appkey='1', appid='1',
                                   is_submit=True)
            WebDriverWait(driver, 30).until(
                ec.visibility_of_element_located((By.XPATH, domain_mgnt.el_edit_domain)))
            driver.find_element_by_xpath(domain_mgnt.el_edit_domain).click()
            edit_type = driver.find_element_by_xpath(domain_mgnt.el_edit_type).text
            domain_input_status = driver.find_element_by_css_selector(domain_mgnt.el_domain_name_parallel).is_enabled()
            domain_input_value = driver.find_element_by_css_selector(domain_mgnt.el_domain_name_parallel).get_attribute(
                'value')
            appid_status = driver.find_element_by_xpath(domain_mgnt.el_edit_appid).is_enabled()
            appkey_status = driver.find_element_by_xpath(domain_mgnt.el_edit_appkey).is_enabled()
            edit_buttion_confirm = driver.find_element_by_xpath(domain_mgnt.el_edit_confirm).is_enabled()
            edit_button_cancel = driver.find_element_by_xpath(domain_mgnt.el_edit_cancel).is_enabled()
            driver.find_element_by_xpath(domain_mgnt.el_edit_cancel).click()
            domain_mgnt.delete_domain()
            assert edit_type == '平级域'
            assert domain_input_value == host
            assert domain_input_status is False
            assert appid_status is True
            assert appkey_status is True
            assert edit_buttion_confirm is True
            assert edit_button_cancel is True
        # except Exception:
        #
        #     raise

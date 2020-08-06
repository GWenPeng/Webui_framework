# coding=utf-8
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from Common.screenshot import ScreenShot
from .domain_mgnt_home_page import Domain_mgnt_home_page
import allure
import time


class Domain_mgnt_page(object):
    """
    文档域管理页面
    """

    def __init__(self, driver):
        self.driver = driver
        # self.driver = webdriver.Chrome()
        self.el_add_domain = "div#docDomains>div>div>div>button"  # 添加文档域 css
        self.el_add_domain_title = "//h1[text()='添加文档域']"
        self.el_domain_infos = "//div[@id='docDomains']/div[1]/div[1]/div[1]" # 文档域管理页面顶部提示信息，用于判断当前域身份
        # <-------------------------------------------------------------------------->以下为文档域列表中的元素
        self.el_list_domain_name = '//tr/td[1]/div/div/div/span'  # 列表首行域名元素 xpath
        self.el_list_policy_name = '//tr/td[4]/div/div/div/span'  # 列表首行策略配置
        self.el_next_page_icon = '//div[text()="第 "]/following-sibling::button[1]'  # 下一页图标按钮
        self.el_page_input = '//div[text()="第 "]/input'  # 页码输入框
        self.el_page_count = '//div[text()=" 条，共 "]'  # 列表页显示总数
        self.el_list_is_null = "(//p[text()='列表为空'])[1]"  # 列表为空
        # <---------------------------------------------------------------------------------->以下是添加文档域弹窗 css
        self.el_windows = 'div[data-test-scope="ui/Dialog2"]>div:nth-child(2)'  # 弹窗元素 css
        self.el_windows_x = '//h1[text()="添加文档域"]/following-sibling::div[1]/div'  # 关闭弹窗'x'
        self.el_child_domain = "form>div:nth-child(1)>div>label"  # 子域 css
        self.el_parallel_domain = "form>div:nth-child(1)>div>div>label"  # 平级域
        self.el_child_domain_selectbox = "//span[text()='子域']/preceding-sibling::span[1]"  # 子域单选框
        self.el_parallel_domain_selectbox = "//span[text()='平级域']/preceding-sibling::span[1]"  # 平级域单选框
        self.el_domain_name_required = "//span[text()='域名：']/../../div[1]/div[1]/span[1]"  # 域名必填*
        self.el_port_required = "//span[text()='端口：']/following-sibling::div/span"  # 端口必填*
        self.el_appid_required = "//label[text()='APP ID:']/following-sibling::div/div[1]/span"  # appid必填*
        self.el_appkey_required = "//label[text()='APP Key:']/following-sibling::div/div[1]/span"  # appkey必填*

        self.el_input_parallel_domain = "form>div:nth-child(1)>div>div>label>span>input"  # 平级域图标按钮
        self.el_confirm = "#docDomains>div>div:nth-child(3)>div>div>div>div:nth-child(2)>div>div>div>button:nth-child(1)"  # 确定按钮
        self.el_cancel = "#docDomains>div>div:nth-child(3)>div>div>div>div:nth-child(2)>div>div>div>button:nth-child(2)"  # 取消按钮
        # <------------------------------------------------------------>添加子域
        self.el_domain_name_input = "form>div:nth-child(2)>div>div>div>input"  # 域名输入框
        self.el_domain_name_input_big = "form>div:nth-child(2)>div>div>div:nth-child(2)" # 放大域名输入框定位
        self.el_domain_name_hint = "//span[text()='域名：']/../../div/div/div[1]/div/div"  # 域名提示信息
        self.el_port_input = "form>div:nth-child(2)>div>div>div:nth-child(4)>div>input"  # 端口号输入框
        self.el_appid_input = "form>div:nth-child(3)>div>div>div>input"  # appid输入框
        self.el_appkey_input = "form>div:nth-child(4)>div>div>div>input"  # appkey输入框
        self.el_domain_name_warn = '//span[text()="域名："]/../following-sibling::div[1]/div/div/div/span/following-sibling::div[1]'  # 域名提示信息
        self.el_error_msg_add_fdomain = '//div[text()="该文档域已是父域，不允许添加为子域。"]'  # 文档域添加父域错误提示
        self.el_error_msg_repet = '//form/following-sibling::div[1][text()="该文档域已存在，不允许重复添加。"]'  # 通用的文档域提示信息
        self.el_domain_added_warn = "//div[contains(text(),'该文档域已被')]"  # 文档域被添加提示
        self.el_domain_added_warn_comm = "//form/following-sibling::div[1]"  # 文档域被添加提示
        self.el_domain_added_link_warn = '//form/following-sibling::div[1][text()="正在连接，请稍候..."]'  # 添加文档域正在连接提示
        self.el_domain_added_warn_edge = "//form/following-sibling::div[1]"  # 文档域被添加提示
        self.el_addself_aschild = "//div[text()='您不能添加当前域为子域。']"
        self.el_addself_asparallel = "//div[text()='您不能添加当前域为平级域。']"
        # <-------------------------------------------------------------->添加平级域
        self.el_direct_mode = "form>div:nth-child(2)>div>div"  # 直链模式开关
        self.el_domain_name_parallel = "form>div:nth-child(3)>div>div>div>input"  # 添加平级域域名
        self.el_domain_parallel_hint = "//span[text()='域名：']/../../div/div/div[1]/div/div"  # 域名提示信息
        self.el_domain_port_parallel = "form>div:nth-child(3)>div>div>div:nth-child(4)>div>input"  # 平级域端口号输入框
        self.el_domain_appid_parallel = "form>div:nth-child(4)>div>div>div>input"  # 平级域appid 输入框
        self.el_domain_appkey_parallel = "form>div:nth-child(5)>div>div>div>input"  # 平级域appkey输入框
        self.el_parallel_title = "//span[text()='域名：']"  # 平级域域名
        self.el_parallel_hint = "//span[text()='域名：']/../../div/div/div[1]"  # 平级域提示符
        self.el_domain_port_input = "//span[text()='端口：']/following-sibling::div/div"  # 端口号文本框 div
        self.el_domain_port_hint = "form>div:nth-child(2)>div>div>div:nth-child(4)>div>div:nth-child(2)>div"  # 端口号提示信息
        self.el_parallel_port_hint = "form>div:nth-child(3)>div>div>div:nth-child(4)>div>div:nth-child(2)>div"  # 端口提示信息
        self.el_domain_appid_hint = "//label[text()='APP ID:']/following-sibling::div/div/div/input/following-sibling::div/div"  # appid提示信息
        self.el_domain_appkey_hint = "//label[text()='APP Key:']/following-sibling::div/div/div/input/following-sibling::div/div"  # appkey提示信息
        self.el_prot_null_hint = "//span[text()='此输入项不允许为空。']"  # 端口号为空提示语
        self.el_prot_range_hint = "//span[text()='端口号必须是 1~65535 之间的整数。']"  # 端口号超出范围提示语
        self.el_direct_mode_explain = "//span[text()='说明']"
        self.el_direct_explain = "//span[text()='说明']/.."
        self.el_direct_mode_explainInfo1 = "//div[text()='直连模式：网络互通，源端可以直接将文件上传到目标端的对象存储（通过HTTPS协议）。']"  # 说明悬浮提示
        self.el_direct_mode_explainInfo2 = "//div[text()='非直连模式：网络不互通，无法通过协议进行数据交换，需借助交换设备实现文档同步。']"  # 说明悬浮提示

        # 添加子域网络连接失败提示
        self.el_connection_tip = "//div[text()='正在连接，请稍候...']"
        self.el_connection_fail = "//div[text()='添加失败，指定的文档域无法连接。']"
        # 编辑文档域
        self.el_edit_domain = "//td[1]/following-sibling::td[4]/div/div/div/button"  # 第一个域的编辑按钮
        self.el_edit_h1 = "//h1[text()='编辑文档域']"  # 编辑文档域弹框title
        self.el_edit_type = "//div[label[text()='域类型：']]/div/div/div/span"  # 编辑子域弹窗文档库类型
        self.el_edit_port = "//span[text()='端口：']/following-sibling::div/div/input"  # 端口输入框
        self.el_edit_appid = "//label[text()='APP ID:']/following-sibling::div/div/div/input"  # APP ID输入框
        self.el_edit_appkey = "//label[text()='APP Key:']/following-sibling::div/div/div/input"  # APP Key输入框
        self.el_edit_confirm = "//button[span[text()='确定']]"
        self.el_edit_cancel = "//button[span[text()='取消']]"
        # 编辑文档域提示
        self.el_edit_port_tip = "//span[text()='端口：']/following-sibling::div/div"  # 端口气泡提示
        self.el_edit_domain_not_exist = "//div[text()='该文档域已不存在。']"
        self.el_edit_domain_port_null = "//span[text()='此输入项不允许为空。']"
        self.el_edit_domain_port_illegal = "//span[text()='端口号必须是 1~65535 之间的整数。']"
        self.el_appid_message = "//label[text()='APP ID:']/../div[1]/div[1]/div[1]/div[1]/div[1]/div/div/span"  # APP ID输入框提示语
        self.el_appkey_message = "//label[text()='APP Key:']/../div[1]/div[1]/div[1]/div[1]/div/div/div/span"  # APP Key输入框提示语
        self.el_edit_connection_fail = "//div[text()='编辑失败，指定的文档域无法连接。']"
        # 删除文档域
        self.el_delete_button = "tbody>tr>td:nth-child(5)>div>div>div>div>button"
        self.el_delete_domain_title = "//div[text()='提示']"
        self.el_delete_domain_hint = "//div[text()='提示']/../following-sibling::div/div/div/div/div[2]/div"  # 删除文档域弹窗提示信息
        self.el_delete_confirm = "//button[span[text()='确定']]"
        self.el_delete_cancel = "//button[span[text()='取消']]"
        self.el_delete_tip = "//div[text()='无法删除，您选中的文档域已绑定策略同步，请先解除绑定，再执行此操作。']"
        self.el_delete_link_failed = '//div[text()="删除失败，指定的文档域无法连接。"]'

        # 解除绑定策略
        self.el_untie_policy = "//*[@id='docDomains']/div/div[2]/div/div[2]/table/tbody/tr/td[5]/div/div/div[3]/button"  # 解绑按钮
        self.el_untie_tip = "//div[text()='您确定要解除该文档域绑定吗？']"  # 解绑弹框提示语
        self.el_untie_filed = "//div[text()='解绑失败，指定的文档域无法连接。']"  # 解绑失败提示语

        # 搜索
        self.el_search_input = "//input[@placeholder='搜索']"
        self.el_search_delete = "(//div[input[@placeholder='搜索']]/following-sibling::div)/span"
        self.el_result_null = "//p[text()='抱歉，没有找到符合条件的结果']"

        # 文档域列表页码操作按钮
        self.el_first_page = "//*[@id='docDomains']/div/div[2]/div/div[3]/div/div[1]/button[1]"  # 首页按钮
        self.el_last_page = "//div/button[2]"  # 上一页按钮
        self.el_next_page = "//div/button[3]"  # 下一页按钮
        self.el_end_page = "//div/button[4]"  # 尾页按钮
        self.el_page_input = "//*[@id='docDomains']/div/div[2]/div/div[3]/div/div[1]/div/input"
        self.el_max_line_page = "//div[@id='docDomains']/div/div[2]/div/div[3]/div/div[2]"  # 每页显示的条数

    @allure.step("添加文档域")
    def add_domain(self, domain_name, appid=None, appkey=None, domain_type="child", direct_mode=False, is_submit=True,
                   **kwargs):
        WebDriverWait(self.driver, 20).until(ec.element_to_be_clickable((By.CSS_SELECTOR, self.el_add_domain)))
        self.driver.find_element_by_css_selector(self.el_add_domain).click()  # 点击添加子域按钮
        if domain_type == "parallel":
            self.driver.find_element_by_css_selector(self.el_parallel_domain).click()  # 点击平级域类型
            if direct_mode:
                self.driver.find_element_by_css_selector(self.el_direct_mode).click()  # 点击直链模式
                self.driver.find_element_by_css_selector(self.el_domain_name_parallel).send_keys(domain_name)  # 输入平级域域名
                for key in kwargs:
                    if key == "port":
                        el_port = self.driver.find_element_by_css_selector(self.el_domain_port_parallel)
                        # print(self.driver.desired_capabilities["browserName"] == "internet explorer")
                        if self.driver.desired_capabilities["browserName"] == "Safari":
                            el_port.send_keys(Keys.COMMAND, 'a')
                            el_port.send_keys(Keys.COMMAND, Keys.DELETE)
                        else:
                            el_port.send_keys(Keys.CONTROL, "a")
                            el_port.send_keys(Keys.DELETE)
                        el_port.send_keys(kwargs[key])  # 输入平级域端口号
                self.driver.find_element_by_css_selector(self.el_domain_appid_parallel).send_keys(appid)  # 输入appid
                self.driver.find_element_by_css_selector(self.el_domain_appkey_parallel).send_keys(appkey)  # 输入appkey
            else:
                self.driver.find_element_by_css_selector(self.el_domain_name_parallel).send_keys(domain_name)  # 输入平级域域名
                for key in kwargs:
                    if key == "port":
                        el_port = self.driver.find_element_by_css_selector(self.el_domain_port_parallel)
                        if self.driver.desired_capabilities["browserName"] == "Safari":
                            el_port.send_keys(Keys.COMMAND, 'a')
                            el_port.send_keys(Keys.COMMAND, Keys.DELETE)
                        else:
                            el_port.send_keys(Keys.CONTROL, "a")
                            el_port.send_keys(Keys.DELETE)
                        el_port.send_keys(kwargs[key])  # 输入平级域端口号
        elif domain_type == "child":
            self.driver.find_element_by_css_selector(self.el_child_domain).click()  # 点击添加类型:子域
            self.driver.find_element_by_css_selector(self.el_domain_name_input).send_keys(domain_name)  # 输入域名
            for key in kwargs:
                if key == "port":
                    el_port = self.driver.find_element_by_css_selector(self.el_port_input)
                    # if self.driver.desired_capabilities["browserName"] == "internet explorer":
                    #     el_port.send_keys(Keys.CONTROL, "a", Keys.DELETE)
                    # else:
                    #     el_port.clear()
                    if self.driver.desired_capabilities["browserName"] == "Safari":
                        el_port.send_keys(Keys.COMMAND, 'a')
                        el_port.send_keys(Keys.COMMAND, Keys.DELETE)
                    else:
                        el_port.send_keys(Keys.CONTROL, "a")
                        el_port.send_keys(Keys.DELETE)
                    el_port.send_keys(kwargs[key])  # 输入子域端口号
            self.driver.find_element_by_css_selector(self.el_appid_input).send_keys(appid)  # 输入appid
            self.driver.find_element_by_css_selector(self.el_appkey_input).send_keys(appkey)  # 输入appkey
        if is_submit:
            # time.sleep(5)
            self.driver.find_element_by_css_selector(self.el_confirm).click()  # 点击确定按钮
        else:
            self.driver.find_element_by_css_selector(self.el_cancel).click()  # 点击取消按钮

    @allure.step("获取文档域列表首行信息")
    def get_domain_info(self):
        domain_info = []
        for i in range(1, 5):
            text = self.driver.find_element_by_css_selector(
                "table>tbody>tr:nth-child(1)>td:nth-child("+str(i)+")>div>div>div>span").text
            domain_info.append(text)
        print(domain_info)
        return domain_info

    @allure.step("获取文档域列表表头信息")
    def get_title_info(self):
        domain_title_info = []
        j = 1
        for i in range(1, 6):
            text = self.driver.find_element_by_xpath("//thead/tr/th["+str(j)+"]/div/div").text
            domain_title_info.append(text)
            j = j + 1
        return domain_title_info

    @allure.step("获取文档域列表行数")
    def get_domain_list_count(self):
        time.sleep(2)
        tbody = self.driver.find_element_by_css_selector('tbody')
        elements = tbody.find_elements_by_tag_name("tr")
        return len(elements)

    @allure.step("编辑文档域")
    def edit_domain(self, domain_name, port=None, app_id=None, app_key=None, is_submit=True, domain_type="child",
                    direct_mode=True):
        # try:
            el_edit_domain = "//td[div[div[div[span[text()=\""+domain_name+"\"]]]]]/following-sibling::td[4]/div/div/div/button"
            WebDriverWait(self.driver, 20).until(ec.visibility_of_element_located((By.XPATH, self.el_edit_domain)))
            self.driver.find_element_by_xpath(el_edit_domain).click()
            WebDriverWait(self.driver, 20).until(ec.visibility_of_element_located((By.XPATH, self.el_edit_h1)))
            edit_port = self.driver.find_element_by_xpath(self.el_edit_port)
            edit_confirm = self.driver.find_element_by_xpath(self.el_edit_confirm)
            edit_cancel = self.driver.find_element_by_xpath(self.el_edit_cancel)
            if not direct_mode:
                if port is None:
                    pass
                else:
                    if self.driver.desired_capabilities["browserName"] == "Safari":
                        edit_port.send_keys(Keys.COMMAND, 'a')
                        edit_port.send_keys(Keys.COMMAND, Keys.DELETE)
                    else:
                        edit_port.send_keys(Keys.CONTROL, 'a')
                        edit_port.send_keys(Keys.DELETE)
                    edit_port.send_keys(port)
            elif direct_mode is True or domain_type == "child":
                edit_appid = self.driver.find_element_by_xpath(self.el_edit_appid)
                edit_appkey = self.driver.find_element_by_xpath(self.el_edit_appkey)
                if port is None and app_id is None and app_key is None:
                    pass
                elif app_id is None and app_key is None and port is not None:
                    # edit_port.send_keys(Keys.CONTROL, 'a', Keys.DELETE)
                    # edit_port.send_keys(port)
                    if self.driver.desired_capabilities["browserName"] == "Safari":
                        edit_port.send_keys(Keys.COMMAND, 'a')
                        edit_port.send_keys(Keys.COMMAND, Keys.DELETE)
                    else:
                        edit_port.send_keys(Keys.CONTROL, 'a')
                        edit_port.send_keys(Keys.DELETE)
                    edit_port.send_keys(port)
                elif port is None and app_id is not None and app_key is not None:
                    edit_appid.send_keys(Keys.CONTROL, 'a', Keys.DELETE)
                    edit_appkey.send_keys(Keys.CONTROL, 'a', Keys.DELETE)
                    edit_appid.send_keys(app_id)
                    edit_appkey.send_keys(app_key)
                else:
                    edit_port.send_keys(Keys.CONTROL, 'a', Keys.DELETE)
                    edit_appid.send_keys(Keys.CONTROL, 'a', Keys.DELETE)
                    edit_appkey.send_keys(Keys.CONTROL, 'a', Keys.DELETE)
                    edit_port.send_keys(port)
                    edit_appid.send_keys(app_id)
                    edit_appkey.send_keys(app_key)
            if is_submit:
                edit_confirm.click()
                time.sleep(3)
            else:
                edit_cancel.click()
                time.sleep(3)
        # except Exception:
        #
        #     Domain_mgnt_home_page(self.driver).close_windows()
        #     raise

    @allure.step("清除文本框内容")
    def clear_input(self, element):
        if self.driver.desired_capabilities["browserName"] == "Safari":
            element.send_keys(Keys.COMMAND, 'a')
            element.send_keys(Keys.COMMAND, Keys.DELETE)
        else:
            element.send_keys(Keys.CONTROL, 'a')
            element.send_keys(Keys.DELETE)

    @allure.step("删除第几行文档域,index默认第一行")
    def delete_domain(self, index=1, is_submit=True):
        # try:
        # self.driver.find_element_by_css_selector(self.el_delete_button).click()
        # time.sleep(3)
        # WebDriverWait(self.driver, 20).until(ec.visibility_of_element_located((By.XPATH, "//tr[%s]/td["
        #                                                                                  "5]/div/div/div/div/button" %
        #                                                                        index)))
            self.driver.find_element_by_xpath("//tr[%s]/td[5]/div/div/div/div/button" % index).click()
            WebDriverWait(self.driver, 20).until(ec.visibility_of_element_located((By.XPATH, self.el_delete_domain_title)))
            if is_submit:
                self.driver.find_element_by_xpath(self.el_delete_confirm).click()
            else:
                self.driver.find_element_by_xpath(self.el_delete_cancel).click()
            time.sleep(3)
        # except Exception:
        #
        #     Domain_mgnt_home_page(self.driver).close_windows()
        #     raise

    @allure.step("获取列表中第几行第几列文本")
    def get_domain_name_by_index(self, row=1, col=1):
        domain_name = self.driver.find_element_by_xpath("//tr[%s]/td[%s]/div/div/div/span" % (row, col)).text
        return domain_name

    @allure.step("根据域名删除关系域")
    def delete_domain_by_name(self, domain_name, is_submit=True):
        self.driver.find_element_by_xpath(
            "(//td[div[div[div[span[text()=\""+domain_name+"\"]]]]]/following-sibling::td[4])/div/div/div[2]/div/button").click()
        WebDriverWait(self.driver, 20).until(ec.visibility_of_element_located((By.XPATH, self.el_delete_domain_title)))
        if is_submit:
            self.driver.find_element_by_xpath(self.el_delete_confirm).click()
        else:
            self.driver.find_element_by_xpath(self.el_delete_cancel).click()
        WebDriverWait(self.driver, 20).until(
            ec.invisibility_of_element_located((By.XPATH, self.el_delete_domain_title)))

    @allure.step("添加文档域ip校验")
    def check_domain_ip(self, domain_name, title, appid, appkey, domain_type="child", direct_mode=False, **kwargs):
        WebDriverWait(self.driver, 20).until(ec.visibility_of_element_located((By.CSS_SELECTOR, self.el_add_domain)))
        self.driver.find_element_by_css_selector(self.el_add_domain).click()  # 点击添加子域按钮
        action = ActionChains(driver=self.driver)
        if domain_type == "child":
            '''
            域名ip校验
            '''
            WebDriverWait(self.driver, 20).until(
                ec.visibility_of_element_located((By.CSS_SELECTOR, self.el_domain_name_input)))
            child_name = self.driver.find_element_by_css_selector(self.el_domain_name_input)  # 域名输入框
            child_name.click()  # 点击域名输入框
            # domain_name.send_keys(Keys.CONTROL, 'a', Keys.DELETE)  # 清空输入框内容
            child_name.send_keys(domain_name)  # 输入域名
            el_confirm = self.driver.find_element_by_css_selector(self.el_confirm)  # 添加文档域【确定】按钮
            el_confirm.click()
            space_tip = list(title)[0]
            domain_name_text = "//span[text()=\""+space_tip+"\"]"
            child_name.click()
            child_hint = self.driver.find_element_by_xpath(self.el_domain_name_hint)
            action.move_to_element(child_hint).perform()
            domain_name_title = self.driver.find_element_by_xpath(domain_name_text).text  # 获取提示内容
            self.driver.find_element_by_css_selector(self.el_cancel).click()  # 点击【取消】
            return domain_name_title
        elif domain_type == "parallel":
            WebDriverWait(self.driver, 20).until(
                ec.visibility_of_element_located((By.CSS_SELECTOR, self.el_parallel_domain)))
            self.driver.find_element_by_css_selector(self.el_parallel_domain).click()
            parallel_name = self.driver.find_element_by_css_selector(self.el_domain_name_parallel)  # 域名输入框
            parallel_name.click()  # 点击域名输入框
            # domain_name.send_keys(Keys.CONTROL, 'a', Keys.DELETE)  # 清空输入框内容
            parallel_name.send_keys(domain_name)  # 输入域名
            # time.sleep(1)
            el_confirm = self.driver.find_element_by_css_selector(self.el_confirm)  # 添加文档域【确定】按钮
            el_confirm.click()
            space_tip = list(title)[0]
            domain_name_text = "//span[text()=\""+space_tip+"\"]"
            # time.sleep(1)
            self.driver.find_element_by_xpath(self.el_parallel_hint).click()
            parallel_hint = self.driver.find_element_by_xpath(self.el_domain_parallel_hint)
            action.move_to_element(parallel_hint).perform()
            parallel_name_title = self.driver.find_element_by_xpath(domain_name_text).text  # 获取提示信息
            self.driver.find_element_by_xpath(self.el_parallel_title).click()
            self.driver.find_element_by_css_selector(self.el_cancel).click()
            return parallel_name_title

    @allure.step("判断元素是否存在")
    def isElement(self, element):
        flag = True
        browser = self.driver
        try:
            browser.find_element_by_css_selector(element)
            return flag

        except:
            flag = False
            return flag

    @allure.step("根据行数，解绑文档域策略")
    def remove_binding_by_index(self, row=1):
        self.driver.find_element_by_xpath("//tr[%s]/td[5]/div/div/div[3]/button" % row).click()
        self.driver.find_element_by_xpath("//span[text()='确定']").click()

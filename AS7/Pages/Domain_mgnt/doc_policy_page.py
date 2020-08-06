# coding=utf-8
from selenium.webdriver.common.keys import Keys
from AS7.Pages.Domain_mgnt.domain_mgnt_home_page import Domain_mgnt_home_page
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.select import Select
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from AS7.Pages.Domain_mgnt.domain_mgnt_page import Domain_mgnt_page
from Common.screenshot import ScreenShot
from selenium.common.exceptions import NoSuchAttributeException
import time
import allure


class doc_policy_page(object):
    """
    文档域策略同步界面
    """

    def __init__(self, driver):
        # self.driver = webdriver.Chrome()
        self.driver = driver
        self.el_add_policy = "//span[text()='添加策略配置']"  # 新增策略按钮
        self.el_add_policy_bt = '//span[text()="添加策略配置"]/..'  # 新增策略的button元素
        self.el_add_policy_enable = "//span[text()='添加策略配置']/.."  # 新增按钮是否可用
        self.el_popups_sidebar = "//span[text()='登录策略']/.." # 新增策略弹窗侧边栏‘登录策略’元素
        self.el_policy_name = "//label[text()='策略配置名称：']/../div/input"  # 策略名称输入框
        self.el_policy_body = "//div[@data-test-scope='ui/Dialog2']/div[2]/div[2]/div/div/div[3]/div/div[2]/div/div[2]/div[1]" # 添加策略body部分
        self.el_password_status = "//div[text()='密码强度']/following-sibling::div[1]/span[1]"  # 密码强度状态
        self.el_restricted_client_status = "//div[text()='限制客户端登录']/following-sibling::div[1]/span[1]"  # 限制客户端登录状态
        self.el_two_factor_authentication_status = "//div[text()='双因子认证']/following-sibling::div[1]/span[1]"  # 双因子认证状态
        self.el_confirm_button = "//h1[text()='添加策略配置']/../../div[2]/div[1]/div[2]/div[1]/button[1]"  # 添加策略配置确定按钮
        self.el_cancel_button = "//h1[text()='添加策略配置']/../../div[2]/div[1]/div[2]/div[1]/button[2]"  # 添加策略配置取消按钮
        self.el_policy_name_empty_hint = "//span[text()='此输入项不允许为空。']"
        self.el_policy_name_illegal_hint = "//span[text()='只允许包含英文特殊字符：~!%#$@-_. ，长度范围 1~100 个字符。']"
        self.el_policy_name_exist_button = "//div[text()='提示']/../following-sibling::div/div/div[2]/div/button"  # 策略配置名称重复提示弹窗确定按钮
        self.el_add_policy_search = "(//input[@placeholder='搜索'])[2]"  # [添加策略配置]策略搜索框
        self.el_add_policy_search_empty = "//label[text()='策略配置名称：']/../../div[2]/div/div[3]/span"  # [添加策略配置]策略搜索框内清空按钮
        self.el_policy_search = "//span[text()='添加策略配置']/../../div[1]/div[2]/input"  # 策略配置搜索框
        self.el_policy_search_empty = "//span[text()='添加策略配置']/../../div[1]/div[3]/span"  # 策略配置搜索框清空按钮
        self.el_edit_confirm_button = "//h1[text()='编辑策略配置']/../../div[2]/div[1]/div[2]/div[1]/button[1]"  # 编辑策略配置确定按钮
        self.el_edit_cancel_button = "//h1[text()='编辑策略配置']/../../div[2]/div[1]/div[2]/div[1]/button[2]"  # 编辑策略配置取消按钮
        # <------------------------------------------------------>密码强度定位
        self.el_pwd_strength = "//div[text()='密码强度']"  # 配置密码强度
        self.el_enable_pwd_strength = "//div[text()='密码强度']/../following-sibling::div/div/div/div/label"  # 是否启用
        self.pwd_drop_down = "//div[text()='密码强度：']/span/span[2]"  # 是否修改密码强度，下拉按钮
        self.strong_pwd = "//span[text()='强密码']"  # 配置密码强度，下拉框中选择强密码
        self.weaf_pwd = "//span[text()='弱密码']"  # 配置密码强度，下拉框中选择弱密码
        self.strong_pwd_length = "//label[text()='强密码格式：密码长度至少为 ']"
        self.strong_pwd_length_input = "//div[label[text()='强密码格式：密码长度至少为 ']]/div/div/div/input"  # 设置密码长度输入框
        self.el_security_pwd_strength = "//select[@id='pwd_strength']"  # 密码强度下拉框
        # <------------------------------------------------------>确定/取消按钮定位
        self.is_submit = "//span[text()='确定']"  # 添加策略配置'确定'按钮
        self.is_hintpoop_cancel = "//span[text()='取消']"  # '取消'按钮
        # <------------------------------------------------------>新增策略列表显示
        self.el_policy_first = "//tbody/tr[1]/td[1]/div/div/div/span"  # 新增策略列表首行策略名称
        self.el_policy_first_selected = "//tbody/tr[1]/td[1]/div/div/div/span/.."  # 判断策略列表首行是否选中
        self.el_policy_list_name = 'tbody>tr>td:nth-child(1)>div>div>div>span'  # 策略列表中,策略名称
        self.el_edit_policy = "(//tbody)[1]/tr/td[2]/div/div/div[1]/div/button/span"  # 编辑策略按钮
        self.el_edit_policy_bt = 'tbody>tr>td:nth-child(2)>div>div>div>div>button'  # 编辑策略bt
        self.el_edit_policy_enable = "(//tbody)[1]/tr/td[2]/div/div/div[1]/div/button/span/.."  # 编辑按钮是否可用
        self.el_delete_policy = "(//tbody)[1]/tr/td[2]/div/div/div[2]/button/span"  # 删除策略按钮
        self.el_delete_policy_enable = "(//tbody)[1]/tr/td[2]/div/div/div[2]/button/span/.."  # 删除按钮是否可用
        self.el_delete_policy_pop = "//div[text()='您确定要删除此策略配置吗？']"  # 删除策略弹窗
        self.el_del_confirm_bt = '//button/span[text()="确定"]/..'  # 弹窗确认按钮
        # 编辑策略提示
        self.el_edit_policy_not_exist = "//span[text()='该策略配置已不存在。']"
        # 页码元素
        self.el_up_page_icon = '(//div[text()="第 "])[1]/preceding-sibling::button[1]'  # 上一页
        self.el_first_page_icon = '(//div[text()="第 "])[1]/preceding-sibling::button[2]'  # 第一页
        self.el_next_page_icon = '(//div[text()="第 "]/following-sibling::button)[1]'  # 下一页图标按钮
        self.el_last_page_icon = '(//div[text()="第 "]/following-sibling::button)[2]'  # 最后一页
        self.el_page_input = '(//div[contains(text(),"第")]/input)[1]'  # 页码输入框
        self.el_page_count = "(//div[contains(text(),'显示')])[1]"  # 列表页显示总数
        self.el_binded_domain_page_input = "(//div[contains(text(),'第')]/input)[2]"  # 绑定子域表单页码输入框
        self.el_page_count_apply = "(//div[contains(text(),'显示')])[2]"  # 策略绑定文档域列表页显示总数
        # 列表提示
        self.el_list_is_null = "(//p[text()='列表为空'])[1]"  # 策略绑定文档域列表，列表为空
        self.el_list_null = "(//p[text()='列表为空'])[2]"
        self.el_list_no_search_results = "(//p[text()='抱歉，没有找到符合条件的结果'])"

        # <------------------------------------------------------>策略绑定文档域列表
        self.el_add_domain = "//span[text()='添加文档域']"  # 绑定文档域按钮
        self.el_add_domain_enable = "//span[text()='添加文档域']/.."  # 绑定文档域按钮是否可用
        self.el_apply_domain_first = "(//tbody)[2]/tr[1]/td[1]/div/div/div"  # 策略绑定文档域首行文档域名称
        self.el_unbind_domain = "(//tbody)[2]/tr/td[2]/div/div/button/span"  # 解绑文档域按钮
        self.el_unbind_domain_enable = "(//tbody)[2]/tr/td[2]/div/div/button/span/.."  # 解绑文档域按钮是否可用
        self.el_applylist_search = "//button[span[text()='添加文档域']]/following-sibling::div/div[2]/input"  # 绑定文档域列表搜索框
        self.el_applylist_search_empty = "//*[@id='policySync']/div/div/div[3]/div/div[2]/div/div[3]/div/div/div/p"  # 搜索结果为空列表时列表提示
        self.el_applylist_search_x = "//button[span[text()='添加文档域']]/following-sibling::div/div[3]"  # 搜索框的清空【x】按钮
        self.el_apply_list = "(//tbody)[2]"  # 策略绑定文档域列表
        self.el_domain_next_page_icon = "(//div[text()='第 '])[2]/following-sibling::button[1]/span"  # 已绑定文档域下一页按钮
        self.el_unbind_domain_enable = "(//tbody)[2]/tr/td[2]/div/div/button/span/.."  # 解绑文档域按钮是否可用
        self.el_unbind_domain_tip = "//div[text()='您确定要解除该文档域绑定吗？']"  # 解绑文档域提示
        self.el_unbind_domain_confirm = "//button[span[text()='确定']]"
        self.el_unbind_domain_cancel = "//button[span[text()='取消']]"
        # <------------------------------------------------------>策略添加文档域弹窗
        self.el_add_domain_title = "//h1[text()='添加文档域']"  # 添加文档域弹窗标题
        self.el_child_domain_location = "//a/span[@title]/span[2]"
        self.el_first_binded_domain = "ul>li:nth-child(1)>div>div>div>span"  # 添加文档域弹窗第一个被绑定的文档域
        self.el_clear_button = "//button[span[text()='清空']]"  # 清空
        self.el_submit_button = "//button[span[text()='确定']]"  # 确定
        self.el_cancel = "//div[h1[text()='添加文档域']]/following-sibling::div/div/div[2]/div/button[2]"  # 取消按钮
        self.el_x = "//div[div[div[label[text()='已选：']]]]/following-sibling::div/ul/li/div[2]"  # 已选列表首行信息后的【x】按钮
        self.el_applypop_search = "//div[h1[text()='添加文档域']]/following-sibling::div/div/div/div/div/div/div/div/div[2]/input"  # 搜索输入框
        self.el_applypop_search_empty = "//div[h1[text()='添加文档域']]/following-sibling::div/div/div/div/div/div/div[2]/div/div/div"  # 搜索结果为空列表时列表提示
        self.el_applypop_search_x = "//div[h1[text()='添加文档域']]/following-sibling::div/div/div/div/div/div/div/div/div[3]"  # 搜索框的清空【x】按钮
        self.el_applydomain_hinticon = "// div[text() = '提示']"
        self.el_applydomain_hinttext = "/html/body/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/div[2]/div"  # 提示信息
        self.el_hintpop_confirm = "/html/body/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/button"  # 提示弹窗【确定】按钮

        # <------------------------------------------------------>限制客户端登录定位
        self.el_restricted_client_login = "//div[div[text()='限制客户端登录']]"  # 展开限制客户端登录策略项
        self.el_enable_restricted_client_login = "//div[text()='限制客户端登录']/../following-sibling::div/div/div/div/label"  # 启用限制客户端登录策略项
        self.el_web_client_option = "//span[text()='禁止Web客户端登录']"  # 禁止Web客户端登录选项
        self.el_android_client_option = "//span[text()='禁止Android客户端登录']"
        self.el_ios_client_option = "//span[text()='禁止iOS客户端登录']"
        self.el_mobile_web_option = "//span[text()='禁止移动Web客户端登录']"

        # 双因子认证
        self.el_two_factor_auth = "//div[text()='双因子认证']"
        self.el_enable_two_factor_auth = "(//span[input[@name='multi_factor_auth']])[2]"  # 已启用单选按钮
        self.el_disable_two_factor_auth = "(//span[input[@name='multi_factor_auth']])[1]"  # 未启用单选按钮
        self.el_selcet_icon = "//span[text()='登录认证： 设置用户必须通过 ']/following-sibling::span[1]"  # 登录选项下拉按钮
        self.el_control_wrong_password = "//span[text()='用户登录时，连续输错密码 ']/following-sibling::div/div/div/input"  # 账号密码+图形验证码输错密码次数输入框
        self.el_SMS_code_tip = "//div[text()='（短信验证码需要配置对应的服务器插件才能获取，如果您还没有配置，可以在 第三方认证集成 页面进行操作）']"
        self.el_dynamic_tip = "//div[text()='（动态密码需要配置对应的应用插件才能获取，如果您还没有配置，可以在 第三方认证集成 页面进行操作）']"

        # 安全管理页面
        self.el_security_tab = "//li[a[span[text()='安全管理']]]"
        self.el_login_auth = "//span[text()='设置用户必须通过']/following-sibling::span[1]/span/div/div/span"  # 登录认证方式
        self.el_login_select = "//span[text()='设置用户必须通过']/following-sibling::span[1]/span"  # 登录认证下拉框

        # 第三方认证集成页面
        self.el_third_party_auth = "//span[text()='第三方认证集成']"
        self.el_third_party_auth_button = "//label[text()='状态：']/../div[1]/div[2]/button"  # 状态开关
        self.el_third_party_auth_save = "//span[text()='保存']"  # 保存按钮

    @allure.step("新增策略")
    def add_policy(self, policy_name, item=None, enable=False, strength='weak', options=None, is_submit=True, **kwargs):
        WebDriverWait(self.driver, 30).until(
            ec.visibility_of_element_located((By.XPATH, self.el_add_policy)))
        self.driver.find_element_by_xpath(self.el_add_policy).click()
        WebDriverWait(self.driver, 30).until(
            ec.visibility_of_element_located((By.XPATH, self.el_policy_name)))
        self.driver.find_element_by_xpath(self.el_policy_name).send_keys(policy_name)
        # 判断配置项
        if item == "pwd_strength":
            self.pwd_strength(enable, strength, **kwargs)
        elif item == "restrict_client_login":
            self.restricted_client_login(enable, options, **kwargs)
        if is_submit:
            self.driver.find_element_by_xpath(self.el_confirm_button).click()
        else:
            self.driver.find_element_by_xpath(self.el_cancel_button).click()

    @allure.step("新增策略--选择双因子认证")
    def add_policy_with_auth(self, policy_name, enable, option, pwd_count=None, is_submit=True):
        WebDriverWait(self.driver, 60).until(ec.visibility_of_element_located((By.XPATH, self.el_add_policy)))
        self.driver.find_element_by_xpath(self.el_add_policy).click()
        WebDriverWait(self.driver, 60).until(ec.visibility_of_element_located((By.XPATH, self.el_policy_name)))
        self.driver.find_element_by_xpath(self.el_policy_name).send_keys(policy_name)
        self.two_factor_auth(enable, option, pwd_count)
        if is_submit:
            self.driver.find_element_by_xpath(self.el_confirm_button).click()
        else:
            self.driver.find_element_by_xpath(self.el_cancel_button).click()

    @allure.step("配置密码强度")
    def pwd_strength(self, enable, strength, **kwargs):
        WebDriverWait(self.driver, 60).until(
            ec.visibility_of_element_located((By.XPATH, self.el_pwd_strength)))  # 密码强度配置项是否显示
        if enable == False:
            pass  # 不启用密码强度--直接点击确定
        elif strength == 'weak':
            self.driver.find_element_by_xpath(self.el_pwd_strength).click()
            WebDriverWait(self.driver, 60).until(
                ec.visibility_of_element_located((By.XPATH, self.el_enable_pwd_strength)))
            self.driver.find_element_by_xpath(self.el_enable_pwd_strength).click()
            self.driver.find_element_by_xpath(self.pwd_drop_down).click()  # 密码强度文本框下拉按钮
            self.driver.find_element_by_xpath(self.weaf_pwd).click()  # 选择弱密码
        else:
            self.driver.find_element_by_xpath(self.el_pwd_strength).click()
            WebDriverWait(self.driver, 60).until(
                ec.visibility_of_element_located((By.XPATH, self.el_enable_pwd_strength)))
            self.driver.find_element_by_xpath(self.el_enable_pwd_strength).click()
            self.driver.find_element_by_xpath(self.pwd_drop_down).click()  # 密码强度文本框下拉按钮
            self.driver.find_element_by_xpath(self.strong_pwd).click()  # 选择强密码
            for key in kwargs:
                if key == "length":
                    WebDriverWait(self.driver, 60).until(
                        ec.visibility_of_element_located((By.XPATH, self.strong_pwd_length)))
                    pwd_length_input = self.driver.find_element_by_xpath(self.strong_pwd_length_input)
                    Domain_mgnt_page(self.driver).clear_input(pwd_length_input)  # 清空输入框
                    pwd_length_input.send_keys(kwargs[key])
                    time.sleep(1)

    @allure.step("限制客户端登录")
    def restricted_client_login(self, enable, options, **kwargs):
        WebDriverWait(self.driver, 60).until(
            ec.visibility_of_element_located((By.XPATH, self.el_restricted_client_login)))
        if enable == False:  # 不开启限制客户端登录
            pass
        else:
            self.driver.find_element_by_xpath(self.el_restricted_client_login).click()
            WebDriverWait(self.driver, 30).until(
                ec.visibility_of_element_located((By.XPATH, self.el_enable_restricted_client_login)))
            self.driver.find_element_by_xpath(self.el_enable_restricted_client_login).click()  # 开启限制客户端登录策略
            list1 = options.split("-")
            tp = tuple(list1)
            print(tp)
            # for i in range(len(tp)):
            if tp[0] == 'Web':
                self.driver.find_element_by_xpath(self.el_web_client_option).click()
                if tp[1] == 'Android':
                    self.driver.find_element_by_xpath(self.el_android_client_option).click()
                    if tp[2] == 'ios':
                        self.driver.find_element_by_xpath(self.el_ios_client_option).click()
                        if tp[3] == 'mobile_web':
                            self.driver.find_element_by_xpath(self.el_mobile_web_option).click()

    @allure.step("双因子认证")
    def two_factor_auth(self, enable, option, pwd_count=None):
        try:
            if not enable:
                pass
            elif enable:
                if option in ["账号密码", "账号密码 + 图形验证码", "账号密码 + 短信验证码", "账号密码 + 动态密码"]:
                    self.driver.find_element_by_xpath(self.el_two_factor_auth).click()
                    WebDriverWait(self.driver, 20).until(
                        ec.visibility_of_element_located((By.XPATH, self.el_enable_two_factor_auth)))
                    self.driver.find_element_by_xpath(self.el_enable_two_factor_auth).click()
                    self.driver.find_element_by_xpath(self.el_selcet_icon).click()
                    # el_option = f"//li[div[div[span[text()='{option}']]]]"
                    el_option = f"//span[text()='{option}']"
                    WebDriverWait(self.driver, 20).until(ec.visibility_of_element_located((By.XPATH, el_option)))
                    self.driver.find_element_by_xpath(el_option).click()
                    # try:
                    if option == "账号密码 + 图形验证码":
                        WebDriverWait(self.driver, 20).until(
                            ec.visibility_of_element_located((By.XPATH, self.el_control_wrong_password)))
                        password_element = self.driver.find_element_by_xpath(self.el_control_wrong_password)
                        if pwd_count is not None:
                            Domain_mgnt_page(self.driver).clear_input(password_element)
                            password_element.send_keys(pwd_count)
                    if option == "账号密码 + 短信验证码":
                        WebDriverWait(self.driver, 20).until(
                            ec.visibility_of_element_located((By.XPATH, self.el_SMS_code_tip)))
                    if option == "账号密码 + 动态密码":
                        WebDriverWait(self.driver, 20).until(
                            ec.visibility_of_element_located((By.XPATH, self.el_dynamic_tip)))
                    # except Exception as e:
                    #
                    #     raise e("登录认证提示语元素不存在或输入密码错误次数失败")
        except Exception:
            raise
            # raise e("传入的参数值不合法")

    @allure.step("获取新增策略列表首行信息")
    def get_policy_info(self):
        el_policy_info = self.driver.find_element_by_xpath(self.el_policy_first).text
        return el_policy_info

    @allure.step("获取绑定文档域列表首行信息")
    def get_apply_domain_info(self):
        time.sleep(3)
        el_doamin_info = self.driver.find_element_by_xpath(self.el_apply_domain_first).text
        time.sleep(2)
        return el_doamin_info

    @allure.step("策略绑定文档域")
    def apply_domain(self, domain_name):
        el_child = f"//a[span[@title='{domain_name}']]"
        time.sleep(2)
        self.driver.find_element_by_xpath(self.el_add_domain).click()
        el_new = WebDriverWait(self.driver, 60).until(
            ec.visibility_of_element_located((By.XPATH, self.is_submit)))
        self.driver.find_element_by_xpath(el_child).click()
        # self.driver.execute_script("$(arguments[0]).click()", self.driver.find_element_by_xpath(el_child))
        el_new.click()

    @allure.step("策略配置--删除绑定的文档域")
    def unbind_domain(self, domain_name, is_submit=True):
        el_name = "//td[div[div[div[span[text()='{}']]]]]/following-sibling::td/div/div/button".format(domain_name)
        self.driver.find_element_by_xpath(el_name).click()
        WebDriverWait(self.driver, 20).until(ec.visibility_of_element_located((By.XPATH, self.el_applydomain_hinticon)))
        time.sleep(2)
        if is_submit:
            self.driver.find_element_by_xpath(self.is_submit).click()
        else:
            self.driver.find_element_by_xpath(self.is_hintpoop_cancel).click()
        time.sleep(2)

    @allure.step("策略配置--删除策略")
    def delete_policy(self, policy_name):
        el_name = "//td[div[div[div[span[text()='{}']]]]]/following-sibling::td/div/div/div[2]/button".format(policy_name)
        self.driver.find_element_by_xpath(el_name).click()
        WebDriverWait(self.driver, 60).until(
            ec.visibility_of_element_located((By.XPATH, self.el_delete_policy_pop)))
        self.driver.find_element_by_xpath(self.is_submit).click()
        time.sleep(2)

    @allure.step("策略配置--绑定文档域弹窗--文档域列表行数")
    def get_apply_domain_poplist_count(self):
        el_tree = "//div[contains(@class,'domain-tree')]/div/div"
        tree = self.driver.find_element_by_xpath(el_tree)
        elements = tree.find_elements_by_tag_name("div")
        print(len(elements))
        return len(elements) / 2

    @allure.step("添加策略配置--检查策略")
    def get_policy(self, line, policy_name):
        el_policy = f"//div[{line}]/div[1]/div[text() = '{policy_name}']"
        return el_policy

    @allure.step("删除策略失败--已绑定文档域")
    def delete_policy_fail(self, policy_name):
        el_name = f"//td[div[div[div[span[text()='{policy_name}']]]]]/following-sibling::td/div/div/div[2]/button"
        self.driver.find_element_by_xpath(el_name).click()
        time.sleep(2)
        self.driver.find_element_by_xpath(self.is_submit).click()

    @allure.step("判断元素是否有某个属性")
    def attribute_is_present(self, xpath, attribute):
        try:
            self.driver.find_element_by_xpath(xpath).get_attribute(attribute)
        except NoSuchAttributeException:
            return False
        else:
            return True

    @allure.step("编辑策略")
    def edit_policy(self, policy_name, edit_policy_name=None, item=None, enable=False, strength='weak', is_submit=True,
                    options=None, option=None, pwd_count=None, **kwargs):
        el_edit_policy = f"//span[text()='{policy_name}']/../../../../../td[2]/div/div[1]/div[1]/div[1]/button"
        time.sleep(2)
        self.driver.find_element_by_xpath(el_edit_policy).click()
        if edit_policy_name is not None:
            Domain_mgnt_page(self.driver).clear_input(self.driver.find_element_by_xpath(self.el_policy_name))
            time.sleep(2)
            self.driver.find_element_by_xpath(self.el_policy_name).send_keys(edit_policy_name)
            time.sleep(2)

        if item == "pwd_strength":
            self.pwd_strength(enable, strength, **kwargs)
        if item == "client_login":
            self.restricted_client_login(enable, options)
        if item == "two_factor_auth":
            self.two_factor_auth(enable, option, pwd_count)

        if is_submit:
            self.driver.find_element_by_xpath(self.el_edit_confirm_button).click()
        else:
            self.driver.find_element_by_xpath(self.el_edit_cancel_button).click()

    @allure.step("清除文本框内容")
    def clear_input(self, element):
        if self.driver.desired_capabilities["browserName"] == "Safari":
            element.send_keys(Keys.COMMAND, 'a')
            element.send_keys(Keys.COMMAND, Keys.DELETE)
        else:
            element.send_keys(Keys.CONTROL, 'a')
            element.send_keys(Keys.DELETE)

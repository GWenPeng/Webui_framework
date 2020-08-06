from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
import time
import allure


class user_org_mgnt_page(object):
    """
    用户组织管理页面
    """

    def __init__(self, driver):
        self.driver = driver
        # self.driver = webdriver.Chrome()
        self.el_dept_mgnt = "a#m-depMgm"  # 部门管理元素 css
        self.el_user_mgnt = "#m-userMgm > span > span"  # 用户管理tab css
        self.el_doc_conf_mgnt = "m-documentMgm"  # 文档配置管理tab id
        # <---------------------------------------------------------------->以下为用户列表显示页面
        self.el_login_name = "div.ui-dataview-field-loginName"  # 用户名称 css
        self.el_display_name = "div.ui-dataview-field-displayName>div>span:nth-child(2)"  # 显示名称 css
        # <----------------------------------------------------------------->以下是初始化配置弹窗
        self.el_setup_conf = "h1._-_-_-_-node_modules--anyshare-ui-lib-Dialog2-styles-desktop---title"  # 初始化弹窗title css
        self.el_bt_confirm = 'div._-_-_-_-node_modules--anyshare-ui-lib-Panel-Footer-styles-desktop---container>div' \
                             '>button '  # 初始化弹窗确定按钮 css

    @allure.step("判断是否要关闭弹窗")
    def is_close_setup_conf(self):
        try:
            if self.driver.find_element_by_css_selector(self.el_setup_conf).is_displayed():
                is_dispalyed = True
            else:
                is_dispalyed = False
        except NoSuchElementException as e:
            print(e)
            is_dispalyed = False
        if is_dispalyed:
            self.driver.find_element_by_css_selector(self.el_bt_confirm).click()


class department_mgnt_module(user_org_mgnt_page):
    """
    部门管理模块
    """

    def __init__(self, driver):
        super().__init__(driver)
        # self.driver = webdriver.Chrome()

        self.el_create_org = "mm-depMgm-createOrganization"  # 创建组织元素 id
        self.el_edit_org = "mm-depMgm-editOrganization"  # 编辑组织元素 id
        self.el_del_org = "mm-depMgm-delOrganization"  # 删除组织元素 id
        self.el_new_create_department = "mm-depMgm-new"  # 新建部门元素 id
        self.el_edit_department = "mm-depMgm-edit"  # 编辑部门元素 id
        # <-------------------------------------------------------------->以下是新建组织弹窗
        self.el_org_name = "input#textOrganizationName"  # 组织名称元素 css
        self.el_org_eamil = "input#createOrganizationEmail"  # 邮箱输入框 css
        self.el_org_owner_site = "select#createOrganization-site"  # 归属站点 css
        self.el_org_comfirm = "#createOrganization > div.dialog-button > a:nth-child(1) > span > span"  # 确定按钮 css
        self.el_org_cancel = "#createOrganization > div.dialog-button > a:nth-child(2) > span > span"  # 取消按钮 css
        # <------------------------------------------------------------->以下是新建部门弹窗元素
        self.el_department_name = "input#createDepartment-name"  # 部门名称输入框
        self.el_email = "input#createDepartment-email"  # 邮箱地址输入框
        self.el_owner_site = "select#createDepartment-site"  # 归属站点选择框
        self.el_option_loclhost = "#createDepartment-site > option"  # localhost option选项
        self.el_confirm = "#createDepartment > div.dialog-button > a:nth-child(1) > span > span"  # 确定按钮
        self.el_cancel = "#createDepartment > div.dialog-button > a:nth-child(2) > span > span"  # 取消按钮

    @allure.step("新建组织")
    def new_create_org(self, org_name, is_submit=True, **kwargs):
        """

        :param is_submit: 是否确认提交，默认为True
        :param org_name: 组织名称
        :param kwargs: 可以传email 或owner_site
        :return:
        """
        ac = ActionChains(driver=self.driver)
        WebDriverWait(driver=self.driver, timeout=60).until(
            ec.visibility_of_element_located((By.CSS_SELECTOR, self.el_dept_mgnt)))
        el_dept_mgnt = self.driver.find_element_by_css_selector(self.el_dept_mgnt)  # 部门管理元素
        ac.move_to_element(el_dept_mgnt).perform()  # 鼠标移动至部门管理元素位置
        # self.driver.find_element_by_id(self.el_create_org).click()  # 点击创建组织元素
        el_create_org = WebDriverWait(self.driver, 60, 1).until(
            ec.visibility_of(self.driver.find_element_by_id(self.el_create_org)))  # 创建组织元素
        ac.move_to_element(el_create_org).perform()  # 移动至创建组织
        el_create_org.click()  # 点击创建组织
        self.driver.find_element_by_css_selector(self.el_org_name).send_keys(org_name)  # 输入组织名称
        for key in kwargs:
            if key == "email":
                self.driver.find_element_by_css_selector(self.el_org_eamil).send_keys(kwargs[key])  # 输入email地址
            elif key == "owner_site":
                el_select = self.driver.find_element_by_css_selector(self.el_org_owner_site)
                # Select(el_select).select_by_value(kwargs[key])  # 根据value值选择option
                Select(el_select).select_by_visible_text(kwargs[key])  # 根据value值选择option

        if is_submit:
            WebDriverWait(self.driver, 10, 1).until(
                ec.element_to_be_clickable((By.CSS_SELECTOR, self.el_org_comfirm))).click()
            # el.click()  # 点击确定按钮
            # time.sleep(3)
        elif not is_submit:
            self.driver.find_element_by_css_selector(self.el_org_cancel).click()  # 点击取消按钮

    @allure.step("新建部门")
    def new_create_department(self, department_name, is_submit=True, **kwargs):
        """

        :param department_name: 部门名称
        :param is_submit: 是否确认提交
        :param kwargs:可以传email 或owner_site
        :return:
        """
        ac = ActionChains(driver=self.driver)
        WebDriverWait(driver=self.driver, timeout=60).until(
            ec.visibility_of_element_located((By.CSS_SELECTOR, self.el_dept_mgnt)))
        el_dept_mgnt = self.driver.find_element_by_css_selector(self.el_dept_mgnt)  # 部门管理元素
        ac.move_to_element(el_dept_mgnt).perform()  # 鼠标移动至部门管理元素位置
        el_new_create_department = WebDriverWait(self.driver, 60, 1).until(
            ec.visibility_of(self.driver.find_element_by_id(self.el_new_create_department)))  # 新建部门元素
        ac.move_to_element(el_new_create_department).perform()  # 移动至新建部门元素
        el_new_create_department.click()  # 点击新建部门
        self.driver.find_element_by_css_selector(self.el_department_name).send_keys(department_name)  # 输入部门名称
        for key in kwargs:
            if key == "email":
                self.driver.find_element_by_css_selector(self.el_email).send_keys(kwargs[key])  # 输入email地址
            elif key == "owner_site":
                el_select = self.driver.find_element_by_css_selector(self.el_owner_site)
                Select(el_select).select_by_visible_text(kwargs[key])  # 根据text值选择option

        # self.driver.find_element_by_css_selector(self.el_confirm).click()  # 点击确定按钮
        # self.driver.find_element_by_css_selector(self.el_cancel).click()
        if is_submit:
            WebDriverWait(self.driver, 10, 1).until(
                ec.element_to_be_clickable((By.CSS_SELECTOR, self.el_confirm))).click()
            # el.click()  # 点击确定按钮
            # time.sleep(3)
        elif not is_submit:
            self.driver.find_element_by_css_selector(self.el_cancel).click()  # 点击取消按钮


class user_mgnt_module(user_org_mgnt_page):
    """
    用户管理模块
    """

    def __init__(self, driver):
        super().__init__(driver)
        # <-------------------------------------------------------> 以下是用户管理下拉选项
        self.el_new_creat = "mm-userMgm-new"  # 新建用户按钮
        self.el_del_user = "mm-userMgm-del"  # 删除用户
        self.el_manage_pwd = "//div[text()='管控密码']"  # 管控密码
        # <-------------------------------------------------------> 以下是新建用户弹窗元素
        self.el_username = "//label[text()='用户名：']/../div/div/input"  # 用户名输入框元素
        self.el_showname = "//label[text()='显示名：']/../div/div/input"  # 显示名输入框元素
        self.el_remark = "user-remark"  # 备注输入框元素
        self.el_email = "createUser-email"  # 邮箱地址输入框元素
        self.el_mobile = "//label[text()='手机号码：']/../div/div/input"  # 手机号码输入框元素
        self.el_IDcard = "createUser-idcardNumber"  # 身份证输入框元素
        self.el_User_csf_level = "createUser-csf-level"  # 用户密级选择框
        self.el_valid_period = "_-_-_-_-node_modules--anyshare-console-lib-ValidityBox2-styles-view---text"  # 有限期选择框 class
        self.el_owner_site = "createUser-site"  # 归属站点选择框
        self.el_quota_space = "createUser-quota-space"  # 配额空间选择框
        self.el_confirm = "//h1[text()='新建用户']/../../div[2]/div/div[2]/div/button[1]"  # 确定按钮 css
        self.el_cancel = "//h1[text()='新建用户']/../../div[2]/div/div[2]/div/button[1]"  # 取消按钮 css
        self.el_close = "a.panel-tool-close"  # 关闭弹窗按钮 css
        # <------------------------------------------------------>以下是删除用户确认弹窗
        self.el_del_user_verify = 'button[type="submit"]'  # 删除用户确认按钮
        self.el_del_user_cancel = 'button[type="button"]'  # 删除用户取消按钮
        # <------------------------------------------------------>管控密码弹窗
        self.el_allow_user = "//span[text()='不允许用户自主修改密码']/../input"  # 不允许用户自主修改密码
        self.el_pwd_input = "//label[text()='用户密码：']/../div/div/input"  # 密码输入框
        self.el_is_button = "//h1[text()='管控密码']/../../div[2]/div/div[2]/div[1]/button[1]"  # 管控密码确认按钮

    @allure.step("创建用户")
    def create_user(self, username, showname, is_submit=True, **kwargs):
        """
        user_security="", valid_period="",
        :param is_submit:
        :param username:
        :param showname:
        :param kwargs:
        :return:
        """
        ac = ActionChains(driver=self.driver)
        WebDriverWait(driver=self.driver, timeout=60).until(
            ec.visibility_of_element_located((By.CSS_SELECTOR, self.el_user_mgnt)))
        el_user_mgnt = self.driver.find_element_by_css_selector(self.el_user_mgnt)  # 用户管理元素
        ac.move_to_element(el_user_mgnt).perform()  # 鼠标移至用户管理按钮上
        el_user_mgnt.click()
        # time.sleep(2)
        el_new = WebDriverWait(self.driver, 60, 1).until(
            ec.visibility_of(self.driver.find_element_by_id(self.el_new_creat)))  # 新建用户按钮
        # el_new = self.driver.find_element_by_id(self.el_new_creat)  # 新建用户按钮
        ac.move_to_element(el_new).perform()
        el_new.click()  # 点击新建用户
        self.driver.find_element_by_xpath(self.el_username).send_keys(username)  # 输入用户名
        self.driver.find_element_by_xpath(self.el_showname).send_keys(showname)  # 输入显示名
        for key in kwargs:
            if key == "remark":
                self.driver.find_element_by_id(self.el_remark).send_keys(kwargs[key])  # 输入备注
            elif key == "email":
                self.driver.find_element_by_id(self.el_email).send_keys(kwargs[key])  # 输入邮箱地址
            elif key == "mobile":
                self.driver.find_element_by_xpath(self.el_mobile).send_keys(kwargs[key])  # 输入手机号
            elif key == "IDcard":
                self.driver.find_element_by_id(self.el_IDcard).send_keys(kwargs[key])  # 输入身份证号
            elif key == "quota_space":
                el_q_space = self.driver.find_element_by_id(self.el_quota_space)
                el_q_space.clear()
                el_q_space.send_keys(kwargs[key])  # 输入配额空间
        if is_submit:
            WebDriverWait(self.driver, 10, 1).until(
                ec.element_to_be_clickable((By.XPATH, self.el_confirm))).click()
            # el.click()  # 点击确定按钮
            # time.sleep(3)
        elif not is_submit:
            self.driver.find_element_by_xpath(self.el_cancel).click()  # 点击取消按钮
        # elif is_submit == "close":
        #     self.driver.find_element_by_css_selector(self.el_close).click()  # 关闭弹窗按钮

        # time.sleep(10)
        # search_js = "document.getElementById('mm-userMgm-new').click();"
        # new_creat_user = self.driver.find_element_by_id("mm-userMgm-new")
        # self.driver
        # search_js = '$(document.querySelector("#mm-userMgm-new")).click();'
        # self.driver.execute_script(search_js)
        # self.driver.find_element_by_xpath('//*[@id="mm-userMgm-new"]/div').click()
        # time.sleep(2)

        # new_creat_user.click()

    @allure.step("删除用户")
    def del_user(self, is_del_user_verify=True):
        Doc_conf_mgnt_moudle(self.driver).close_personal_doc()  # 调用关闭个人文档方法
        ac = ActionChains(driver=self.driver)
        el_user_mgnt = self.driver.find_element_by_css_selector(self.el_user_mgnt)  # 用户管理元素
        ac.move_to_element(el_user_mgnt).perform()  # 鼠标移至用户管理按钮上
        el_del_user = WebDriverWait(self.driver, 60, 1).until(
            ec.visibility_of(self.driver.find_element_by_id(self.el_del_user)))
        # time.sleep(3)
        # el_del_user = self.driver.find_element_by_id(self.el_del_user)
        ac.move_to_element(el_del_user).perform()
        # time.sleep(3)
        el_del_user.click()  # 点击删除用户
        self.is_del_user(is_del_user_verify)  # 是否确认删除用户

    @allure.step("再次确认是否删除用户")
    def is_del_user(self, is_del=True):
        if is_del:
            self.driver.find_element_by_css_selector(self.el_del_user_verify).click()  # 点击确认删除按钮
        elif not is_del:
            self.driver.find_element_by_css_selector(self.el_del_user_cancel).click()  # 点击取消按钮

    @allure.step("管控用户密码")
    def control_pwd(self, user_name, allow="is", pwd=None):
        el_select_user = f"//span[text()='{user_name}']/../../div[1]/input"
        self.driver.find_element_by_xpath(el_select_user).click()  # 选择用户
        ac = ActionChains(driver=self.driver)
        el_user_mgnt = self.driver.find_element_by_css_selector(self.el_user_mgnt)  # 用户管理元素
        ac.move_to_element(el_user_mgnt).perform()  # 鼠标移至用户管理按钮上
        el_user_mgnt.click()
        manage_pwd = self.driver.find_element_by_xpath(self.el_manage_pwd)
        manage_pwd.click()
        if allow != "is":
            time.sleep(1)
            allow_user = self.driver.find_element_by_xpath(self.el_allow_user)
            allow_user.click()
            time.sleep(1)
            pwd_input = self.driver.find_element_by_xpath(self.el_pwd_input)
            pwd_input.send_keys(pwd)
            time.sleep(1)
            is_button = self.driver.find_element_by_xpath(self.el_is_button)
            is_button.click()


class Doc_conf_mgnt_moudle(user_org_mgnt_page):
    """
    文档配置管理模块
    """

    def __init__(self, driver):
        super().__init__(driver)
        # <--------------------------------------------------------> 以下为文档配置管理下拉选项
        self.el_close_personal_doc = "mm-documentMgm-close"  # 关闭个人文档选项 id
        # <-------------------------------------------------------->以下为关闭个人文档弹窗元素
        self.el_org_department = "close-document-range"  # 组织管理部门选项框 id select option
        self.el_option_department = "#close-document-rang>option:nth-child"  # 部门option选项值 css
        self.el_move_to_assign_doc = 'label[for="close-document-move"]'  # 迁移至指定文档库选项 css
        self.el_complete_del = 'label[for="close-document-delete"]'  # 彻底删除选项 css
        self.el_confirm = 'confirm-btn'  # 确定按钮 id
        self.el_cancel = "#close-document>div.dialog-button>a:nth-child(2)"  # 取消按钮 css
        self.el_pwd = "input#pwd"  # 密码输入框 css
        # <------------------------------------------------------------>以下是关闭个人文档再次确认弹窗
        self.el_again_confirm = "div.messager-button>a:nth-child(1)"  # 再次确认按钮
        self.el_agein_cancel = "div.messager-button>a:nth-child(2)"  # 再次取消按钮

    @allure.step("关闭个人文档")
    def close_personal_doc(self, is_complete_del=True, pwd="eisoo.com", is_submit=True, verify_close=True, **kwargs):
        el = self.driver.find_element_by_id(self.el_doc_conf_mgnt)  # 文档配置管理元素
        ac = ActionChains(driver=self.driver)
        ac.move_to_element(el).perform()  # 鼠标移动至文档配置管理tab
        el_cl = WebDriverWait(self.driver, 60, 1).until(
            ec.visibility_of(self.driver.find_element_by_id(self.el_close_personal_doc)))
        # time.sleep(2)
        # el_cl = self.driver.find_element_by_id(self.el_close_personal_doc)
        ac.move_to_element(el_cl).perform()  # 鼠标移动至关闭个人文档选项
        # time.sleep(2)
        el_cl.click()

        for key in kwargs:
            if key == "option":  # 你关闭的组织部门选项 0为部门成员 1为组织管理及其子部门成员
                self.driver.find_element_by_id(self.el_org_department).click()
                self.driver.find_element_by_css_selector(self.el_option_department + "(" + kwargs[key] + ")")
        if is_complete_del:  # 彻底删除
            self.driver.find_element_by_css_selector(self.el_complete_del).click()  # 点击彻底选项
            self.driver.find_element_by_css_selector(self.el_pwd).send_keys(pwd)  # 输入彻底删除
        elif not is_complete_del:  # 迁移至指定的文档库
            self.driver.find_element_by_css_selector(self.el_move_to_assign_doc).click()
        if is_submit:
            self.driver.find_element_by_id(self.el_confirm).click()
        elif not is_submit:
            self.driver.find_element_by_css_selector(self.el_cancel).click()
        self.is_close_doc(verify_close)  # 点击确认弹窗

    @allure.step("再次确认是否关闭个人文档")
    def is_close_doc(self, is_close=True):
        if is_close:
            self.driver.find_element_by_css_selector(self.el_again_confirm).click()  # 点击再次确认按钮
        elif not is_close:
            self.driver.find_element_by_css_selector(self.el_agein_cancel).click()  # 点击取消按钮

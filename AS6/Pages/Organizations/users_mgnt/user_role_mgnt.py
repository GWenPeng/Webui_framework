from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
from AS6.Pages.Login_page import Login_page
from selenium.webdriver.common.keys import Keys
from Common.parse_data import do_excel
import allure
import pytest


class UserRoleMgnt(object):
    """
    用户角色管理页面
    """

    def __init__(self, driver):
        self.driver = driver
        # self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)
        # 用户角色管理入口
        self.el_tab1 = "//span[text()='组织管理']"
        self.el_tab2 = "//div[contains(@class,'container')]/div/span/span[text()='用户管理']"
        self.el_tab3 = "//span[text()='用户角色管理']"
        # 新增角色页面
        self.el_add_role_button = "//button[span[text()='新增角色']]"
        self.el_add_role_title = "//h1[text()='新增角色']"
        self.el_role_name = "//div[label[text()='角色名称：']]/div/div/input"
        self.el_role_name_click = "//div[label[text()='角色名称：']]/div/div"
        self.el_role_feature = "//div[label[text()='角色职能：']]/div/div/textarea"
        self.el_add_role_ok = "//button[span[text()='确定']]"
        self.el_add_role_cancel = "//button[span[text()='取消']]"
        self.el_role_name_tip1 = "//span[text() = '角色名不能包含  / : * ? \" < > | 特殊字符，请重新输入。']"
        self.el_role_name_tip2 = "//div[text()='角色名称不合法，可能字符过长或包含  / : * ? \" < > | 特殊字符；']"
        self.el_role_feature_tip = "//div[text()='角色职能不能超过800个字。']"
        self.el_tip_button_ok = "//button[text()='确定']"
        # 删除角色
        self.el_div_tip = "//div[text()='提示']"
        self.el_delete_tip = "//div[text()='删除该角色将导致已拥有该角色的所有用户失去该角色，您确定要执行此操作吗？']"
        self.el_delete_ok = "//button[text()='确定']"
        self.el_delete_cancel = "//button[text()='取消']"
        # 编辑角色
        self.el_edit_h1 = "//h1[text()='编辑角色']"
        # 列表页面按钮
        self.el_clear_member_button = "//button[span[text()='清空成员']]"
        self.el_add_member_button = "//button[span[text()='添加成员']]"
        # 列表页面搜索框
        self.el_search_role = "//input[@placeholder='请输入角色名']"
        self.el_search_member = "//input[@placeholder='请输入角色成员']"
        # 添加成员页面
        self.el_add_member_h1 = "//h1[text()='添加成员']"
        self.el_add_member_search = "//input[@placeholder='查找']"
        self.el_add_member_clear = "//span[text()='清空']/preceding::button[1]"
        self.el_add_member_ok = "//button[span[text()='确定']]"
        self.el_add_member_cancel = "//button[span[text()='取消']]"

    # 入口检查
    @allure.step("入口检查")
    def check_entrance(self):
        self.wait.until(EC.presence_of_element_located((By.XPATH, self.el_tab2)))
        tab3 = self.driver.find_element_by_xpath(self.el_tab3)
        tab3.click()
        self.wait.until(EC.visibility_of_element_located((By.XPATH, self.el_add_role_button)))

    # 新增角色
    @allure.step("新增角色")
    def add_role(self, name, feture=None, opration="ok"):
        add_role_button = self.driver.find_element_by_xpath(self.el_add_role_button)  # 新增角色按钮
        add_role_button.click()
        self.wait.until(EC.visibility_of_element_located((By.XPATH, self.el_add_role_title)))  # 新增角色弹框
        role_name = self.driver.find_element_by_xpath(self.el_role_name)  # 角色名称
        role_feature = self.driver.find_element_by_xpath(self.el_role_feature)  # 角色职能
        button_ok = self.driver.find_element_by_xpath(self.el_add_role_ok)  # 确定
        button_cancel = self.driver.find_element_by_xpath(self.el_add_role_cancel)  # 取消
        role_name.send_keys(name)
        if feture is not None:
            role_feature.send_keys(feture)
        if opration == 'ok':
            button_ok.click()
        else:
            button_cancel.click()
        self.wait.until(EC.invisibility_of_element_located((By.XPATH,self.el_add_role_title)))

    @allure.step("删除角色")
    def delete_role(self,delete_name,operation="ok"):
        el_delete_role = f"//td[div[div[div[span[text()='{delete_name}']]]]]/following::td[3]/div/div/div/div[2]/div/button"
        self.driver.find_element_by_xpath(el_delete_role).click()
        self.wait.until(EC.visibility_of_element_located((By.XPATH,self.el_div_tip)))
        text = self.driver.find_element_by_xpath(self.el_delete_tip).text
        data = do_excel(filename="organizations/user_role_mgnt/user_role.xlsx", sheetname="提示语",
                        minrow=1, maxrow=1, mincol=2, maxcol=2)[0]
        assert text == data[0]
        try:
            if operation == "ok":
                self.driver.find_element_by_xpath(self.el_delete_ok).click()
            elif operation == "cancel":
                self.driver.find_element_by_xpath(self.el_delete_cancel).click()
        except ValueError as e:
            print("请输入确定'ok'或取消'cancel'!")
        self.wait.until(EC.invisibility_of_element_located((By.XPATH,self.el_div_tip)))

    @allure.step("编辑角色")
    def edit_role(self,rolename,operation,new_role_name=None,new_role_feature=None):
        el_edit_role = f"//td[div[div[div[span[text()={rolename}]]]]]/following::td[3]/div/div/div/div[1]/div/button"
        el_role_feture_value = f"(//td[div[div[div[span[text()={rolename}]]]]]/following::td)[1]/div/div/div/span"
        el_role_creator = f"(//td[div[div[div[span[text()={rolename}]]]]]/following::td)[2]/div/div/div/span"
        role_feture_text = self.driver.find_element_by_xpath(el_role_feture_value).text
        role_creator = self.driver.find_element_by_xpath(el_role_creator)
        self.driver.find_element_by_xpath(el_edit_role).click()
        self.wait.until(EC.visibility_of_element_located((By.XPATH,self.el_edit_h1)))
        role_name = self.driver.find_element_by_xpath(self.el_role_name)
        role_feature = self.driver.find_element_by_xpath(self.el_role_feature)
        role_name_value = role_name.get_attribute('value')
        role_feature_value = role_feature.get_attribute('value')
        assert role_name_value == rolename
        assert role_feature_value == role_feture_text
        if new_role_feature is None and new_role_name is None:
            if operation == "ok" or operation == "cancel":
                self.driver.find_element_by_xpath(self.el_add_role_ok).click()
                self.wait.until(EC.invisibility_of_element_located((By.XPATH, self.el_edit_h1)))
                assert self.get_role_info() == [rolename,role_feture_text,role_creator]
        else:
            role_name.send_keys(Keys.CONTROL, 'a')
            role_name.send_keys(Keys.DELETE)
            role_feature.send_keys(Keys.CONTROL, "a")
            role_feature.send_keys(Keys.DELETE)
            self.driver.find_element_by_xpath(self.el_role_name).send_keys(new_role_name)
            self.driver.find_element_by_xpath(self.el_role_feature).send_keys(new_role_feature)
            if operation == "ok":
                self.driver.find_element_by_xpath(self.el_add_role_ok).click()
                self.wait.until(EC.invisibility_of_element_located((By.XPATH, self.el_edit_h1)))
                assert self.get_role_info() == [new_role_name,new_role_feature,role_creator]
            elif operation == "cancel":
                self.driver.find_element_by_xpath(self.el_add_role_cancel).click()
                self.wait.until(EC.invisibility_of_element_located((By.XPATH, self.el_edit_h1)))
                assert self.get_role_info() == [rolename, role_feture_text, role_creator]

    @allure.step("获取角色列表")
    def get_role_list(self):
        tbody = self.driver.find_element_by_xpath("(//tbody)[1]")
        tr = tbody.find_elements_by_tag_name('tr')
        print(len(tr))
        row = []
        roles = []
        for i in range(1, len(tr) + 1):
            for j in range(1, 4):
                path = f"tr:nth-child({i})>td:nth-child({j})>div>div>div>span"
                element = tbody.find_element_by_css_selector(path)
                row.append(element.text)
            roles.append(row[i * 3 - 3: i * 3])
        print(roles)
        return roles

    @allure.step("获取第一个角色的信息")
    def get_role_info(self):
        tbody = self.driver.find_element_by_xpath("(//tbody)[1]")
        row = []
        for j in range(1, 4):
            path = f"tr:nth-child(1)>td:nth-child({j})>div>div>div>span"
            element = tbody.find_element_by_css_selector(path)
            row.append(element.text)
        return row

    @allure.step("获取角色名称")
    def get_role_name(self,count):
        tbody = self.driver.find_element_by_xpath("(//tbody)[1]")
        row = []
        for i in range(1, count+1):
            path = f"tr:nth-child({i})>td:nth-child(1)>div>div>div>span"
            element = tbody.find_element_by_css_selector(path)
            row.append(element.text)
        return row

    @allure.step("获取角色成员列表")
    def get_member_list(self):
        tbody = self.driver.find_element_by_xpath("(//tbody)[2]")
        tr = tbody.find_elements_by_tag_name('tr')
        print(len(tr))
        row = []
        roles = []
        for i in range(1, len(tr) + 1):
            for j in range(1, 4):
                path = f"tr:nth-child({i})>td:nth-child({j})>div>div>div>span"
                element = tbody.find_element_by_css_selector(path)
                row.append(element.text)
            roles.append(row[i * 3 - 3: i * 3])
        print(roles)
        return roles

    @allure.step("选择角色")
    def choose_role(self, role):
        role_name = self.driver.find_element_by_xpath(f"//span[text()={role}[1]")
        role_name.click()

    @allure.step("元素是否灰化")
    def element_is_disabled(self, xpath):
        element = self.driver.find_element_by_xpath(xpath)
        return element.get_attribute("disabled")

    # 清空成员
    @allure.step("清空成员")
    def clear_members(self):
        clear_member = self.driver.find_element_by_xpath(self.el_clear_member_button)
        clear_member.click()

    # 添加成员
    @allure.step("添加成员")
    def add_member(self, orgname, rolename):
        add_member_button = self.driver.find_element_by_xpath(self.el_add_member_button)
        expand_org_icon = self.driver.find_element_by_xpath(f"//a[span[@title={orgname}]]/preceding-sibling::span[1]")
        choose_user = self.driver.find_element_by_xpath(
            f"//span[contains(@class,'OrganizationTree')][text()={rolename}]")
        add_member_button.click()
        self.wait.until(EC.visibility_of_element_located((By.XPATH, self.el_add_member_h1)))
        expand_org_icon.click()
        self.wait.until(EC.visibility_of_element_located(choose_user, visibility=True))
        choose_user.click()


# if __name__ == '__main__':
    # driver = webdriver.Chrome()
    # driver.maximize_window()
    # driver.get("http://10.2.64.235:8000")
    # Login_page(driver).login(username="admin", password="eisoo.cn")
    # a = UserRoleMgnt(driver=driver)
    # a.check_entrance()

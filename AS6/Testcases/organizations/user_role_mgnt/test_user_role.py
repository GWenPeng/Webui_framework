from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from AS6.Pages.Organizations.users_mgnt.user_role_mgnt import UserRoleMgnt
from Common.parse_data import do_excel
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pytest
import allure


class Test_Add_Role:

    @pytest.fixture(scope='class',autouse=True)
    def check_entrance(self,driver):
        UserRoleMgnt(driver).check_entrance()
        yield
        # driver.quit()

    @allure.testcase("519 用户角色管理--页面检查,"
                     "522 用户角色管理--创建者栏")
    def test_check_role(self,driver):
        UserRole = UserRoleMgnt(driver)
        roles = UserRole.get_role_list()
        el_clear_member_button = UserRole.el_clear_member_button
        el_add_member_button = UserRole.el_add_member_button
        clear_member_button_status = UserRole.element_is_disabled(el_clear_member_button)
        add_member_button_status = UserRole.element_is_disabled(el_add_member_button)
        data = do_excel(filename="organizations/user_role_mgnt/user_role.xlsx", sheetname="默认角色",
                        minrow=2, maxrow=7, mincol=1, maxcol=3)
        print(data)
        data1 = []
        for i in data:
            list(i)
            data1.append(list(i))
        print(data1)
        assert roles == data1
        assert clear_member_button_status == "true"
        assert add_member_button_status == "true"

    @allure.testcase("6992 用户角色管理-新增角色成功"
                     "465 用户角色管理-删除自定义角色")
    @pytest.mark.high
    def test_add_role_success(self,driver):
        UserRole = UserRoleMgnt(driver)
        data = do_excel(filename="organizations/user_role_mgnt/user_role.xlsx",sheetname="新增角色",
                        minrow=2,maxrow=3,mincol=1,maxcol=3)
        super_admin = do_excel(filename="organizations/user_role_mgnt/user_role.xlsx", sheetname="默认角色",
                                    minrow=2, maxrow=2, mincol=1, maxcol=1)[0]
        for i in range(0, len(data)):
            data1 = data[i]
            UserRole.add_role(data1[0], data1[1])
            info = UserRole.get_role_info()
            if data1[1] is None:
                assert info == [data1[0], '---', data1[2]]
            else:
                assert info == [data1[0], data1[1], data1[2]]
            UserRole.delete_role(str(data1[0]))
            assert UserRole.get_role_name(count=1)[0] == super_admin[0]

    @allure.testcase("6993 用户角色管理--新增角色--角色名称不合法"
                     "6994 用户角色管理-新增角色-角色职能不合法")
    @pytest.mark.high
    def test_add_role_fail(self, driver):
        UserRole = UserRoleMgnt(driver)
        self.data = do_excel(filename="organizations/user_role_mgnt/user_role.xlsx", sheetname="新增角色",
                             minrow=4, maxrow=8, mincol=1, maxcol=3)
        self.tip = do_excel(filename="organizations/user_role_mgnt/user_role.xlsx", sheetname="提示语",
                            minrow=2, maxrow=4, mincol=2, maxcol=2)
        self.super_admin = do_excel(filename="organizations/user_role_mgnt/user_role.xlsx", sheetname="默认角色",
                                    minrow=2, maxrow=2, mincol=1, maxcol=1)[0]
        add_role_button = driver.find_element_by_xpath(UserRole.el_add_role_button)  # 新增角色按钮
        add_role_button.click()
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, UserRole.el_add_role_title)))  # 新增角色弹框
        role_name = driver.find_element_by_xpath(UserRole.el_role_name)
        role_feature = driver.find_element_by_xpath(UserRole.el_role_feature)
        button_ok = driver.find_element_by_xpath(UserRole.el_add_role_ok)
        for i in range(0, len(self.data)):
            data1 = self.data[i]
            role_name.send_keys(data1[0])
            role_feature.send_keys(data1[1])
            button_ok.click()
            if i < len(self.data) - 1:
                if i == len(self.data) - 2:
                    driver.implicitly_wait(3)
                    tip2 = driver.find_element_by_xpath(UserRole.el_role_name_tip2).text
                    driver.implicitly_wait(6)
                    assert tip2 == self.tip[0][0]
                    driver.find_element_by_xpath(UserRole.el_tip_button_ok).click()
                    driver.implicitly_wait(3)
                else:
                    driver.find_element_by_xpath(UserRole.el_role_name_click).click()
                    driver.implicitly_wait(3)
                    text = driver.find_element_by_xpath(UserRole.el_role_name_tip1).text
                    driver.implicitly_wait(3)
                    assert text == self.tip[1][0]
                role_name.send_keys(Keys.CONTROL, 'a')
                role_name.send_keys(Keys.DELETE)
                role_feature.send_keys(Keys.CONTROL, "a")
                role_feature.send_keys(Keys.DELETE)
            elif i == len(self.data) - 1:
                error_feature_tip = driver.find_element_by_xpath(UserRole.el_role_feature_tip).text
                assert error_feature_tip == self.tip[2][0]
                driver.find_element_by_xpath(UserRole.el_add_role_cancel).click()
                WebDriverWait(driver, 10).until(
                    EC.invisibility_of_element_located((By.XPATH, UserRole.el_add_role_title)))










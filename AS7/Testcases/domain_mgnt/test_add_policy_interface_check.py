# coding=utf-8
from AS7.Pages.Domain_mgnt.domain_mgnt_home_page import Domain_mgnt_home_page
from AS7.Pages.Domain_mgnt.doc_policy_page import doc_policy_page
from Common.parse_data import do_excel
from Common.screenshot import ScreenShot
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

# from Common.screenshot import Screen_shot
from Common.mysqlconnect import DB_connect
from Common.thrift_client import Thrift_client
from ShareMgnt import ncTShareMgnt

import pytest
import allure
import time


class Test_AddPolicyInterfaceCheck:

    # @pytest.fixture(scope='function')
    @allure.testcase("caseid:5494,策略同步-添加策略配置弹窗检查")
    @pytest.mark.high
    @pytest.mark.jt_suite
    def test_add_policy_interface1_check(self, driver):
        # try:
            Domain_mgnt_home_page(driver).return_domain_home_page()   # 进入文档域管理
            Domain_mgnt_home_page(driver).policy_sync()  # 进入策略同步
            add_policy = doc_policy_page(driver).el_add_policy
            WebDriverWait(driver, 60).until(ec.visibility_of_element_located((
                By.XPATH, add_policy)))  # 等待新增策略按钮出现
            driver.find_element_by_xpath(add_policy).click()  # 点击新增策略按钮
            policy_name = doc_policy_page(driver).el_policy_name
            WebDriverWait(driver, 60).until(ec.visibility_of_element_located((
                By.XPATH, policy_name)))  # 等待弹窗出现
            value_policy_name = driver.find_element_by_xpath(policy_name).get_attribute("value")
            assert value_policy_name == ""  # 断言策略配置名称输入框为空
            policy_search = doc_policy_page(driver).el_policy_search
            search_placeholder = driver.find_element_by_xpath(policy_search).get_attribute("placeholder")
            assert search_placeholder == "搜索"  # 断言搜索框内的占位符
            policy_password_status = doc_policy_page(driver).el_password_status
            password_status = driver.find_element_by_xpath(policy_password_status).text
            assert password_status == "未启用"  # 断言密码强度的状态
            restricted_client = doc_policy_page(driver).el_restricted_client_status
            restricted_client_status = driver.find_element_by_xpath(restricted_client).text
            assert restricted_client_status == "未启用"  # 断言限制客户端登录的状态
            el_two_factor_authentication = doc_policy_page(driver).el_two_factor_authentication_status
            two_factor_authentication_status = driver.find_element_by_xpath(el_two_factor_authentication).text
            assert two_factor_authentication_status == "未启用"  # 断言双因子认证的状态
            confirm_button = doc_policy_page(driver).el_confirm_button
            confirm_button_status = driver.find_element_by_xpath(confirm_button).get_attribute("class")
            assert confirm_button_status.split("-")[-1] != "disabled"  # 断言【确认】按钮状态
            cancel_button = doc_policy_page(driver).el_cancel_button
            cancel_button_status = driver.find_element_by_xpath(cancel_button).get_attribute("class")
            assert cancel_button_status.split("-")[-1] != "disabled"  # 断言【取消】按钮状态
            driver.find_element_by_xpath(cancel_button).click()  # 点击【取消】按钮
            Domain_mgnt_home_page(driver).return_domain_home_page()  # 进入文档域管理
        # except Exception:
        #
        #     Domain_mgnt_home_page(driver).close_windows()
        #     raise

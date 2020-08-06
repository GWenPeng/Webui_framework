# coding=utf-8
from AS7.Pages.Domain_mgnt.domain_mgnt_home_page import Domain_mgnt_home_page
from AS7.Pages.Domain_mgnt.domain_mgnt_page import Domain_mgnt_page
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



class Test_AddDomainInterfaceCheck:

    @allure.testcase("caseid:5352,文档域管理--添加文档域--页面检查")
    @pytest.mark.normal
    @pytest.mark.jt_suite
    def test_add_domain_interface_check(self, driver):
        # try:
            Domain_mgnt_home_page(driver).return_domain_home_page()  # 进入文档域管理
            add_domain_button = Domain_mgnt_page(driver).el_add_domain
            add_domain_button_status = driver.find_element_by_css_selector(add_domain_button).get_attribute("class")
            assert add_domain_button_status.split("-")[-1] != "disabled"  # 断言添加文档域按钮状态
            driver.find_element_by_css_selector(add_domain_button).click()  # 点击添加文档域按钮
            add_domain_interface_title = Domain_mgnt_page(driver).el_add_domain_title
            WebDriverWait(driver, 60).until(ec.visibility_of_element_located((
               By.XPATH, add_domain_interface_title)))  # 等待添加文档域弹窗出现
            child_domain_selectbox = Domain_mgnt_page(driver).el_child_domain_selectbox
            childdomain_selectbox_status = driver.find_element_by_xpath(child_domain_selectbox).get_attribute("class")
            assert childdomain_selectbox_status.split("-")[-1] == "checked"  # 断言子域默认被勾选
            parallel_domain_selectbox = Domain_mgnt_page(driver).el_parallel_domain_selectbox
            leveldomain_selectbox_status = driver.find_element_by_xpath(parallel_domain_selectbox).get_attribute("class")
            assert leveldomain_selectbox_status.split("-")[-1] != "disabled"  # 断言平级域单选框状态
            domain_name_required = Domain_mgnt_page(driver).el_domain_name_required
            WebDriverWait(driver, 60).until(ec.visibility_of(driver.find_element_by_xpath(domain_name_required)))  # 断言域名为必填项
            domain_name = Domain_mgnt_page(driver).el_domain_name_input
            domain_name_value = driver.find_element_by_css_selector(domain_name).get_attribute("value")
            assert domain_name_value == ""  # 断言域名值默认为空
            port_required = Domain_mgnt_page(driver).el_port_required
            WebDriverWait(driver, 60).until(ec.visibility_of(driver.find_element_by_xpath(port_required)))  # 断言端口为必填项
            port_input = Domain_mgnt_page(driver).el_port_input
            port_value = driver.find_element_by_css_selector(port_input).get_attribute("value")
            assert port_value == "443"  # 断言端口默认值
            appid_required = Domain_mgnt_page(driver).el_appid_required
            WebDriverWait(driver, 60).until(ec.visibility_of(driver.find_element_by_xpath(appid_required)))  # 断言APPID为必填项
            appid_input = Domain_mgnt_page(driver).el_appid_input
            appid_value = driver.find_element_by_css_selector(appid_input).get_attribute("value")
            assert appid_value == ""  # 断言APPID默认值为空
            appkey_required = Domain_mgnt_page(driver).el_appkey_required
            WebDriverWait(driver, 60).until(ec.visibility_of(driver.find_element_by_xpath(appkey_required)))  # 断言APPKEY为必填项
            appkey_input = Domain_mgnt_page(driver).el_appkey_input
            appkey_value = driver.find_element_by_css_selector(appkey_input).get_attribute("value")
            assert appkey_value == ""  # 断言APPKEY默认值为空
            confirm_button = Domain_mgnt_page(driver).el_confirm
            confirm_button_status = driver.find_element_by_css_selector(confirm_button).get_attribute("class")
            assert confirm_button_status.split("-")[-1] != "disabled"  # 断言【确认】按钮状态
            cancel_button = Domain_mgnt_page(driver).el_cancel
            cancel_button_status = driver.find_element_by_css_selector(cancel_button).get_attribute("class")
            assert cancel_button_status.split("-")[-1] != "disabled"  # 断言【取消】按钮状态
            driver.find_element_by_css_selector(cancel_button).click()  # 点击【取消】按钮
            Domain_mgnt_home_page(driver).return_domain_home_page()  # 进入文档域管理
        # except Exception:
        #
        #     Domain_mgnt_home_page(driver).close_windows()
        #     raise


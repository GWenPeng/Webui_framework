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


class TestPolicyRankPageTurn:

    @pytest.fixture(scope="function")
    def clear_data(self, request):
        yield
        host = request.config.getoption(name="--host")
        host = host.split('//')[1].split(':')[0]
        db = DB_connect(host=host)

        delete_sql = "delete from domain_mgnt.t_relationship_domain where f_domain_type = 'child'"
        db.delete(delete_sql)  # 删除子域

    @allure.testcase("caseid:5416,文档域管理--列表排序和翻页")
    @pytest.mark.high
    @pytest.mark.jt_suite
    def test_rank_pageturn(self, driver, request, clear_data):
        # try:
        host = request.config.getoption(name="--host")
        host = host.split('//')[1].split(':')[0]
        db = DB_connect(host=host)

        for i in range(1, 12):
            sql = "insert into domain_mgnt.t_relationship_domain values" \
                  "('{}','{}',443,'','','child','','admin1','eisoo.com',now())"
            domain_id = "9b04d18d-6c15-45a6-8c8c-6b8dc67" + str(i)
            domain = "11.22.33." + str(i)
            domain_sql = sql.format(domain_id, domain)
            db.insert(domain_sql)

        for i in range(1):
            sql = "insert into domain_mgnt.t_relationship_domain values" \
                  "('{}','{}',443,'','','child','','admin','eisoo.com',now())"
            domain_id = "9b04d18d-6c15-45a6-8c8c-6b8dc68" + str(i)
            domain = "a_domain.com" + str(i)
            domain_sql = sql.format(domain_id, domain)
            db.insert(domain_sql)

        for i in range(1):
            sql = "insert into domain_mgnt.t_relationship_domain values" \
                  "('{}','{}',443,'','','child','','admin','eisoo.com',now())"
            domain_id = "9b04d18d-6c15-45a6-8c8c-6b8dc69" + str(i)
            domain = "z_domain.com" + str(i)
            domain_sql = sql.format(domain_id, domain)
            db.insert(domain_sql)

        for i in range(8):
            sql = "insert into domain_mgnt.t_relationship_domain values" \
                  "('{}','{}',443,'','','child','','admin','eisoo.com',now())"
            domain_id = "9b04d18d-6c15-45a6-8c8c-6b8dc60" + str(i)
            domain = "AA_domain.com" + str(i)
            domain_sql = sql.format(domain_id, domain)
            db.insert(domain_sql)

        for i in range(8):
            sql = "insert into domain_mgnt.t_relationship_domain values" \
                  "('{}','{}',443,'','','child','','admin','eisoo.com',now())"
            domain_id = "9b04d18d-6c15-45a6-8c8c-6b8dc61" + str(i)
            domain = "ZZ_domain.com" + str(i)
            domain_sql = sql.format(domain_id, domain)
            db.insert(domain_sql)  # 数据库添加子域

        Domain_mgnt_home_page(driver).return_domain_home_page()  # 进入文档域管理
        driver.refresh()
        time.sleep(5)
        line1_domain_name_value = Domain_mgnt_page(driver).get_domain_name_by_index(1, 1)
        assert line1_domain_name_value == "11.22.33.1"  # 断言列表第1行为IP地址：11.22.33.1
        line2_domain_name_value = Domain_mgnt_page(driver).get_domain_name_by_index(2, 1)
        assert line2_domain_name_value == "11.22.33.10"  # 断言列表第2行为IP地址：11.22.33.10
        line3_domain_name_value = Domain_mgnt_page(driver).get_domain_name_by_index(3, 1)
        assert line3_domain_name_value == "11.22.33.11"  # 断言列表第3行为IP地址：11.22.33.11
        line12_domain_name_value = Domain_mgnt_page(driver).get_domain_name_by_index(12, 1)
        assert line12_domain_name_value == "a_domain.com0"  # 断言列表第12行为域名：a_domain.com0
        line13_domain_name_value = Domain_mgnt_page(driver).get_domain_name_by_index(13, 1)
        assert line13_domain_name_value == "AA_domain.com0"  # 断言列表第13行为域名：AA_domain.com0
        max_line_page = Domain_mgnt_page(driver).el_max_line_page
        max_line_page_text = driver.find_element_by_xpath(max_line_page).text
        number = max_line_page_text.count("20")
        assert number == 1  # 断言每页最多显示20条
        next_page = Domain_mgnt_page(driver).el_next_page
        driver.find_element_by_xpath(next_page).click()  # 翻至第二页
        time.sleep(3)
        p2line1_domain_name_value = Domain_mgnt_page(driver).get_domain_name_by_index(1, 1)
        assert p2line1_domain_name_value == "z_domain.com0"  # 断言列表第2页第1行为域名：z_domain.com0
        p2line2_domain_name_value = Domain_mgnt_page(driver).get_domain_name_by_index(2, 1)
        assert p2line2_domain_name_value == "ZZ_domain.com0"  # 断言列表第2页第2行为域名：ZZ_domain.com0
        page_input = Domain_mgnt_page(driver).el_page_input
        Domain_mgnt_page(driver).clear_input(driver.find_element_by_xpath(page_input))  # 清空页码输入框
        driver.find_element_by_xpath(page_input).send_keys("1")
        time.sleep(3)
        page_input_value = driver.find_element_by_xpath(page_input).get_attribute("value")
        assert page_input_value == "1"  # 跳转至输入的有效页码
        page_input = Domain_mgnt_page(driver).el_page_input
        Domain_mgnt_page(driver).clear_input(driver.find_element_by_xpath(page_input))  # 清空页码输入框
        driver.find_element_by_xpath(page_input).send_keys("3")
        page_input_value2 = driver.find_element_by_xpath(page_input).get_attribute("value")
        assert page_input_value2 == ""  # 无法输入超过当前实际页码数
        delete_sql = "delete from domain_mgnt.t_relationship_domain where f_app_id = 'admin1'"
        db.delete(delete_sql)  # 删除部分子域
        Domain_mgnt_home_page(driver).return_domain_home_page()  # 进入文档域管理
        driver.refresh()
        time.sleep(5)
        first_page = Domain_mgnt_page(driver).el_first_page
        # first_page_button = driver.find_element_by_xpath(first_page).get_attribute("class")
        is_true = driver.find_element_by_xpath(first_page).get_attribute("disabled")
        assert is_true == "true"  # 断言首页按钮灰化
        # assert first_page_button.split("-")[-1] == "disabled"  # 断言首页按钮灰化
        last_page = Domain_mgnt_page(driver).el_last_page
        # last_page_button = driver.find_element_by_xpath(last_page).get_attribute("class")
        is_true = driver.find_element_by_xpath(last_page).get_attribute("disabled")
        assert is_true == "true"  # 断言上一页按钮灰化
        # assert last_page_button.split("-")[-1] == "disabled"  # 断言上一页按钮灰化
        next_page = Domain_mgnt_page(driver).el_next_page
        # next_page_button = driver.find_element_by_xpath(next_page).get_attribute("class")
        is_true = driver.find_element_by_xpath(next_page).get_attribute("disabled")
        assert is_true == "true"  # 断言下一页按钮灰化
        # assert next_page_button.split("-")[-1] == "disabled"  # 断言下一页按钮灰化
        end_page = Domain_mgnt_page(driver).el_end_page
        # end_page_button = driver.find_element_by_xpath(end_page).get_attribute("class")
        is_true = driver.find_element_by_xpath(end_page).get_attribute("disabled")
        assert is_true == "true"   # 断言尾页按钮灰化
        # assert end_page_button.split("-")[-1] == "disabled"  # 断言尾页按钮灰化
        delete_sql = "delete from domain_mgnt.t_relationship_domain where f_app_id = 'admin'"
        db.delete(delete_sql)  # 删除子域
    # except Exception:
    #
    #     Domain_mgnt_home_page(driver).close_windows()
    #     raise

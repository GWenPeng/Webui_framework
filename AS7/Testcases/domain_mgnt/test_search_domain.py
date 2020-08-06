from selenium.webdriver.common.by import By
from AS7.Pages.Domain_mgnt.domain_mgnt_home_page import Domain_mgnt_home_page
from AS7.Pages.Domain_mgnt.domain_mgnt_page import Domain_mgnt_page
from AS7.Pages.Domain_mgnt.CommonDocDomain import CommonDocDomain
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure
import pytest


class TestSearchDoamin:

    @allure.step("添加133个平级域")
    @pytest.fixture(scope="function")
    def add_parallel_domain(self, request):
        host = request.config.getoption(name="--host")
        host = host.split('//')[1].split(':')[0]
        uuids = []
        hosts = []
        for i in range(1, 134):
            randomIP = "186." + "186." + str(i)
            if randomIP != host:
                hosts.append(randomIP)
        uuids = CommonDocDomain().addRelationDomain(httphost=host, domaintype="parallel", host=hosts,
                                                           network_type="indirect")
        yield
        for uuid in uuids:
            CommonDocDomain().delRelationDomain(host=host, uuid=uuid)

    @allure.testcase("5449 文档域管理--搜索")
    @pytest.mark.high
    @pytest.mark.gfr
    def test_search_domain_success(self,driver,add_parallel_domain):
        Domain_mgnt_home_page(driver).return_domain_home_page()
        domain_mgnt = Domain_mgnt_page(driver)
        search_input = driver.find_element_by_xpath(domain_mgnt.el_search_input)
        search_input.send_keys("3")
        assert domain_mgnt.get_domain_list_count() == 20
        driver.find_element_by_xpath(domain_mgnt.el_next_page_icon).click()
        assert domain_mgnt.get_domain_list_count() == 6
        WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.XPATH,domain_mgnt.el_search_delete)))
        driver.find_element_by_xpath(domain_mgnt.el_search_delete).click()
        assert search_input.get_attribute("value") == ""
        assert driver.find_element_by_xpath(domain_mgnt.el_page_input).get_attribute("value") == "1"
        search_input.send_keys("333")
        WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH,domain_mgnt.el_result_null)))
        domain_mgnt.clear_input(search_input)
        assert search_input.get_attribute("value") == ""
        assert domain_mgnt.get_domain_list_count() == 20












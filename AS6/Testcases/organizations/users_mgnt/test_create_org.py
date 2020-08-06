from AS6.Pages.Organizations.users_mgnt.users_org_mgnt_page import department_mgnt_moudle
from AS6.Pages.Organizations.users_mgnt.users_org_mgnt_page import user_org_mgnt_page
import time
import pytest


@pytest.mark.skip
def test_create_org(driver):
    department_mgnt_moudle(driver).new_create_org(org_name="小部门", email="1221414321@qq.com", owner_site="sss")
    department_mgnt_moudle(driver).new_create_department(department_name="小布梦", email="2214143212@qq.com",
                                                         owner_site="sss")
    time.sleep(5)

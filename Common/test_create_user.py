from AS6.Pages.Organizations.users_mgnt.users_org_mgnt_page import user_mgnt_module
from AS6.Pages.Organizations.users_mgnt.users_org_mgnt_page import user_org_mgnt_page
from Common.parse_data import do_excel
from Common.screenshot import ScreenShot
from Common.mysqlconnect import DB_connect
from Common.thrift_client import Thrift_client
from ShareMgnt import ncTShareMgnt
import pytest
import allure


@pytest.mark.skip
class Test_create_user:

    @pytest.fixture(scope='function')
    def clean_user_info(self, driver):
        yield
        user_mgnt_module(driver).del_user()
        # db = DB_connect(dbname="db_93")  # 连接数据库
        # db.delete("DELETE from sharemgnt_db.t_user where f_display_name='aaa';")  # SQL删除用户

        # tc = Thrift_client(service=ncTShareMgnt)  # 调用thrift接口删除用户
        # tc.client.Usrm_DelUser(userId="9803e4f2-3377-11ea-9a77-005056822f8e")  # 调用thrift接口删除用户

    @allure.testcase("caseid:23231")
    @pytest.mark.high
    # @screenshot(driver)  # 自动异常截图
    def test_create_user_success(self, driver, clean_user_info):
        # try:
            data = \
                do_excel(filename="creat_user.xlsx", sheetname="创建用户", minrow=2, maxrow=2,
                         mincol=1,
                         maxcol=11)[
                    0]  # 读取excle 数据
            user_mgnt_module(driver).create_user(username=data[0], showname=data[1], remark=data[2], mobile=data[4],
                                                 quota_space=data[9])
            # user_mgnt_moudle(driver).del_user()
            el_display_name = driver.find_element_by_css_selector(user_org_mgnt_page(driver).el_display_name)
            print(el_display_name.text)
            assert el_display_name.text == data[10]
        # except Exception:
        #
        #     raise

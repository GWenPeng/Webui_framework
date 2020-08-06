# coding=utf-8
from AS7.Pages.Login_page import Login_page
from Common.readConfig import readconfigs
from selenium import webdriver
from selenium.common.exceptions import SessionNotCreatedException
from Common.readdrivers import Read_drivers
from Common.mysqlconnect import DB_connect
from Common.ssh_client import SSHClient
from Common.property import Properties
from Common.http_request import Http_client
import pytest
from Common.screenshot import ScreenShot
from AS7.Pages.Domain_mgnt.domain_mgnt_home_page import Domain_mgnt_home_page


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport():
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" or report.when == "setup" or report.when == "teardown":
        if report.outcome == "failed":
            scs = ScreenShot(driver)
            scs(report.nodeid.split("::")[-1] + "执行阶段：" + report.when)
            Domain_mgnt_home_page(driver).close_windows()


@pytest.fixture(scope='session', autouse=False)
def setUpClass(request):
    host = request.config.getoption("--host")
    close_firewall(host=host)
    host = host.split('//')[1].split(':')[0]
    db = DB_connect(host=host)  # 连接数据库
    del_person = 'delete from t_person_group'
    del_user = 'delete from t_user where f_login_name not in(\'system\',\'admin\',\'security\',\'audit\')'
    del_department = 'delete from t_department where f_name <> (\'组织结构\')'
    del_relation = 'delete from t_department_relation'
    del_userRelation = 'delete from t_user_department_relation'
    db.delete(del_person)  # 删除组织，部门，用户等数据
    db.delete(del_user)
    db.delete(del_department)
    db.delete(del_relation)
    db.delete(del_userRelation)
    db.close()  # 关闭连接


@pytest.fixture(scope="session", autouse=False)
def clearEnv(request):
    # 更新域身份为平级域
    update_domain_parallel = "UPDATE domain_mgnt.t_domain_self SET domain_mgnt.t_domain_self.f_type = 'parallel', " \
                             "domain_mgnt.t_domain_self.f_parent_host = null"
    # 清空绑定/策略/子域表单
    delete_table1 = "DELETE FROM domain_mgnt.t_library_sync_plan"
    delete_table2 = "DELETE FROM domain_mgnt.t_policy_tpl_domains"
    delete_table3 = "DELETE FROM domain_mgnt.t_policy_tpls"
    delete_table4 = "DELETE FROM domain_mgnt.t_relationship_domain"
    self_host = request.config.getoption("--host")
    self_host = self_host.split("//")[1].split(":")[0]  # 本域IP
    self_db = DB_connect(host=self_host)
    self_db.update(update_domain_parallel)
    self_db.delete(delete_table1)
    self_db.delete(delete_table2)
    self_db.delete(delete_table3)
    self_db.delete(delete_table4)
    self_db.close()

    def env(section, tagnema):
        rc = readconfigs(configName="ui_config.ini")
        section_env = rc.get_items(section=section)
        for key in section_env:
            host = section_env[key]
            db = DB_connect(host=host)
            db.update(update_domain_parallel)
            db.delete(delete_table1)
            db.delete(delete_table2)
            db.delete(delete_table3)
            db.delete(delete_table4)
            db.close()
        # 调用添加子域接,构造父子域
        post_client = Http_client(tagname=tagnema)
        jsondata = {"host": section_env["child_domain"], "port": 443, "type": "child", "app_id": "admin",
                    "app_key": "eisoo"}
        post_client.post(url="/api/document-domain-management/v1/domain",
                         header='{"Content-Type":"application/json"}',
                         jsondata=jsondata)

    browserName = request.config.getoption(name="--browsername")
    print(browserName)
    if browserName == "Chrome":
        env(section="chrome_domain", tagnema="HTTPChrome")
    elif browserName == "Ie":
        env(section="Ie_domain", tagnema="HTTPIe")
    elif browserName == "Firefox":
        env(section="firefox_domain", tagnema="HTTPIe")
    elif browserName == "Edge":
        env(section="edge_domain", tagnema="HTTPChrome")
    elif browserName == "Safari":
        env(section="safari_domain", tagnema="HTTPIe")
    else:
        pass


@pytest.fixture(scope='session', autouse=True)
def get_domain(request):
    browserName = request.config.getoption(name="--browsername")
    rc = readconfigs(configName="ui_config.ini")
    if browserName == "Chrome":
        return rc.get_items(section="chrome_domain")
    elif browserName == "Firefox":
        return rc.get_items(section="firefox_domain")
    elif browserName == "Safari":
        return rc.get_items(section="safari_domain")
    elif browserName == "Ie":
        return rc.get_items(section="Ie_domain")
    elif browserName == "Edge":
        return rc.get_items(section="edge_domain")
    else:
        return rc.get_items(section="default_domain")


@pytest.fixture(scope='session', autouse=True)
def driver(request):
    """
    "browserName": "MicrosoftEdge"
    "browserName": "internet explorer"
    "browserName": "chrome"
    "browserName": "firefox"
    """
    global driver
    browserName = request.config.getoption(name="--browsername")
    try:
        if browserName == "Edge":
            driver = webdriver.Edge()
        elif browserName == "Ie":
            # print("----------------------")
            # print("正在打开浏览器")
            # with open(file="C:\\logs.txt",mode="a") as  file:
            #     file.write("driver 正在打开浏览器\n")
            try:
                # driver = webdriver.Ie(log_level="WARN", service_log_path="C:\\logs.log", port=5555, keep_alive=True)
                driver = webdriver.Ie()
                # driver = webdriver.Remote(command_executor="http://10.2.181.4:4444/wd/hub",
                #                           desired_capabilities={'browserName': "internet explorer"})
            except Exception:
                # with open(file="C:\\logs.txt", mode="a") as  file:
                #     file.write("driver 创建失败\n")
                # print("driver 创建失败")
                raise
            # with open(file="C:\\logs.txt", mode="a") as  file:
            #     file.write("driver 创建成功\n")
            #     print(driver)

            # print(".....................")
        elif browserName == "Chrome":
            driver = webdriver.Chrome()
        elif browserName == "Firefox":
            driver = webdriver.Firefox()
        elif browserName == "Safari":
            # print(Read_drivers().get_driver_path("safari"))
            # driver = webdriver.Safari()
            driver = webdriver.Remote(command_executor="http://10.2.180.223:15001/wd/hub",
                                      desired_capabilities={'browserName': "safari"})
        else:
            driver = webdriver.Chrome()
    except SessionNotCreatedException as e:
        print("浏览器启动异常,请检查对应驱动版本!")
        raise e
    # driver = webdriver.Ie(Read_drivers().get_driver_path("IE32"))  # 调用本地IE32位driver
    # driver = webdriver.Chrome(Read_drivers().get_driver_path("chrome"))  # 调用本地chrome
    # driver = webdriver.Edge("C:\drivers\MicrosoftWebDriver.exe", port=17556)
    # driver=webdriver.Firefox()
    # driver = webdriver.Remote(command_executor="http://10.2.180.223:15001/wd/hub",
    #                           desired_capabilities={
    #                               'browserName': request.config.getoption(name="--browsername")})  # 调用hub节点的driver

    try:
        # driver.implicitly_wait(30)

        # dirver.set_page_load_timeout(15)
        driver.maximize_window()
        driver.get(request.config.getoption(name="--host"))
        prop = Properties("environment.properties")
        prop.put('host', request.config.getoption(name="--host"))
        driver.set_page_load_timeout(10)
    except Exception as e:
        print(e)
        driver.quit()
    return driver


@pytest.fixture(scope='session', autouse=True)
def setup(driver, request):
    try:
        host = request.config.getoption(name="--host")
        close_firewall(host)  # 关闭防火墙
        set_csf_level_enum(host)  # 设置密级
        redcof = readconfigs(configName="ui_config.ini")
        username = redcof.get_user_info(option_name="username")
        password = redcof.get_user_info(option_name="password")
        Login_page(driver).login(username=username, password=password)
        # user_org_mgnt_page(driver).is_close_setup_conf()
    except Exception:
        driver.quit()
        raise
    yield
    driver.quit()


def pytest_addoption(parser):
    parser.addoption('--browsername', action="store", default="Chrome",
                     help='my option:"Ie,Edge,Chrome,Firefox,Safari')
    parser.addoption('--host', action='store', default='https://10.2.182.10:8000', help='ex:https://10.2.182.10:8000')


def set_csf_level_enum(host):
    host = host.split('//')[1].split(':')[0]
    DB_connect(host=host).update("UPDATE sharemgnt_db.t_sharemgnt_config set "
                                 "f_value='{\"内部\": 6, \"机密\": 8, \"非密\": 5, "
                                 "\"秘密\": 7}' where f_key='csf_level_enum';")


def close_firewall(host):  # 关闭防火墙
    host = host.split('//')[1].split(':')[0]
    # print(host)
    # tc = Thrift_client(service=ncTECMSManager, host=host, port=9201)
    # tc.client.disable_firewall()
    # tc.close()
    sh = SSHClient(host=host)
    sh.command("firewall-cmd --zone=public --add-port=9600/tcp;firewall-cmd --zone=public "
               "--add-port=3320/tcp;firewall-cmd --zone=public --add-port=9121/tcp;firewall-cmd --zone=public "
               "--add-port=9080/tcp;firewall-cmd --zone=public --add-port=8081/tcp;firewall-cmd --zone=public "
               "--add-port=1/tcp;firewall-cmd --zone=public --add-port=65535/tcp;")
    sh.ssh_close()


# @pytest.fixture
# def get_browser(request):
#     return request.config.getoption("--browsername")

if __name__ == '__main__':
    # set_csf_level_enum(host="http://10.2.180.93:8000")
    # close_firewall(host="http://10.2.180.93:8000")
    clearEnv("https://10.2.180.129:8000")

from AS6.Pages.Login_page import Login_page
from Common.readConfig import readconfigs
from selenium import webdriver
from Common.readdrivers import Read_drivers
from Common.mysqlconnect import DB_connect
from Common.ssh_client import SSHClient
from Common.property import Properties
import pytest


@pytest.fixture(scope='session', autouse=True)
def driver(request):
    """
    "browserName": "MicrosoftEdge"
    "browserName": "internet explorer"
    "browserName": "chrome"
    "browserName": "firefox"
    """

    # driver = webdriver.Ie(Read_drivers().get_driver_path("IE32"))  # 调用本地IE32位driver
    # driver = webdriver.Chrome(Read_drivers().get_driver_path("chrome"))  # 调用本地chrome
    driver=webdriver.Edge("C:\drivers\MicrosoftWebDriver.exe",port=17556)
    # driver=webdriver.Firefox()
    # driver = webdriver.Remote(command_executor="http://10.2.180.223:15001/wd/hub",
    #                           desired_capabilities={
    #                               'browserName': request.config.getoption(name="--browsername")})  # 调用hub节点的driver

    try:
        driver.implicitly_wait(30)

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
    host = request.config.getoption(name="--host")
    close_firewall(host)  # 关闭防火墙
    set_csf_level_enum(host)  # 设置密级
    redcof = readconfigs(configName="ui_config.ini")
    username = redcof.get_user_info(option_name="username")
    password = redcof.get_user_info(option_name="password")
    Login_page(driver).login(username=username, password=password)
    # user_org_mgnt_page(driver).is_close_setup_conf()
    yield
    driver.quit()


def pytest_addoption(parser):
    parser.addoption('--browsername', action="store", default="MicrosoftEdge", help='my option:"MicrosoftEdge" or "internet '
                                                                             'explorer" or "chrome" or "firefox"')
    parser.addoption('--host', action='store', default='http://10.2.180.93:8000', help='ex:http://10.2.180.93:8000')


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
    sh.command("cd /sysvol/apphome/app/ThriftAPI/gen-py-tmp/ECMSManager;./ncTECMSManager-remote -h "
               "127.0.0.1:9201 disable_firewall")
    sh.ssh_close()


# @pytest.fixture
# def get_browser(request):
#     return request.config.getoption("--browsername")

if __name__ == '__main__':
    # set_csf_level_enum(host="http://10.2.180.93:8000")
    close_firewall(host="http://10.2.180.93:8000")

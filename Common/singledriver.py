# coding=utf-8
from selenium import webdriver
from Common.readdrivers import Read_drivers
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class SingleDriver:
    """
    单例模式，统一管理浏览器的实例
    """

    __instance = None

    def __new__(cls, *args, **kwargs):
        """
        new 对象会调用
        """
        if cls.__instance is None:
            # cls.__instance = webdriver.Chrome(Read_drivers().get_driver_path("chrome"))  #调用本地driver
            cls.__instance = webdriver.Remote(command_executor="http://10.2.180.223:15000/wd/hub",
                                              desired_capabilities={'browserName': 'Edge'})
        # cls.__instance.implicitly_wait(20)

        # cls.__instance.set_page_load_timeout(15)
        cls.__instance.maximize_window()
        return cls.__instance


if __name__ == '__main__':
    dr1 = SingleDriver()
    dr2 = SingleDriver()

    print(dr1 == dr2, dr1, dr2)

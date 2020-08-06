import os


class Read_drivers:
    def __init__(self):
        # 获取当前路径
        # current_path = os.path.dirname(os.path.abspath(__file__))
        # 获取当前文件夹的父级路径第一种办法
        # father_path = os.path.abspath(current_path+os.path.sep+"..")
        # 获取当前文件夹的父级路径第二种办法
        self.father_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # self.conf = configparser.ConfigParser()
        # # 读取config.ini文件参数信息
        # self.conf.read(dirpath, encoding="utf-8")
        # self.conf.has_section()

    def get_driver_path(self, driver_name):
        if driver_name == "safari":
            driver_path = os.path.join(self.father_path, "Drivers/" + driver_name + "driver")
        else:
            driver_path = os.path.join(self.father_path, "Drivers/" + driver_name + "driver.exe")
        return driver_path


if __name__ == '__main__':
    print(Read_drivers().get_driver_path(driver_name="safari"))

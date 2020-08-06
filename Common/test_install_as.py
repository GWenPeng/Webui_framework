# coding=utf-8
from Common.ftp_download import MyFtp
from Common.ssh_client import sftp_upload
from Common.ssh_client import SSHClient
import threading
import time
import pytest


def replace_package(host="10.2.180.157"):
    try:
        sh = SSHClient(host=host)
        code = sh.command("cd /root;ls")
        if "ReplacePackage" not in str(code):
            sh.command("scp -r root@10.2.176.245:/root/ReplacePackage /root;driver")
    except Exception:
        raise


def cul_ftp_downloadFile(host=None, remotepath="ftp://asftp.eisoo.com/FTP", filename=None):
    # try:
    sh = SSHClient(host=host)
    res = sh.command("curl -O " + remotepath + filename)
    print(res)
    # code = sh.command("cd /root;ls")
    # if "ReplacePackage" not in str(code):
    #     sh.command("scp -r root@10.2.176.245:/root/ReplacePackage /root;driver")


def test_install_as_web(remotepath='ftp://asftp.eisoo.com/FTP/Server/Feature-ASP-380/',
                        hostlist=["10.2.180.93"],
                        filename="AnyShare-Server-7.0.0-20200619-el7.x86_64-1086.tar.gz",
                        replace_path="/root/ReplacePackage/as_7.0/replace_package.sh"):
    """

    :param remotepath: ftp下载路径
    :param hostlist: 要安装的服务器host列表
    :param filename: 下载的大包名称
    :param replace_path: 替包脚本路径
    :return:
    """
    time1 = time.time()
    if hostlist is None:
        hostlist = ["10.2.180.210", "10.2.180.211", "10.2.180.218", "10.2.181.21", "10.2.181.22",
                    "10.2.181.23", "10.2.181.24", "10.2.181.25"]

    startime = time.time()
    print('这是主线程:正在执行下载安装包', threading.current_thread().name)
    t1_list = []
    for host in hostlist:
        t1 = threading.Thread(target=cul_ftp_downloadFile, args=(host, remotepath, filename))
        t1_list.append(t1)
    for t1 in t1_list:
        t1.setDaemon(True)
        t1.start()
    for t1 in t1_list:
        t1.join()
    print('下载安装包完成耗时:', time.time() - startime)
    startime1 = time.time()
    print('这是主线程:正在执行替包脚本', threading.current_thread().name)
    t2_list = []
    for host in hostlist:
        T = threading.Thread(target=SSHClient(host=host).command,
                             args=("sh " + replace_path + " %s%s" % ("/root/", filename),))
        t2_list.append(T)
    for t2 in t2_list:
        t2.setDaemon(True)
        t2.start()
    for t2 in t2_list:
        t2.join()
    print("替包完成用时:", time.time() - startime1)
    print("所有任务执行完成总共用时:", time.time() - time1)


def test_install_as_service(domian_tag="MISSION-23", policy_tage="MISSION-25",
                            hostlist=["10.2.150.245"]):
    if hostlist is None:
        hostlist = ["10.2.180.210", "10.2.180.211", "10.2.180.218", "10.2.181.21", "10.2.181.22",
                    "10.2.181.23", "10.2.181.24", "10.2.181.25"]
    tim = time.time()
    t_list = []
    for host in hostlist:
        T = threading.Thread(target=SSHClient(host=host).command,
                             args=("cd /sysvol/apphome/app/ThriftAPI/gen-py-tmp/Deploy/;./ncTDeployManager-remote -h "
                                   "localhost:9700 deploy_delete_chart domain-mgnt;./ncTDeployManager-remote -h "
                                   "localhost:9700 deploy_delete_chart policy-mgnt;./ncTDeployManager-remote -h "
                                   "localhost:9700 deploy_install_chart domain-mgnt;./ncTDeployManager-remote -h "
                                   "localhost:9700 deploy_install_chart  policy-mgnt;sleep 5s;helm upgrade "
                                   "domain-mgnt --reuse-values --set api.protocol=https,api.port=443,image.tag=%s"
                                   " helm_repos/domain-mgnt;helm upgrade policy-mgnt --reuse-values "
                                   "--set api.protocol=https,api.port=443,image.tag=%s "
                                   "helm_repos/policy-mgnt;sleep 10s;kubectl get pods | grep Running | awk '{print "
                                   "$1}' | xargs kubectl delete pod" % (domian_tag, policy_tage),))
        t_list.append(T)
    for t in t_list:
        t.setDaemon(True)
        t.start()
    for t in t_list:
        t.join()

    print("service 安装完成总共用时", time.time() - tim)

    # for host in hostlist:
    #     T = threading.Thread(target=SSHClient(host=host).command,
    #                          args=("helm upgrade "
    #                                "domain-mgnt --reuse-values --set api.protocol=https,api.port=443,image.tag=%s"
    #                                " helm_repos/domain-mgnt;helm upgrade policy-mgnt --reuse-values "
    #                                "--set api.protocol=https,api.port=443,image.tag=%s "
    #                                "helm_repos/policy-mgnt;sleep 10s;kubectl get pods | grep Running | awk '{print "
    #                                "$1}' | xargs kubectl delete pod" % (domian_tag, policy_tage),))
    #     T.start()
    #     print("service 安装完成")

#
# if __name__ == '__main__':
#     replace_package()

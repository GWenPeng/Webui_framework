# coding= utf-8
import paramiko
from Common.readConfig import readconfigs
from paramiko import AuthenticationException


def sftp_upload(hostname, filename, srcpath, destpath, port=22):
    transport = paramiko.Transport((hostname, port))
    transport.connect(username="root", password="driver")
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.put(srcpath+filename, destpath+filename)
    sftp.close()


class SSHClient:
    def __init__(self, ssh_name="SSHClient", host=None):
        self.host = None
        rc = readconfigs()
        if host is None:
            self.Host = rc.get_sshclient(ssh_name=ssh_name, name="host")
        else:
            self.Host = host
        self.Port = rc.get_sshclient(ssh_name=ssh_name, name="port")
        self.User = rc.get_sshclient(ssh_name=ssh_name, name="user")
        self.Password = rc.get_sshclient(ssh_name=ssh_name, name="password")
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.ssh.connect(self.Host, self.Port, self.User, self.Password)
        except AuthenticationException:
            print("user or password error !")

    def command(self, *args):
        print(args)
        stdin, stdout, stderr = self.ssh.exec_command(*args)
        res, err = stdout.read(), stderr.read()
        result = res if res else err
        return result

    def ssh_close(self):
        self.ssh.close()

    # return ssh_client
    # ssh.exec_command("pwd")
    # ssh.exec_command("mkdir guwenpeng")

    # ssh.exec_command("cd guwenpeng")
    # stdin,stdout,stderr = ssh.exec_command("pwd")
    # 上边的代码输出应该是 /root\n，但结果却是 /root ，即使用root登陆的缺省目录
    # 原因是exec_command为单个会话，执行完成之后会回到登录时的缺省目录
    # 修改为这样执行结果则为预期的 /root/guwenpeng 目录
    # stdin, stdout, stderr = ssh.exec_command("cd guwenpeng;pwd")
    #
    # print(stdout.read())

    # ssh.close()


if __name__ == '__main__':
    # sh = SSHClient()
    # 删除对应的服务容器及镜像
    # sh.exec_command("cd /root/docker;docker-compose -f domain_mgnt.yml down --rmi all;docker-compose -f "
    #                 "domain_mgnt.yml up -d")
    sftp_upload(hostname=["10.2.181.169"],filename="AnyShare-Server-7.0.0-20200415-el7.x86_64-255.tar.gz",srcpath="../Data/",destpath="/root/")

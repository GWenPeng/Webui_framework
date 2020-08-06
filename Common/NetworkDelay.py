from Common.ssh_client import SSHClient

class NETWORKDELAY:
    def __init__(self,host=None,delay_time="1000"):
        self.host=host
        self.delay_time=delay_time

    def delay(self):
        sh = SSHClient(host=self.host)
        delay_command = "tc qdisc add dev ens160 root netem delay %sms"%(self.delay_time)
        sh.command(delay_command)

    def delete_delay(self):
        sh = SSHClient(host=self.host)
        delete_delay = "tc qdisc del dev ens160 root netem delay %sms"%(self.delay_time)
        sh.command(delete_delay)
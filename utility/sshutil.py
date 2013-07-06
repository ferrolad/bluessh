#encoding=utf-8
from fabric.api import env, sudo
from fabric.network import disconnect_all
from baseutil import error_log
from threading import Thread
from time import sleep
from config.models import SSHServer
#from django.contrib import messages
from Queue import Queue


class SSHUtil:
    def __init__(self, User, ssh_user=None, ssh_pwd=None, expired_date=None):
        '''ssh_user,ssh_pwd只有在修改密码、有效期时才用的到
        '''
        self.User = User
        # 储存待执行命令的FIFO队列
        self.q = Queue()

        # 启动后台持续执行的python daemon进程
        t_daemon = Thread(target=self.exec_queue_worker)
        t_daemon.daemon = True
        t_daemon.start()

    # 真正执行工作的函数，每次从队读取一条任务来执行
    # 多条命令同时执行会使fabric混乱
    def exec_queue_worker(self):
        '''每次从队读取一条任务来执行
        '''
        while True:
            item = self.q.get()
            # for test only
            print "after self.q.get"
            print item
            cmd = item['cmd']
            host = item['host']
            admin_pwd = item['admin_pwd']

            ''' run, sudo and the other operations only look in one place when
                connecting: env.host_string. All of the other mechanisms for setting hosts
                are interpreted by the fab tool when it runs,
                and don’t matter when running as a library
            '''
            env.host_string = host
            env.password = admin_pwd
            env.reject_unknown_hosts = False  # default False
            env.disable_known_hosts = True  # default False
            env.timeout = 15  # default 10
            env.connection_attempts = 10  # default 1
            env.skip_bad_hosts = True  # default false
            env.warn_only = True  # default false
            try:
                result = sudo(cmd)
                if result.failed:
                    str_detail = 'host_string=%s\nerror_message=%s\n' % (
                        host, result)
                    error_log("远端SSH命令执行错误：fabric报出的错误", str_detail, self.User)
            except Exception as e:
                #记录异常
                str_detail = 'host_string=%s\nerror_message=%s\n' % (
                    host, e.message)
                error_log("远端SSH命令执行错误：非fabric报出的错误", str_detail, self.User)
                #发送邮件通知管理员
            finally:
                self.q.task_done()

    # 把一条命令入列
    def push_cmd_to_queue(self, cmd, host, admin_pwd):
        item = {'cmd': cmd, 'host': host, 'admin_pwd': admin_pwd}
        self.q.put(item)
        # for test only
        print 'after self.q.put'
        print item

    def ssh_create_worker(self, ssh_info_list):
        '''host是username@addr:prot的形式
        '''
        ssh_servers = SSHServer.objects.filter(is_active=True)
        for item in ssh_info_list:
            # for test only
            print 'after in ssh_info_list'
            print item
            ssh_user, ssh_pwd, expired_date = item
            expired_str = expired_date.strftime("%m/%d/%Y")
            for server in ssh_servers:
                # host是username@addr:prot的形式
                host = "%s@%s:%s" % (server.admin_user, server.address, server.port)
                admin_pwd = server.admin_pwd
                #添加一个没有home目录、在ssh_max2组、带有效期、没有shell登录权限的新帐号
                cmd = "useradd -M -g ssh_max2 -e %s -s /sbin/nologin %s" \
                    % (expired_str, ssh_user)
                self.push_cmd_to_queue(cmd, host, admin_pwd)
                # 修改该帐号的密码
                cmd = "echo '%s:%s'|sudo chpasswd" % (ssh_user, ssh_pwd)
                self.push_cmd_to_queue(cmd, host, admin_pwd)

                # gitfree added 2012-11-10 增加l2tp/ipsec VPN账号自动创建
                expired_line = expired_date.strftime("%Y-%m-%d")
                vpn_str = '%s\t*\t"%s"\t*' % (ssh_user, ssh_pwd)
                cmd = "echo -e '# %s\n%s' >> /etc/ppp/chap-secrets" \
                    % (expired_line, vpn_str)
                self.push_cmd_to_queue(cmd, host, admin_pwd)
                # gitfree added 2012-11-15 暂不重启，可能会影响其他在线用户
                # gitfree added 2013-01-24 可能并不需要重启
                #cmd = "service ipsec restart" #重启ipsec服务
                #self.push_cmd_to_queue(cmd, host, admin_pwd)
        self.q.join()  # wait until q is empty
        sleep(5)
        try:
            disconnect_all()
        except:
            pass

    def ssh_create_onall(self, ssh_info_list):
        '''在所有服务器上创建一个新的SSH用户

            ssh_list -- 待创建的所有ssh帐号信息组成的 list，list的每个成员为形如
                        (ssh_user,ssh_pwd,expired_date)的tuple
        '''
        th = Thread(target=self.ssh_create_worker, args=(ssh_info_list,))
        th.start()

    def ssh_change_pwd_worker(self, ssh_user, ssh_pwd):
        ssh_servers = SSHServer.objects.filter(is_active=True)
        for server in ssh_servers:
            # host是username@addr:prot的形式
            host = "%s@%s:%s" % (server.admin_user, server.address, server.port)
            admin_pwd = server.admin_pwd
            cmd = "echo '%s:%s'|sudo chpasswd" % (ssh_user, ssh_pwd)
            self.push_cmd_to_queue(cmd, host, admin_pwd)
        self.q.join()  # wait until q is empty
        sleep(5)
        try:
            disconnect_all()
        except:
            pass

    def ssh_change_pwd_onall(self, ssh_user, ssh_pwd):
        '''在所有服务器上修改指定SSH用户的密码'''
        th = Thread(target=self.ssh_change_pwd_worker, args=(ssh_user, ssh_pwd))
        th.start()

    def ssh_change_expire_worker(self, ssh_user, expired_str):
        ssh_servers = SSHServer.objects.filter(is_active=True)
        for server in ssh_servers:
            # host是username@addr:prot的形式
            host = "%s@%s:%s" % (server.admin_user, server.address, server.port)
            admin_pwd = server.admin_pwd
            cmd = "usermod -e %s %s" % (expired_str, ssh_user)
            self.push_cmd_to_queue(cmd, host, admin_pwd)
        self.q.join()  # wait until q is empty
        sleep(5)
        try:
            disconnect_all()
        except:
            pass

    def ssh_change_expire_onall(self, ssh_user, expired_date):
        '''在所有服务器上修改指定SSH用户的到期时间
        '''
        # expired_str为 MM/DD/YYYY格式
        expired_str = expired_date.strftime("%m/%d/%Y")

        th = Thread(target=self.ssh_change_expire_worker, args=(ssh_user, expired_str))
        th.start()

    def ssh_delete_worker(self, ssh_user):
        ssh_servers = SSHServer.objects.filter(is_active=True)
        for server in ssh_servers:
            # host是username@addr:prot的形式
            host = "%s@%s:%s" % (
                server.admin_user, server.address, server.port)
            admin_pwd = server.admin_pwd
            cmd = "userdel %s" % ssh_user
            self.push_cmd_to_queue(cmd, host, admin_pwd)
        self.q.join()  # wait until q is empty
        sleep(5)
        try:
            disconnect_all()
        except:
            pass

    def ssh_delete_onall(self, ssh_user):
        '''在所有服务器上删除指定SSH用户'''
        th = Thread(target=self.ssh_delete_worker, args=(ssh_user,))
        th.start()

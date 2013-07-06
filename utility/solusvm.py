#encoding=utf-8
import urllib,urllib2

class SolusVM:
    def __init__(self,master_ip,key,hash):
        url = 'https://%s:5656/api/client' % master_ip
        paras = {}
        paras['key'] = key
        paras['hash'] = hash
        paras['action'] = 'info'
        paras_data = urllib.urlencode(paras)
        result = urllib2.urlopen(url,paras_data)

    def get_status(self):
        print self.result

    def get_mem_info(self):
        pass

    def get_cpu_info(self):
        pass

vm = SolusVM('174.127.96.25','UE02B-CF4HB-48W5W','ea5964a3426e15d7fc97c5946ac155ba0b5d0763')
vm.get_status()

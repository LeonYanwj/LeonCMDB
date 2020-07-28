# import winrm
#
# win2008 = winrm.Session("http://10.20.1.27:5985/wsman",auth=('administrator','abcd1234,'))
# r = win2008.run_ps(r"(New-Object System.Net.WebClient).DownloadFile('http://39.97.104.43:80/download/Salt-Minion-3000.2-Py2-AMD64-Setup.exe','C:\tmpsalt\Salt-Minion-3000.2-Py2-AMD64-Setup.exe')")
# print(r.std_err.decode('utf-8'))
# print(r.std_out.decode('utf-8'))
#
# data = {u'10.20.10.144': {u'ps.virtual_memory': {u'available': 11380510720, u'used': 24919998464, u'cached': 2730442752, u'percent': 66.1, u'free': 8646873088, u'inactive': 214175744, u'active': 24084090880, u'total': 33566871552, u'buffers': 3194880}, u'disk.usage': {u'/dev': {u'available': u'16380228', u'1K-blocks': u'16380228', u'used': u'0', u'capacity': u'0%', u'filesystem': u'devtmpfs'}, u'/boot': {u'available': u'900568', u'1K-blocks': u'1038336', u'used': u'137768', u'capacity': u'14%', u'filesystem': u'/dev/vda1'}, u'/sys/fs/cgroup': {u'available': u'16390072', u'1K-blocks': u'16390072', u'used': u'0', u'capacity': u'0%', u'filesystem': u'tmpfs'}, u'/': {u'available': u'158869984', u'1K-blocks': u'208655340', u'used': u'49785356', u'capacity': u'24%', u'filesystem': u'/dev/vda2'}, u'/run': {u'available': u'16373024', u'1K-blocks': u'16390072', u'used': u'17048', u'capacity': u'1%', u'filesystem': u'tmpfs'}, u'/run/user/0': {u'available': u'3278016', u'1K-blocks': u'3278016', u'used': u'0', u'capacity': u'0%', u'filesystem': u'tmpfs'}, u'/run/user/994': {u'available': u'3278016', u'1K-blocks': u'3278016', u'used': u'0', u'capacity': u'0%', u'filesystem': u'tmpfs'}, u'/dev/shm': {u'available': u'16389652', u'1K-blocks': u'16390072', u'used': u'420', u'capacity': u'1%', u'filesystem': u'tmpfs'}}, u'ps.cpu_percent': 5.2}, u'10.20.1.27': {u'ps.virtual_memory': {u'available': 4109238272, u'total': 8589402112, u'percent': 52.2, u'free': 4109238272, u'used': 4480163840}, u'disk.usage': {u'D:\\': {u'available': 0, u'1K-blocks': 3193688, u'used': 3193688, u'capacity': u'100%', u'filesystem': u'D:\\'}, u'C:\\': {u'available': 45153464, u'1K-blocks': 62810108, u'used': 17656644, u'capacity': u'28%', u'filesystem': u'C:\\'}}, u'ps.cpu_percent': 28.0}}
#
# host_data = data.get("10.20.10.144")
# use_mem_size = host_data['ps.virtual_memory']['percent']
# cache_mem_size = host_data['ps.virtual_memory']
#
# from salt import client
# from salt import utils
#
# local = client.LocalClient()


class Findme(object):
    def __init__(self,things,like):
        self.things = things
        self.like = like
    
    def best(self):
        print("I'm kind of the world")

class Gift(Findme):

    def best(self):
        super(Gift, self).best()
        print("you're best in the world")


g = Gift(123,456)
g.best()
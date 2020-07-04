# import winrm
#
# win2008 = winrm.Session("http://10.20.1.27:5985/wsman",auth=('administrator','abcd1234,'))
# r = win2008.run_ps(r"(New-Object System.Net.WebClient).DownloadFile('http://39.97.104.43:80/download/Salt-Minion-3000.2-Py2-AMD64-Setup.exe','C:\tmpsalt\Salt-Minion-3000.2-Py2-AMD64-Setup.exe')")
# print(r.std_err.decode('utf-8'))
# print(r.std_out.decode('utf-8'))

a  = {
	u'D:\\': {
		u'available': 0,
		u'1K-blocks': 3193688,
		u'used': 3193688,
		u'capacity': u'100%',
		u'filesystem': u'D:\\'
	}, u'C:\\': {
		u'available': 46010992,
		u'1K-blocks': 62810108,
		u'used': 16799116,
		u'capacity': u'27%',
		u'filesystem': u'C:\\'
	}
}

for i in a:
    print(a[i].get("1K-blocks"))
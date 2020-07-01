import winrm

win2008 = winrm.Session("http://10.20.1.27:5985/wsman",auth=('administrator','abcd1234,'))
r = win2008.run_ps(r"(New-Object System.Net.WebClient).DownloadFile('http://39.97.104.43:80/download/Salt-Minion-3000.2-Py2-AMD64-Setup.exe','C:\tmpsalt\Salt-Minion-3000.2-Py2-AMD64-Setup.exe')")
print(r.std_err.decode('utf-8'))
print(r.std_out.decode('utf-8'))
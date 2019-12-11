#!/usr/bin/env python3

import pymssql
import time
import datetime

class SqlServerC(object):

    def __init__(self,hostip,username,password):
        self.hostip = hostip
        self.username = username
        self.password = password
        self.result = {}

    def __connection(self,SQL):
        '''
        :param SQL: 需要传递的SQL语句
        :return: 将Oracle连接返回并提供给工作函数使用
        '''
        try:
            conn = pymssql.connect(server='%s'%self.hostip,user='%s'%self.username,password='%s'%self.password,charset='utf8')
            curs = conn.cursor()
            rr = curs.execute(SQL)
            row = curs.fetchall()
        except Exception as e:
            print('当前SqlServer数据库连接出现错误%s'%e)
        return row

    def __enumerateApi(self,data,content=None):
        __data = {}
        __data_list = []
        for row in content:
            for i,j in enumerate(data):
                __data[j] = row[i]
                if i == len(data) - 1:
                    __data[j] = row[i]
                    __data_list.append(__data)
                    __data = {}
        return __data_list

    def __strdatatimeApi(self,data,content):
        #次函数和__enumerateApi功能一样，只是为了解决时间格式问题
        __data = {}
        __data_list = []
        for row in content:
            for i,j in enumerate(data):
                __data[j] = row[i]
                if i == len(data) - 1:
                    __data[j] = str(row[i])
                    __data_list.append(__data)
                    __data = {}
        return __data_list

    def ssversion(self):
        # 查询当前SqlServer版本号
        r_row = self.__connection(r'select @@version')
        result = r_row

    def ssdatasize(self):
        # 查看所有数据库名称及大小
        data = {}
        data_list =[]
        r_row = self.__connection(r'exec sp_helpdb')
        result = r_row
        for i in result:
            data['name'] = i[0]
            data['size'] = i[1]
            data['onwer'] = i[2]
            data['created'] = i[4]
            data['status'] = i[5]
            data_list.append(data)
            data = {}

    def ssconn(self):
        #查看各数据库连接数
        data = {}
        data_list = []
        SQL = r'''
        SELECT @@ServerName AS server,NAME AS dbname,COUNT(STATUS) AS number_of_connections,GETDATE() AS timestamp
FROM sys.databases sd LEFT JOIN sys.sysprocesses sp ON sd.database_id = sp.dbid
WHERE database_id NOT BETWEEN 1 AND 4
GROUP BY NAME
        '''
        r_row = self.__connection(SQL)
        for i in r_row:
            data['server'] = i[0]
            data['dbname'] = i[1]
            data['number_of_connections'] = i[2]
            data['timestamp'] = str(i[3])
            data_list.append(data)
            data = {}
        print(data_list)

    def sqlstarttime(self):
        #SqlServer 数据库启动时间
        SQL = r'select convert(varchar(30),login_time,120) from master..sysprocesses where spid=1'
        r_row = self.__connection(SQL)
        self.result['ServerStartTime'] = r_row[0][0]

    def currentInstance(self):
        #当前数据库实例名 ---------- batev1
        SQL = r"select 'Instance:'+ltrim(@@servicename)"
        r_row = self.__connection(SQL)
        if len(r_row) == 1:
            #当前只有一个数据库实例
            instance = r_row[0][0]
            instance_name = instance.split(':')[1]
        else:
            #当前有一个以上的数据库实例
            instance_list = []
            for i in r_row:
                instance = i[0]
                instance_name = instance.split(':')[1]
                instance_list.append(instance_name)
        self.result['Instance_name'] = instance_name

    def logsize(self):
        #sqlserver日志文件大小及使用情况
        mydata = ['Database_Name','LogSizeMB','LogSizeUsage','Status']
        SQL = r'dbcc sqlperf(logspace)'
        r_row = self.__connection(SQL)
        res = self.__enumerateApi(mydata,r_row)
        self.result['Logsize'] = res

    def SqlServerDisk(self):
        #SqlServer service use localhost disk usage
        # SQL查询到数据为单行，不适合用self.__enumerateApi函数，会导致本地函数执行过于冗长
        mydata = ['ReadDiskTime','WriteDiskTime','ErrorTime','Current_time']
        SQL = '''
        select
@@total_read [读取磁盘次数],
@@total_write [写入磁盘次数],
@@total_errors [磁盘写入错误数],
getdate() [当前时间]
        '''
        r_row = self.__connection(SQL)
        res = self.__enumerateApi(mydata,r_row)
        self.result['SqlserverDisk'] = res

    def SqlserverIOState(self):
        # 获取I/O工作情况
        data = {}
        SQL = '''
        select @@io_busy,
@@timeticks [每个时钟周期对应的微秒数],
@@io_busy*@@timeticks [I/O操作毫秒数],
getdate() [当前时间]
        '''
        r_row = self.__connection(SQL)[0]
        data['每个时钟周期对应的微秒数'] = r_row[1]
        data['I/O操作毫秒数'] = r_row[2]
        data['当前时间'] = str(r_row[3])

    def SqlserverCPUsate(self):
        #查看CPU活动及工作情况
        data = {}
        SQL = '''
        select
@@cpu_busy,
@@timeticks [每个时钟周期对应的微秒数],
@@cpu_busy*cast(@@timeticks as float)/1000 [CPU工作时间(秒)],
@@idle*cast(@@timeticks as float)/1000 [CPU空闲时间(秒)],
getdate() [当前时间]
        '''
        r_row = self.__connection(SQL)[0]
        data['每个时钟周期对应的微秒数'] = r_row[1]
        data['CPU工作时间(秒)'] = r_row[2]
        data['CPU空闲时间(秒)'] = str(r_row[3])

    def CheckLock(self):
        #检查锁与等待
        mydata = ['spid','dbid','ObjId','IndId','Type','Resource','Mode','Status']
        r_row = self.__connection(r"exec sp_lock")
        res = self.__enumerateApi(mydata,r_row)
        self.result['CheckLock'] = res

    def __UserProcessMssage(self):
        #用户和进程信息,此函数仅为保留函数，不建议使用该函数查看SqlServer资源使用信息
        SQL= r'''
        exec sp_who2
        '''
        mydata = ['SPID', 'Status', 'Login', 'HostName', 'BlkBy', 'DBName', 'Command', 'CPUTime','DiskIO', 'LastBatch', 'ProgramName', 'SPID', 'REQUESTID']
        r_row = self.__connection(SQL)
        res = self.__enumerateApi(mydata,r_row)
        self.result['UserProcessMssage'] = res

    def ActiveUserProcess(self):
        #活动用户和进程的信息
        mydata = ['spid', 'ecid', 'status', 'loginame', 'hostname', 'blk', 'dbname', 'cmd', 'request_id']
        r_row = self.__connection(r"exec sp_who 'active'")
        res = self.__enumerateApi(mydata,r_row)
        self.result['ActiveUserProcess'] = res

    def currentSQL(self):
        #当前正在执行的SQL语句
        SQL = r"select session_id,start_time,status,command,text from sys.dm_exec_requests r cross apply sys.dm_exec_sql_text(r.sql_handle) s where session_id>50 and session_id<>@@spid"
        mydata = ['session_id','start_time','status','command','test']
        r_row = self.__connection(SQL)
        res = self.__enumerateApi(mydata,r_row)
        self.result['CurrentSQL'] = res

    def session(self):
        # 各个数据库中连接数
        SQL = '''
        SELECT @@ServerName AS server,NAME AS dbname,COUNT(STATUS) AS number_of_connections,GETDATE() AS timestamp
FROM sys.databases sd LEFT JOIN sys.sysprocesses sp ON sd.database_id = sp.dbid
WHERE database_id NOT BETWEEN 1 AND 4
GROUP BY NAME
        '''
        mydata = ['server','dbname','count','timestamp']
        r_row = self.__connection(SQL)
        res = self.__strdatatimeApi(mydata,r_row)
        self.result['session'] = res

    def test(self):
        SQL = r"SELECT * FROM Persons  OFFSET 1 ROWS  FETCH NEXT 10 ROWS ONLY"
        r_row = self.__connection(SQL)
        print(r_row)


s = SqlServerC('10.20.50.97','sa','nihao123!')
s.test()
# s.session()
# print(s.result)
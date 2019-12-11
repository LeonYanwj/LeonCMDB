#!/usr/bin/env python

import re
import time
import cx_Oracle

class OracleCheck(object):

    def __init__(self,hostip,username,password,instance):
        self.hostip = hostip
        self.username = username
        self.password = password
        self.instance = instance
        self.result = {}

    def __connection(self,SQL):
        '''
        :param SQL: 需要传递的SQL语句
        :return: 将Oracle连接返回并提供给工作函数使用
        '''
        try:
            conn = cx_Oracle.connect("%s/%s@%s:49161/%s"%(self.username,self.password,self.hostip,self.instance))
            curs = conn.cursor()
            rr = curs.execute(SQL)
            row = curs.fetchall()
        except Exception as e:
            print("脚本执行过程中出错，错误编号:%s"%e)
        return row

    def get_hwh(self):
        '''
        :param r_row: 获取数据库缓冲区高速缓存命中率
        :return:
        '''
        r_row = self.__connection(r"select 1-(phy.value/(cur.value+con.value)) from v$sysstat cur, v$sysstat con, v$sysstat phy where cur.name = 'db block gets' and con.name = 'consistent gets' and phy.name = 'physical reads'")
        result = r_row[0][0]
        #将浮点数转换成百分比
        result = "%.2f%%"%(result * 100)
        self.result['hwh'] = result

    def get_ttn(self):
        '''
        :param data: 获取临时表空间中的数值
        :return:
        '''
        data = {}
        r_row = self.__connection(r'select FILE_NAME, FILE_ID, TABLESPACE_NAME, BYTES/1024/1024 "BYTES(M)", USER_BYTES/1024/1024 "USER_BYTES(M)", status from dba_temp_files')
        result = r_row[0]
        data['文件名称'] = result[0]
        data['文件ID'] = result[1]
        data['表空间名称'] = result[2]
        data['表空间大小'] = result[3]
        data['表空间已使用大小'] = result[4]
        data['表空间状态'] = result[5]
        self.result['ttn'] = data

    def cf(self):
        '''
        :return: oracle contronl file name and path
        '''
        r_row = self.__connection(r"select name from v$controlfile")
        result = r_row[0]
        data = []
        for i in result:
            data.append(i)
        self.result['控制文件'] = data

    def get_chart(self):
        r_row = self.__connection("select * from v$nls_parameters where parameter='NLS_CHARACTERSET'")[0][1]
        self.result['default_charaset'] = r_row

    def rb(self):
        data = {}
        data_list = []
        r_row = self.__connection("SELECT SEGMENT_NAME, TABLESPACE_NAME, STATUS FROM DBA_ROLLBACK_SEGS")
        for i in r_row:
            data['SEGMENT_NAME'] = i[0]
            data['TABLESPACE_NAME'] = i[1]
            data['STATUS'] = i[2]
            data_list.append(data)
            data = {}
        self.result['rb'] = data_list

    def rdl(self):
        """look at oracle redolog file """
        r_row = self.__connection(r"select a.member,a.group#,b.thread#,b.bytes,b.members,b.status from v$logfile a,v$log b where a.group#=b.group#")
        data = {}
        data_list = []
        for i in r_row:
            data['MEMBER'] = i[0]
            data['GROUP'] = i[1]
            data['THREAD'] = i[2]
            data['BYTES'] = i[3]
            data['MEMBERS'] = i[4]
            data['STATUS'] = i[5]
            data_list.append(data)
            data = {}
        self.result['rdl'] = data_list

    def tsu(self):
        '''oracle tablespace_name size and usage'''
        data = {}
        data_list = []
        row = r"""
        select substr(a.TABLESPACE_NAME,1,30) TablespaceName,
sum(a.bytes/1024/1024) as "Totle_size(M)",
sum(nvl(b.free_space1/1024/1024,0)) as "Free_space(M)",
sum(a.bytes/1024/1024)-sum(nvl(b.free_space1/1024/1024,0)) as "Used_space(M)",
round((sum(a.bytes/1024/1024)-sum(nvl(b.free_space1/1024/1024,0)))
*100/sum(a.bytes/1024/1024),2) as "Used_percent%" from dba_data_files a,(select sum(nvl(bytes,0)) free_space1,file_id from dba_free_space
group by file_id) b where a.file_id = b.file_id(+) group by a.TABLESPACE_NAME
order by "Used_percent%"
        """
        r_row = self.__connection(row)
        for i in r_row:
            data['TABLESPACENAME'] = i[0]
            data['Totle_size_MB'] = i[1]
            data['Free_space_MB'] = i[2]
            data['Used_space_MB'] = i[3]
            data['Used_percent'] = i[4]
            data_list.append(data)
            data = {}
        self.result['tsu'] = data_list

    def odf(self):
        '''get oracle data file size/name/path/id/status'''
        data = {}
        data_list = []
        r_row = self.__connection(r"select tablespace_name,file_id,status,bytes/1024/1024 FileSizeM,file_name from dba_data_files order by tablespace_name")
        for i in r_row:
            data['TABLESPACE_NAME'] = i[0]
            data['FILE_ID'] = i[1]
            data['STATUS'] = i[2]
            data['FILESIZE_BM'] = i[3]
            data['FILE_NAME'] = i[4]
            data_list.append(data)
            data = {}
        self.result['odf'] = data_list

    def tse(self):
        'oracle tablespace extend method'
        data = {}
        data_list =[]
        r_row = self.__connection(r"select TABLESPACE_NAME, BLOCK_SIZE, EXTENT_MANAGEMENT, SEGMENT_SPACE_MANAGEMENT from dba_tablespaces")
        for i in r_row:
            data['TABLESPACE_NAME'] = i[0]
            data['BLOCK_SIZE'] = i[1]
            data['EXTENT_MANAGEMENT'] = i[2]
            data['SEGMENT_SPACE_MANAGEMENT'] = i[3]
            data_list.append(data)
            data = {}
        self.result['tse'] = data_list

    def ub(self):
        'usr objects(table index size)'
        data = {}
        data_list = []
        r_row = self.__connection(r"select OWNER ,SEGMENT_NAME,PARTITION_NAME,SEGMENT_TYPE,TABLESPACE_NAME,bytes/1024/1024 as table_size_M from  Dba_Segments where SEGMENT_TYPE='TABLE' order by OWNER")
        for i in r_row:
            data['OWNER'] = i[0]
            data['SEGMENT_NAME'] = i[1]
            data['PARTITION_NAME'] = i[2]
            data['SEGMENT_TYPE'] = i[3]
            data['TABLESPACE_NAME'] = i[4]
            data['TABLE_SIZE_MM'] = i[5]
            data_list.append(data)
            data = {}
        self.result['ub'] = data_list

    def invaild_index(self):
        'check oracle invaild index'

        row = '''
        select index_name, owner, status, tablespace_name
 from dba_indexes
 where owner not in('SYS','SYSTEM')
 and status != 'VALID'
 and tablespace_name is not null
union all
select index_name, index_owner owner, status, tablespace_name
 from dba_ind_partitions
 where index_owner not in ('SYS','SYSTEM')
 and status <> 'USABLE'
 and tablespace_name is not null'''
        r_row = self.__connection(row)
        if not r_row:
            self.result['invaild_index'] = None
        else:
            self.result['invaild_index'] = r_row

    def session_usage(self):
        'oracle session useage '

        row = r'''select cur_sessions, tot_sessions, a.cur_sessions/b.tot_sessions*100 "sessions used%" from (select count(*) cur_sessions from v$session) a, (select value tot_sessions from v$parameter where name = 'sessions') b'''
        r_row = self.__connection(row)[0]
        data = {}
        data['cur_sessions'] = r_row[0]
        data['tot_sessions'] =r_row[1]
        data['sessions_used%'] =r_row[1]
        self.result['session_usage'] = data


o = OracleCheck('10.20.10.13','leonyan','123456','XE')
import pymssql


server = '172.20.128.3'
user = 'sa'
password = 'abc123,'
database = 'test'

conn = pymssql.connect(server,user,password,database)
cursor = conn.cursor()


# 查询操作
cursor.execute('SELECT * FROM persons')
row = cursor.fetchone()
for i in row:
    print(i)
conn.close()


'''
class SQLServer(object):
    def __init__(self,server,user,password,database):
        self.server = server
        self.user = user
        self.password = password
        self.database = database
    def __getConnect(self):
        if not self.database:
            raise(NameError,'no settings databases infomations')
        self.conn = pymssql.connect(self.server,self.user,self.password,self.database)
        cur = self.conn.cursor()
        if not cur:
            raise(NameError,'connect database error')
        else:
            return cur
    def execQuery(self,sql):
        cur = self.__getConnect()
        cur.execute(sql)
        result = cur.fetchall()
        self.conn.close()
        return result
    def dataStatus(self,sql):
        if self.execQuery(sql):
            res = '数据库正常运行'
        else:
            res = '数据库未正常运行'
        return res
'''
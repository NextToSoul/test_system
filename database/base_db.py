import pymysql
from config.settings import DB_USER,DB_HOST,DB_PASSWORD,DB_NAME

class DatabaseManage():
    def __init__(self):
        self.connection=None #创建一个属性

    def __enter__(self):
        self.create_connection()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_connection()

    #创建数据库连接
    def create_connection(self):
        if not self.connection or not self.connection.open:
            try:
                self.connection=pymysql.connect(
                    host=DB_HOST,
                    user=DB_USER,
                    password=DB_PASSWORD,
                    database=DB_NAME,
                    cursorclass=pymysql.cursors.DictCursor
                )

            except Exception as e:
                print(f'数据库连接错误：{e}')

        return self.connection


    #查询
    def fetch_query(self,query,params=None,single=False):
        result=None
        if self.connection:
            try:
                with self.connection.cursor() as cursor:
                    cursor.execute(query,params) # 执行查询
                    if single:
                        result=cursor.fetchone() #查询一条记录
                    else:
                        result=cursor.fetchall()
            except Exception as e:
                print(f'查询错误:{e}')
        else:
            print(f'没有建立数据库连接')

        return result

    #执行（新增、删除、修改）语句
    def execute_query(self,query,params=None):
        if self.connection:
            try:
                with self.connection.cursor() as cursor:
                    cursor.execute(query,params) # 执行新增/修改/删除
                    self.connection.commit() # 提交，保存到数据库
                    #return True
                    return cursor.lastrowid
            except Exception as e:
                print(f'执行异常:{e}')
                return None
        else:
            print(f'没有建立数据库连接')
        return None

    #关闭数据库连接
    def close_connection(self):
        if self.connection:
            self.connection.close()


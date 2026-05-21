from database.base_db import DatabaseManage
#from project_management.project_dialog import BaseProjectDialog

class ppcuDB(DatabaseManage):
    #查询ppcu信息
    def fetch_ppcus(self):
        query = '''
            SELECT ppcu_number from ppcu_numbers
            '''
        return self.fetch_query(query)

    #查询ppcu编号所对应的PPCU ID
    def fetch_ppcuID(self,ppcu_number):
        query='''
        select ppcu_id
        from ppcu_numbers
        where ppcu_number=%s;
        '''
        result=self.fetch_query(query,(ppcu_number,))
        return result[0]['ppcu_id'] if result else None

'''if __name__=='__main__':
    with ppcuDB() as db:
        print(db.fetch_ppcuID(ppcu_number='Z01-1-PPCU'))
        print(type(db.fetch_ppcuID(ppcu_number='Z01-1-PPCU')))
        print(db.fetch_ppcus())'''





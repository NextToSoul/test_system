from database.base_db import DatabaseManage

class feedsystemDB(DatabaseManage):
    #查询贮供信息
    def fetch_feedsystems(self):
        query='''
        select feedsystem_number from feedsystem_numbers
        '''
        return self.fetch_query(query)

    #查询贮供编号对应的ID
    def fetch_feedsystemID(self,feedsystem_number):
        query='''
        SELECT
          feedsystem_id 
        FROM
          feedsystem_numbers 
        WHERE
          feedsystem_number = %s;
        '''
        result=self.fetch_query(query,(feedsystem_number,))
        return result[0]['feedsystem_id']

'''if __name__=='__main__':
    with feedsystemDB() as db:
        print(db.fetch_feedsystemID('Z01-2-ZG'))'''
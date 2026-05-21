from database.base_db import DatabaseManage

class thrusterDB(DatabaseManage):
    #查询推力器信息
    def fetch_thrusters(self):
        query='''
        SELECT thruster_number from thruster_numbers
        '''

        return self.fetch_query(query)

    #查询推力器编号所对应的ID
    def fetch_thrusterID(self,thruster_number):
        query='''
        select thruster_id
        from thruster_numbers
        where thruster_number=%s;
        '''
        result=self.fetch_query(query,(thruster_number,))
        return result[0]['thruster_id']

'''if __name__=='__main__':
    with thrusterDB() as db:
        print(db.fetch_thrusterID('Z01-4-TLQ'))'''
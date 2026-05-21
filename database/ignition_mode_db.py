from scipy.cluster.hierarchy import single

from database.base_db import DatabaseManage


class IgnitionModeDB(DatabaseManage):

    #获取点火模式
    def fetch_modes(self):
        query='''
        SELECT
          ignition_mode 
        FROM
          ignition_modes
        '''
        return self.fetch_query(query)

    #获取点火模式对应的ID
    def fetch_mode_id(self,ignition_mode):
        query='''
        SELECT
          ignition_mode_id 
        FROM
          ignition_modes 
        WHERE
          ignition_mode = %s
        '''
        params=(ignition_mode,)
        result=self.fetch_query(query,params,single=True)
        if not result:
            return -1
        return result['ignition_mode_id']
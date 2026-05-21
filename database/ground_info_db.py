from database.base_db import DatabaseManage

class GroundInfoDB(DatabaseManage):

    #添加接地信息
    def add_ground_info(self,ground_info):
        query='''
        INSERT INTO grounding_record ( project_id, mc_sc, ppcu_coldplate, ppcu_thruster, ppcu_feedsystem, busneg_feedsystem, oc_feedsystem, ppcu_mc, ppcu_sc, commgnd_feedsystem, grounding_notes )
        VALUES
          (
            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
          )
        '''
        # 如果是空字符串 / 只有空格 → 存为空字符串 ''
        def clean_val(val):
            val=str(val).strip()
            return val if val else None

        params=(
            clean_val(ground_info['project_id']),
            clean_val(ground_info['mc_sc']),
            clean_val(ground_info['ppcu_coldplate']),
            clean_val(ground_info['ppcu_thruster']),
            clean_val(ground_info['ppcu_feedsystem']),
            clean_val(ground_info['busneg_feedsystem']),
            clean_val(ground_info['oc_feedsystem']),
            clean_val(ground_info['ppcu_mc']),
            clean_val(ground_info['ppcu_sc']),
            clean_val(ground_info['commgnd_feedsystem']),
            clean_val(ground_info['grounding_notes'])
        )
        return self.execute_query(query,params)

    #查询project_id对应的接地信息是否存在
    def fetchbool_projectid_to_ground(self,project_id):
        query='''
        SELECT
          1 
        FROM
          grounding_record 
        WHERE
          project_id = %s 
          LIMIT 1
        '''
        params=(project_id,)
        result=self.fetch_query(query,params,single=True)
        return result is not None

    #查询project_id对应的接地信息
    def fetch_projectid_to_ground(self,project_id):
        query='''
        SELECT
          * 
        FROM
          grounding_record 
        WHERE
          project_id = %s 
        '''
        params=(project_id,)
        result=self.fetch_query(query,params,single=True)
        return result

    #更新接地信息
    def update_ground_info(self,ground_info):
        query='''
        UPDATE grounding_record 
        SET mc_sc = %s,
            ppcu_coldplate = %s,
            ppcu_thruster = %s,
            ppcu_feedsystem = %s,
            busneg_feedsystem = %s,
            oc_feedsystem = %s,
            ppcu_mc = %s,
            ppcu_sc = %s,
            commgnd_feedsystem = %s,
            grounding_notes = %s 
        WHERE
            project_id =%s
        '''

        # 如果是空字符串 / 只有空格 → 存为空字符串 ''
        def clean_val(val):
            val = str(val).strip()
            return val if val else None

        params=(
            clean_val(ground_info['mc_sc']),
            clean_val(ground_info['ppcu_coldplate']),
            clean_val(ground_info['ppcu_thruster']),
            clean_val(ground_info['ppcu_feedsystem']),
            clean_val(ground_info['busneg_feedsystem']),
            clean_val(ground_info['oc_feedsystem']),
            clean_val(ground_info['ppcu_mc']),
            clean_val(ground_info['ppcu_sc']),
            clean_val(ground_info['commgnd_feedsystem']),
            clean_val(ground_info['grounding_notes']),
            clean_val(ground_info['project_id'])
        )
        self.execute_query(query,params)
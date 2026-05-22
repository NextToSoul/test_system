#from scipy.cluster.hierarchy import single

from database.base_db import DatabaseManage


class IgnitionConditionDB(DatabaseManage):

    #新增点火条件
    def add_ignition_condition(self,condition_infos):
        query= '''
        INSERT into ignition_condition (project_id,ignition_time,ignition_mode_id,busbar_voltage,busbar_current,transient_voltage,
        steady_voltage,fc_tgt,ol_ifc,heating_current,heating_current2,keep_alive_current,excitation_current,anode_current_limit,
        system_power_limit,pid_proportional_constant,thruster_duration,pi_cdt,anode_duration,sv_mbs,condition_notes)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        '''
        params=(
            condition_infos['project_id'],
            condition_infos['ignition_time'],
            condition_infos['ignition_mode_id'],
            condition_infos['busbar_voltage'],
            condition_infos['busbar_current'],
            condition_infos['transient_voltage'],
            condition_infos['steady_voltage'],
            condition_infos['fc_tgt'],
            condition_infos['ol_ifc'],
            condition_infos['heating_current'],
            condition_infos['heating_current2'],
            condition_infos['keep_alive_current'],
            condition_infos['excitation_current'],
            condition_infos['anode_current_limit'],
            condition_infos['system_power_limit'],
            condition_infos['pid_proportional_constant'],
            condition_infos['thruster_duration'],
            condition_infos['pi_cdt'],
            condition_infos['anode_duration'],
            condition_infos['sv_mbs'],
            condition_infos['condition_notes']
        )
        return self.execute_query(query,params)
        #return self.cursor.lastrowid

    #获取某project_id对应的点火条件和点火记录的组合(联合查询)
    def get_condition_and_record(self,project_id):
        query='''
        SELECT
          ignition_condition.*,
          ignition_modes.ignition_mode,
          ignition_record.* 
        FROM
          ignition_condition
          JOIN ignition_modes ON ignition_condition.ignition_mode_id = ignition_modes.ignition_mode_id
          JOIN ignition_record ON ignition_condition.condition_id = ignition_record.condition_id
        WHERE
          project_id = %s 
        ORDER BY
          ignition_time
        '''
        params=(project_id,)
        return self.fetch_query(query,params)

    #更新点火条件
    def update_condition(self,condition_infos,condition_id):
        query='''
        UPDATE ignition_condition 
        SET ignition_time = %s,
            ignition_mode_id = %s,
            busbar_voltage = %s,
            busbar_current = %s,
            transient_voltage = %s,
            steady_voltage = %s,
            fc_tgt = %s,
            ol_ifc = %s,
            heating_current = %s,
            heating_current2 = %s,
            keep_alive_current = %s,
            excitation_current = %s,
            anode_current_limit = %s,
            system_power_limit = %s,
            pid_proportional_constant = %s,
            thruster_duration = %s,
            pi_cdt = %s,
            anode_duration = %s,
            sv_mbs = %s,
            condition_notes = %s 
        WHERE
          condition_id = %s
        '''
        params=(
            condition_infos['ignition_time'],
            condition_infos['ignition_mode_id'],
            condition_infos['busbar_voltage'],
            condition_infos['busbar_current'],
            condition_infos['transient_voltage'],
            condition_infos['steady_voltage'],
            condition_infos['fc_tgt'],
            condition_infos['ol_ifc'],
            condition_infos['heating_current'],
            condition_infos['heating_current2'],
            condition_infos['keep_alive_current'],
            condition_infos['excitation_current'],
            condition_infos['anode_current_limit'],
            condition_infos['system_power_limit'],
            condition_infos['pid_proportional_constant'],
            condition_infos['thruster_duration'],
            condition_infos['pi_cdt'],
            condition_infos['anode_duration'],
            condition_infos['sv_mbs'],
            condition_infos['condition_notes'],
            condition_id
        )
        self.execute_query(query,params)

    def delete_condition(self,condition_id):
        '''删除单条数据'''
        query='''
        DELETE 
        FROM
          ignition_condition 
        WHERE
          condition_id = %s
        '''
        params=(condition_id,)
        self.execute_query(query,params)

    # 从数据库中读取表结构
    def get_table_colums(self, table_name):
        query=f"DESCRIBE {table_name}"
        rows=self.fetch_query(query)
        #print(rows)
        colums=[]
        for row in rows:
            field_name=row['Field']
            field_type=row['Type'].lower()

            if field_name in ['project_id','condition_id']:
                continue
            #自动识别类型
            if 'int' in field_type:
                py_type='int'
            elif 'float' in field_type or 'double' in field_type:
                py_type='float'
            elif 'time' in field_type:
                py_type='time'
            elif 'date' in field_type:
                py_type='date'
            else:
                py_type='string'
            colums.append({'field':field_name,'type':py_type})
        #print(colums)




if __name__=='__main__':
    with IgnitionConditionDB() as db:
        db.get_table_colums('ignition_condition')

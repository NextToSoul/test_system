from database.base_db import DatabaseManage


class IgnitionRecordDB(DatabaseManage):

    #新增点火记录
    def add_ignition_record(self,record_infos):
        params=(
            record_infos['condition_id'],
            record_infos['oscilloscope1_drawnumber'],
            record_infos['oscilloscope2_drawnumber'],
            record_infos['flow_adjustment_time'],
            record_infos['heat_traffic'],
            record_infos['heat_duration'],
            record_infos['p1_anode_surge_current'],
            record_infos['p1_maximum_anode_voltage'],
            record_infos['p1_minimum_holding_current'],
            record_infos['p1_bus_current_surge'],
            record_infos['p2_anode_transient_voltage'],
            record_infos['p3_anode_surge_current'],
            record_infos['p3_maximum_anode_voltage'],
            record_infos['p3_minimum_anode_voltage'],
            record_infos['p3_bus_current_surge'],
            record_infos['p3_minimum_bus_current'],
            record_infos['p4_transient_voltage'],
            record_infos['p4_anode_steady_current'],
            record_infos['p4_bus_current'],
            record_infos['p4_pp_anode_current'],
            record_infos['p4_pp_bus_current'],
            record_infos['p4_pp_busbar_voltage'],
            record_infos['p4_pp_keep_alive_current'],
            record_infos['thrust'],
            record_infos['p4_traffic'],
            record_infos['test_conclusion'],
            record_infos['record_notes']
        )

        values=','.join(['%s']*len(params))
        query=f'''
        INSERT INTO ignition_record (condition_id,oscilloscope1_drawnumber,oscilloscope2_drawnumber,flow_adjustment_time,heat_traffic,
        heat_duration,p1_anode_surge_current,p1_maximum_anode_voltage,p1_minimum_holding_current,p1_bus_current_surge,
        p2_anode_transient_voltage,p3_anode_surge_current,p3_maximum_anode_voltage,p3_minimum_anode_voltage,p3_bus_current_surge,
        p3_minimum_bus_current,p4_transient_voltage,p4_anode_steady_current,p4_bus_current,p4_pp_anode_current,p4_pp_bus_current,
        p4_pp_busbar_voltage,p4_pp_keep_alive_current,thrust,p4_traffic,test_conclusion,record_notes)
VALUES ({values})
        '''
        self.execute_query(query,params)

    #更新点火记录
    def update_record(self,record_infos,condition_id):
        query='''
        UPDATE ignition_record 
        SET oscilloscope1_drawnumber=%s,
            oscilloscope2_drawnumber=%s,
            flow_adjustment_time=%s,
            heat_traffic=%s,
            heat_duration=%s,
            p1_anode_surge_current=%s,
            p1_maximum_anode_voltage=%s,
            p1_minimum_holding_current=%s,
            p1_bus_current_surge=%s,
            p2_anode_transient_voltage=%s,
            p3_anode_surge_current=%s,
            p3_maximum_anode_voltage=%s,
            p3_minimum_anode_voltage=%s,
            p3_bus_current_surge=%s,
            p3_minimum_bus_current=%s,
            p4_transient_voltage=%s,
            p4_anode_steady_current=%s,
            p4_bus_current=%s,
            p4_pp_anode_current=%s,
            p4_pp_bus_current=%s,
            p4_pp_busbar_voltage=%s,
            p4_pp_keep_alive_current=%s,
            thrust=%s,
            p4_traffic=%s,
            test_conclusion=%s,
            record_notes=%s
        WHERE condition_id=%s
        '''
        params=(
            record_infos['oscilloscope1_drawnumber'],
            record_infos['oscilloscope2_drawnumber'],
            record_infos['flow_adjustment_time'],
            record_infos['heat_traffic'],
            record_infos['heat_duration'],
            record_infos['p1_anode_surge_current'],
            record_infos['p1_maximum_anode_voltage'],
            record_infos['p1_minimum_holding_current'],
            record_infos['p1_bus_current_surge'],
            record_infos['p2_anode_transient_voltage'],
            record_infos['p3_anode_surge_current'],
            record_infos['p3_maximum_anode_voltage'],
            record_infos['p3_minimum_anode_voltage'],
            record_infos['p3_bus_current_surge'],
            record_infos['p3_minimum_bus_current'],
            record_infos['p4_transient_voltage'],
            record_infos['p4_anode_steady_current'],
            record_infos['p4_bus_current'],
            record_infos['p4_pp_anode_current'],
            record_infos['p4_pp_bus_current'],
            record_infos['p4_pp_busbar_voltage'],
            record_infos['p4_pp_keep_alive_current'],
            record_infos['thrust'],
            record_infos['p4_traffic'],
            record_infos['test_conclusion'],
            record_infos['record_notes'],
            condition_id
        )
        self.execute_query(query,params)

    def delete_record(self,condition_id):
        '''删除单条数据'''
        query='''
        DELETE 
        FROM
          ignition_record 
        WHERE
          condition_id = %s
        '''
        params=(condition_id,)
        self.execute_query(query,params)
from numpy.ma.core import append

from database.base_db import DatabaseManage

#创建项目数据库
class itemDB(DatabaseManage):
    #查询项目信息
    def fetch_items(self):
        query='''
    SELECT
      i.*,
      p.ppcu_number,
      t.thruster_number,
      f.feedsystem_number 
    FROM
      ignition_item i
      JOIN ppcu_numbers p ON i.ppcu_id = p.ppcu_id
      JOIN thruster_numbers t ON i.thruster_id = t.thruster_id
      JOIN feedsystem_numbers f ON i.feedsystem_id = f.feedsystem_id 
    ORDER BY
      project_id ASC 
        '''

        return self.fetch_query(query)

    #翻页查询
    def fetch_trun_page(self,page,per_page=20):
        offset=(page-1)*20
        query='''
        SELECT
          i.*,
          p.ppcu_number,
          t.thruster_number,
          f.feedsystem_number 
        FROM
          ignition_item i
          JOIN ppcu_numbers p ON i.ppcu_id = p.ppcu_id
          JOIN thruster_numbers t ON i.thruster_id = t.thruster_id
          JOIN feedsystem_numbers f ON i.feedsystem_id = f.feedsystem_id 
        ORDER BY
          project_id ASC
          LIMIT %s OFFSET %s
        '''
        params=(per_page,offset)
        return self.fetch_query(query,params)

    #数据总条目查询
    def fetch_total_items(self):
        query='''
        SELECT
          COUNT(*) AS count 
        FROM
          ignition_item
        '''
        result=self.fetch_query(query,single=True)
        return result['count']

    #有筛选条件时的总条目数查询
    def fetch_filter_items(self,search_text,combo_text,date_str):
        params = []
        conds = []
        query='''
        SELECT
          COUNT(*) AS count 
        FROM
          ignition_item
          JOIN ppcu_numbers ON ignition_item.ppcu_id = ppcu_numbers.ppcu_id
          JOIN thruster_numbers ON ignition_item.thruster_id = thruster_numbers.thruster_id
          JOIN feedsystem_numbers ON ignition_item.feedsystem_id = feedsystem_numbers.feedsystem_id 
        '''
        if search_text:
            conds.append(' (ppcu_number LIKE %s OR thruster_number LIKE %s OR feedsystem_number LIKE %s) ')
            params.extend([f'%{search_text}%'] * 3)
        if combo_text and combo_text!='所有工质':
            conds.append(' working_fluid=%s ')
            params.append(combo_text)
        if date_str and date_str!='请选择日期':
            conds.append(' ignition_date=%s ')
            params.append(date_str)

        if conds:
            query+=' WHERE '+' AND '.join(conds)
        result=self.fetch_query(query,params,single=True)
        return result['count']


    #搜索项目信息，并以分页条件拆分
    def search_items(self,search_text,combo_text,date_str,page,per_page=20):
        offset = (page - 1) * 20
        params=[]
        conds=[]
        query='''
        SELECT
          ignition_item.*,
          ppcu_numbers.ppcu_number,
          thruster_numbers.thruster_number,
          feedsystem_numbers.feedsystem_number 
        FROM
          ignition_item
          JOIN ppcu_numbers ON ignition_item.ppcu_id = ppcu_numbers.ppcu_id
          JOIN thruster_numbers ON ignition_item.thruster_id = thruster_numbers.thruster_id
          JOIN feedsystem_numbers ON ignition_item.feedsystem_id = feedsystem_numbers.feedsystem_id 
        '''
        if search_text:
            conds.append(' (ppcu_number LIKE %s OR thruster_number LIKE %s OR feedsystem_number LIKE %s) ')
            params.extend([f'%{search_text}%'] * 3)
        if combo_text and combo_text!='所有工质':
            conds.append(' working_fluid=%s ')
            params.append(combo_text)
        if date_str and date_str!='请选择日期':
            conds.append(' ignition_date=%s ')
            params.append(date_str)

        if conds:
            query+=' WHERE '+' AND '.join(conds)
        query+=' ORDER BY project_id ASC LIMIT %s OFFSET %s '
        params.extend([per_page,offset])

        return self.fetch_query(query,tuple(params))

    def batch_export_items(self,search_text,combo_text,date_str,project_ids):
        params=[]
        conds=[]
        query='''
        SELECT
          ignition_item.*,
          ppcu_numbers.ppcu_number,
          thruster_numbers.thruster_number,
          feedsystem_numbers.feedsystem_number 
        FROM
          ignition_item
          JOIN ppcu_numbers ON ignition_item.ppcu_id = ppcu_numbers.ppcu_id
          JOIN thruster_numbers ON ignition_item.thruster_id = thruster_numbers.thruster_id
          JOIN feedsystem_numbers ON ignition_item.feedsystem_id = feedsystem_numbers.feedsystem_id 
        '''
        if search_text:
            conds.append(' (ppcu_number LIKE %s OR thruster_number LIKE %s OR feedsystem_number LIKE %s) ')
            params.extend([f'%{search_text}%'] * 3)
        if combo_text and combo_text!='所有工质':
            conds.append(' working_fluid=%s ')
            params.append(combo_text)
        if date_str and date_str!='请选择日期':
            conds.append(' ignition_date=%s ')
            params.append(date_str)
        if len(project_ids)!=0:
            ids=','.join(['%s']*len(project_ids))
            conds.append(f' project_id IN ({ids}) ')
            params.extend(project_ids)

        if conds:
            query+=' WHERE '+' AND '.join(conds)
        query+=' ORDER BY project_id ASC'

        return self.fetch_query(query,tuple(params))

    #添加项目信息
    def add_item(self,item_info):
        query='''
        INSERT INTO ignition_item ( project_name, ppcu_id, thruster_id, feedsystem_id, working_fluid, sw_version, ignition_date, ignition_location )
        VALUES
          ( %s, %s, %s, %s, %s, %s, %s, %s );
        '''
        params=(
            item_info['project_name'],
            item_info['ppcu_id'],
            item_info['thruster_id'],
            item_info['feedsystem_id'],
            item_info['working_fluid'],
            item_info['sw_version'],
            item_info['ignition_date'],
            item_info['ignition_location']
        )
        self.execute_query(query,params)
        return self.get_last_insert_id()#返回当前创建的自增id

    #获取最后插入的自增ID
    def get_last_insert_id(self):
        if self.connection:
            return self.connection.insert_id()
        return None

    #复制表结构工具函数
    def copy_table(self,source_table,target_table):
        query=f'CREATE TABLE IF NOT EXISTS {target_table} LIKE {source_table}'
        self.execute_query(query)

    #更新ignition_item表中condition_table, record_table, grounding_table三个字段的名称
    def update_exclusive_table(self,condition_table,record_table,grounding_table,project_id):
        query='''
        UPDATE ignition_item 
        SET condition_table=%s,record_table=%s,grounding_table=%s 
        WHERE project_id=%s
        '''
        params=(condition_table,record_table,grounding_table,project_id)
        self.execute_query(query,params)

    #添加项目信息（通过导入excel方式添加）
    def add_excel_item(self,item_info):
        query='''
        INSERT INTO ignition_item ( project_id, project_name, ppcu_id, thruster_id, feedsystem_id, working_fluid, sw_version, ignition_date, ignition_location )
        VALUES
          ( %s, %s, %s, %s, %s, %s, %s, %s, %s );
        '''
        params = (
            item_info['project_id'],
            item_info['project_name'],
            item_info['ppcu_id'],
            item_info['thruster_id'],
            item_info['feedsystem_id'],
            item_info['working_fluid'],
            item_info['sw_version'],
            item_info['ignition_date'],
            item_info['ignition_location']
        )
        self.execute_query(query,params)

    #修改项目信息
    def edit_item(self,project_info,project_id):
        query='''
        UPDATE ignition_item 
        SET project_name = %s,
            ppcu_id = %s,
            thruster_id = %s,
            feedsystem_id = %s,
            working_fluid = %s,
            sw_version = %s,
            ignition_date = %s,
            ignition_location = %s 
        WHERE
          project_id = %s;
        '''
        params=tuple(project_info.values())+(project_id,)
        self.execute_query(query,params)

    # 更新项目信息（通过导入excel方式添加，遇到重复项时）
    def edit_excel_item(self,project_info,project_id):
        query='''
        UPDATE ignition_item 
        SET project_id = %s,
            project_name = %s,
            ppcu_id = %s,
            thruster_id = %s,
            feedsystem_id = %s,
            working_fluid = %s,
            sw_version = %s,
            ignition_date = %s,
            ignition_location = %s 
        WHERE
          project_id = %s;
        '''
        params=tuple(project_info.values())+(project_id,)
        self.execute_query(query,params)

    #查询project_id所对应的项目信息
    def fetch_existing_items(self,project_id):
        query='''
        SELECT
          i.*,
          p.ppcu_number,
          t.thruster_number,
          f.feedsystem_number 
        FROM
          ignition_item i
          JOIN ppcu_numbers p ON i.ppcu_id = p.ppcu_id
          JOIN thruster_numbers t ON i.thruster_id = t.thruster_id
          JOIN feedsystem_numbers f ON i.feedsystem_id = f.feedsystem_id 
        WHERE
          project_id =%s
        '''
        params=(project_id,)
        return self.fetch_query(query,params,single=True)

    #删除信息
    def delete_item(self,project_id):
        query='''
        DELETE 
        FROM
          ignition_item 
        WHERE
          project_id = %s
        '''
        params=(project_id,)
        self.execute_query(query,params)

    #批量删除项目信息
    def batch_delete_item(self,project_ids):
        params = ','.join(['%s'] * len(project_ids))
        query=f'''
        DELETE 
        FROM
          ignition_item 
        WHERE
          project_id IN ({params})
        '''
        self.execute_query(query,project_ids)



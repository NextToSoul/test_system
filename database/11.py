def search_items(self, search_text, combo_text):
    params = [f'%{search_text}%'] * 3
    query = '''
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
    WHERE
      ppcu_number LIKE %s 
      OR thruster_number LIKE %s 
      OR feedsystem_number LIKE %s 
    ORDER BY
      project_id ASC
      LIMIT 20 OFFSET 20
    '''
    if combo_text :
        if combo_text == '所有工质':
            query = '''
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
                    WHERE
                      ppcu_number LIKE %s 
                      OR thruster_number LIKE %s 
                      OR feedsystem_number LIKE %s 
                    ORDER BY
                      project_id ASC
                    '''
        else:

            query = '''
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
                    WHERE
                      (ppcu_number LIKE %s 
                      OR thruster_number LIKE %s 
                      OR feedsystem_number LIKE %s) 
                      AND working_fluid=%s
                    ORDER BY
                      project_id ASC
                    '''
            params.append(combo_text)
    return self.fetch_query(query, tuple(params))
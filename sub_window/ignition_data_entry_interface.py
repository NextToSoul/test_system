import time
from dataclasses import fields

from PySide6.QtCore import Qt, QTime
from PySide6.QtNetwork import QAbstractSocket
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QGridLayout, QTableWidget, QHeaderView, \
    QTableWidgetItem, QAbstractItemView
from openpyxl.styles.builtins import title
from qfluentwidgets import CardWidget, TableWidget, PushButton, setCustomStyleSheet, ComboBox, LineEdit, \
    StrongBodyLabel, TimePicker, InfoBar, RoundMenu, Action, \
    PrimaryDropDownPushButton, MessageBox
from qfluentwidgets import FluentIcon as FIF

from database.ignition_condition_db import IgnitionConditionDB
from database.ignition_mode_db import IgnitionModeDB
from database.ignition_record_db import IgnitionRecordDB
from utils.custom_button_style import ADD_BUTTON_STYLE, UPDATE_BUTTON_STYLE, DELETE_BUTTON_STYLE
from utils.custom_function import is_double, to_none
from utils.performance_monitoring_tool import timer
from utils.ui_components import CustomGroundHeaderView


class IgnitionDataEntryInterface(QWidget):

    def __init__(self, project_id=None):
        super().__init__()
        self.setWindowTitle('点火数据记录')
        self.project_id = project_id
        # self.resize(400, 300)
        self.showMaximized()
        self.setup_ui()
        self.load_data()
        self.populate_table()

    def setup_ui(self):
        # 给整个界面定义一个垂直布局
        layout = QVBoxLayout(self)
        #创建一个cardwidget，用于装【新增】、【修改】、【删除】按钮
        card_widget = CardWidget(self)
        #创建一个cardwidget，用于装【保存】、【清空】按钮
        card2_widget=CardWidget(self)
        # 给card_widget创建一个水平布局
        card_hboxlayout = QHBoxLayout(card_widget)
        card2_hboxlayout=QHBoxLayout(card2_widget)

        # 在card_hboxlayout中添加并设置控件
        #【新增】按钮
        self.add_button = PushButton('新增记录', self)
        setCustomStyleSheet(self.add_button, ADD_BUTTON_STYLE, ADD_BUTTON_STYLE)
        self.add_button.clicked.connect(self.add_condition_and_record_info)
        #【修改】按钮
        self.edit_button = PushButton('修改记录', self)
        setCustomStyleSheet(self.edit_button, UPDATE_BUTTON_STYLE, UPDATE_BUTTON_STYLE)
        #self.edit_button.setEnabled(False)
        self.edit_button.clicked.connect(self.edit_condition_or_record_info)
        #【删除】按钮
        self.delete_button=PushButton('删除',self)
        setCustomStyleSheet(self.delete_button,DELETE_BUTTON_STYLE,DELETE_BUTTON_STYLE)
        #self.delete_button.setEnabled(False)
        self.delete_button.clicked.connect(self.delete_condition_and_record_info)
        #【清除】按钮
        self.menu = RoundMenu(parent=self)
        erase_all_action = Action(FIF.ERASE_TOOL, '清除所有输入')
        erase_condition_action = Action(FIF.ERASE_TOOL, '仅清除条件')
        erase_record_action = Action(FIF.ERASE_TOOL, '仅清除记录')
        self.menu.addAction(erase_all_action)
        self.menu.addAction(erase_condition_action)
        self.menu.addAction(erase_record_action)
        self.erase_button = PrimaryDropDownPushButton(FIF.ERASE_TOOL, '清除')
        self.erase_button.setMenu(self.menu)

        card_hboxlayout.addWidget(self.add_button)
        card_hboxlayout.addWidget(self.edit_button)
        card_hboxlayout.addWidget(self.erase_button)
        card_hboxlayout.addStretch(1)
        card_hboxlayout.addWidget(self.delete_button)

        #在card2_hboxlayout中添加并设置控件
        #【保存】按钮
        self.save_button = PushButton('保存', self)
        setCustomStyleSheet(self.save_button, UPDATE_BUTTON_STYLE, UPDATE_BUTTON_STYLE)
        self.save_button.setEnabled(False)
        self.save_button.clicked.connect(self.modified_and_save)
        #【取消】按钮
        self.cancel_button=PushButton('取消',self)
        setCustomStyleSheet(self.cancel_button,DELETE_BUTTON_STYLE,DELETE_BUTTON_STYLE)
        self.cancel_button.setEnabled(False)
        self.cancel_button.clicked.connect(self.cancel_save)

        card2_hboxlayout.addStretch(1)
        card2_hboxlayout.addWidget(self.save_button)
        card2_hboxlayout.addWidget(self.cancel_button)

        # ======创建表格======
        self.table_widget = TableWidget(self)
        self.table_widget.setEditTriggers(QTableWidget.NoEditTriggers)  # 设置表格不可编辑
        #创建表格选中单元格触发时间
        self.table_widget.selectionModel().selectionChanged.connect(self.on_table_selection_changed)
        self.table_widget.setBorderRadius(8)  # 设置圆角半径
        self.table_widget.setBorderVisible(True)  # 设置表格边框可见
        self.table_widget.setViewportMargins(0, 0, 20, 0)
        #self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        self.table_widget.setColumnCount(46)
        self.table_widget.setHorizontalHeaderLabels(
            ['点火开始时间', '点火模式', '母线电压', '母线电流', '阳极暂态电压', '阳极稳态电压', '贮供流量控制目标值',
             '开环初期阶段流量校正系数', '加热电流', '触持后加热电流', '触持电流', '励磁电流', '阳极电流上限值',
             '系统总功率上限', 'PID比例常数', '推力器固定启动时长', '点火结束除气时间', '阳极点火时长',
             '电磁阀驱动主/备', '点火条件备注', '示波器1图号', '示波器2图号', '流量调节时间', '92阶段流量', '加热时长',
             '加阳极-阳极浪涌电流', '加阳极-阳极电压最大值', '加阳极-触持电流最小值', '加阳极-母线电流浪涌',
             '阳极暂态电压', '加励磁-阳极浪涌电流', '加励磁-阳极电压最大值', '加励磁-阳极电压下探值',
             '加励磁-母线电流浪涌', '加励磁-母线电流下探', '稳态-阳极稳态电压', '稳态-阳极稳态电流', '稳态-母线电流',
             '稳态-阳极电流峰峰值', '稳态-母线电流峰峰值', '稳态-母线电压峰峰值', '稳态-触持电流峰峰值', '推力',
             '稳态阶段流量', '试验结论', '结论备注'])

        # 设置自定义表头格式
        # self.custom_ground_header=CustomGroundHeaderView(Qt.Orientation.Horizontal,self.table_widget)
        # self.table_widget.setHorizontalHeader(self.custom_ground_header)

        # ======创建一个栅格布局，用于对点火条件控件进行布局======
        condition_card_widget = CardWidget(self)
        condition_gridlayout = QGridLayout(condition_card_widget)
        self.ignition_time_input = TimePicker(self)  # 点火开始时间
        self.ignition_time_input.timeChanged.connect(self.on_time_change)
        self.ignition_mode_combo = ComboBox(self)  # 点火模式
        self.ignition_modes()
        self.ignition_mode_combo.setCurrentIndex(-1)
        self.ignition_mode_combo.setText('控制模式')
        self.busbar_voltage_input = LineEdit(self)  # 母线电压
        self.busbar_current_input = LineEdit(self)  # 母线电流
        self.transient_voltage_input = LineEdit(self)  # 阳极暂态电压
        self.steady_voltage_input = LineEdit(self)  # 阳极稳态电压
        self.fc_tgt_input = LineEdit(self)  # 贮供流量控制目标值
        self.ol_ifc_input = LineEdit(self)  # 开环初期阶段流量校正系数
        self.heating_current_input = LineEdit(self)  # 加热电流
        self.heating_current2_input = LineEdit(self)  # 触持后加热电流
        self.keep_alive_current_input = LineEdit(self)  # 触持电流
        self.excitation_current_input = LineEdit(self)  # 励磁电流
        self.anode_current_limit_input = LineEdit(self)  # 阳极电流上限值
        self.system_power_limit_input = LineEdit(self)  # 系统总功率上限
        self.pid_proportional_constant_input = LineEdit(self)  # PID比例常数
        self.thruster_duration_input = LineEdit(self)  # 推力器固定启动时长
        self.pi_cdt_input = LineEdit(self)  # 点火结束除气时间
        self.anode_duration_input = LineEdit(self)  # 阳极点火时长
        self.sv_mbs_input = LineEdit(self)  # 电磁阀驱动主/备
        self.condition_notes_input = LineEdit(self)  # 备注

        condition_fields = [
            ('点火开始时间:', self.ignition_time_input),
            ('点火模式:', self.ignition_mode_combo),
            ('母线电压:', self.busbar_voltage_input),
            ('母线电流:', self.busbar_current_input),
            ('阳极暂态电压:', self.transient_voltage_input),
            ('阳极稳态电压:', self.steady_voltage_input),
            ('贮供流量控制目标值:', self.fc_tgt_input),
            ('开环初期阶段流量校正系数:', self.ol_ifc_input),
            ('加热电流:', self.heating_current_input),
            ('触持后加热电流:', self.heating_current2_input),
            ('触持电流:', self.keep_alive_current_input),
            ('励磁电流:', self.excitation_current_input),
            ('阳极电流上限值:', self.anode_current_limit_input),
            ('系统总功率上限:', self.system_power_limit_input),
            ('PID比例常数:', self.pid_proportional_constant_input),
            ('推力器固定启动时长:', self.thruster_duration_input),
            ('点火结束除气时间:', self.pi_cdt_input),
            ('阳极点火时长:', self.anode_duration_input),
            ('电磁阀驱动主/备:', self.sv_mbs_input),
            ('备注:', self.condition_notes_input)

        ]

        condition_row = 0
        condition_col = 0
        max_condition_col = 5
        for conditon_text, condition_input in condition_fields:
            condition_label = StrongBodyLabel(conditon_text, self)
            condition_gridlayout.addWidget(condition_label, condition_row, condition_col * 2)
            condition_gridlayout.addWidget(condition_input, condition_row, condition_col * 2 + 1)
            condition_col += 1
            if condition_col >= max_condition_col:
                condition_col = 0
                condition_row += 1

        # ======创建一个栅格布局，用于对点火记录控件进行布局======
        self.record_card_widget = CardWidget(self)
        record_gridlayout = QGridLayout(self.record_card_widget)
        self.oscilloscope1_drawnumber_input = LineEdit(self)  # 示波器1图号
        self.oscilloscope2_drawnumber_input = LineEdit(self)  # 示波器2图号
        self.flow_adjustment_time_input = LineEdit(self)  # 流量调节时间
        self.heat_traffic_input = LineEdit(self)  # 92阶段流量
        self.heat_duration_input = LineEdit(self)  # 加热时长
        self.p1_anode_surge_current_input = LineEdit(self)  # 加阳极-阳极浪涌电流
        self.p1_maximum_anode_voltage_input = LineEdit(self)  # 加阳极-阳极电压最大值
        self.p1_minimum_holding_current_input = LineEdit(self)  # 加阳极-触持电流最小值
        self.p1_bus_current_surge_input = LineEdit(self)  # 加阳极-母线电流浪涌
        self.p2_anode_transient_voltage_input = LineEdit(self)  # 阳极暂态电压
        self.p3_anode_surge_current_input = LineEdit(self)  # 加励磁-阳极浪涌电流
        self.p3_maximum_anode_voltage_input = LineEdit(self)  # 加励磁-阳极电压最大值
        self.p3_minimum_anode_voltage_input = LineEdit(self)  # 加励磁-阳极电压下探值
        self.p3_bus_current_surge_input = LineEdit(self)  # 加励磁-母线电流浪涌
        self.p3_minimum_bus_current_input = LineEdit(self)  # 加励磁-母线电流下探
        self.p4_transient_voltage_input = LineEdit(self)  # 稳态-阳极稳态电压
        self.p4_anode_steady_current_input = LineEdit(self)  # 稳态-阳极稳态电流
        self.p4_bus_current_input = LineEdit(self)  # 稳态-母线电流
        self.p4_pp_anode_current_input = LineEdit(self)  # 稳态-阳极电流峰峰值
        self.p4_pp_bus_current_input = LineEdit(self)  # 稳态-母线电流峰峰值
        self.p4_pp_busbar_voltage_input = LineEdit(self)  # 稳态-母线电压峰峰值
        self.p4_pp_keep_alive_current_input = LineEdit(self)  # 稳态-触持电流峰峰值
        self.thrust_input = LineEdit(self)  # 推力
        self.p4_traffic_input = LineEdit(self)  # 稳态阶段流量
        self.test_conclusion_input = LineEdit(self)  # 试验结论
        self.record_notes_input = LineEdit(self)  # 备注

        record_fields = [
            ('示波器1图号:', self.oscilloscope1_drawnumber_input),
            ('示波器2图号:', self.oscilloscope2_drawnumber_input),
            ('流量调节时间:', self.flow_adjustment_time_input),
            ('92阶段流量:', self.heat_traffic_input),
            ('加热时长:', self.heat_duration_input),
            ('加阳极-阳极浪涌电流:', self.p1_anode_surge_current_input),
            ('加阳极-阳极电压最大值:', self.p1_maximum_anode_voltage_input),
            ('加阳极-触持电流最小值:', self.p1_minimum_holding_current_input),
            ('加阳极-母线电流浪涌:', self.p1_bus_current_surge_input),
            ('阳极暂态电压:', self.p2_anode_transient_voltage_input),
            ('加励磁-阳极浪涌电流:', self.p3_anode_surge_current_input),
            ('加励磁-阳极电压最大值:', self.p3_maximum_anode_voltage_input),
            ('加励磁-阳极电压下探值:', self.p3_minimum_anode_voltage_input),
            ('加励磁-母线电流浪涌:', self.p3_bus_current_surge_input),
            ('加励磁-母线电流下探:', self.p3_minimum_bus_current_input),
            ('稳态-阳极稳态电压:', self.p4_transient_voltage_input),
            ('稳态-阳极稳态电流:', self.p4_anode_steady_current_input),
            ('稳态-母线电流:', self.p4_bus_current_input),
            ('稳态-阳极电流峰峰值:', self.p4_pp_anode_current_input),
            ('稳态-母线电流峰峰值:', self.p4_pp_bus_current_input),
            ('稳态-母线电压峰峰值:', self.p4_pp_busbar_voltage_input),
            ('稳态-触持电流峰峰值:', self.p4_pp_keep_alive_current_input),
            ('推力:', self.thrust_input),
            ('稳态阶段流量:', self.p4_traffic_input),
            ('试验结论:', self.test_conclusion_input),
            ('备注:', self.record_notes_input)
        ]
        record_row = 0
        record_col = 0
        max_record_col = 5
        for record_text, record_input in record_fields:
            record_label = StrongBodyLabel(record_text)
            record_gridlayout.addWidget(record_label, record_row, record_col * 2)
            record_gridlayout.addWidget(record_input, record_row, record_col * 2 + 1)
            record_col += 1
            if record_col >= max_record_col:
                record_col = 0
                record_row += 1

        layout.addWidget(self.table_widget)
        layout.addWidget(card_widget)
        layout.addWidget(condition_card_widget)
        layout.addWidget(self.record_card_widget)
        layout.addWidget(card2_widget)


    # 获取并给【点火模式】控件赋值
    def ignition_modes(self):
        with IgnitionModeDB() as db:
            modes = db.fetch_modes()
        self.ignition_mode_combo.clear()
        for i in modes:
            ignition_mode = i['ignition_mode']
            self.ignition_mode_combo.addItem(ignition_mode)

    def _vertify_information(self,infos):
        '''对输入参数的数据类型进行校验'''
        error_infos=[]
        for num,(key,value) in enumerate(infos.items()):
            if key in ['sv_mbs','condition_notes','project_id','ignition_time']:
                continue
            if key=='ignition_mode_id':
                if value==-1:
                    error_infos.append('请选择点火模式')
            if not is_double(value):
                error_infos.append(f'{key}仅支持浮点型数据/不填')
        return error_infos


    def add_condition_and_record_info(self):
        '''【添加】点火条件和记录'''
        if self.save_button.isEnabled():
            InfoBar.warning(title='警告', content='请先保存/取消当前数据', duration=3000, parent=self)
            return
        self.table_widget.clearSelection() #清空界面高亮（可写可不写）
        self.table_widget.setCurrentCell(-1,-1) #把当前焦点单元格设为“无”
        self.table_widget.setSelectionMode(QAbstractItemView.NoSelection) #禁止选中行
        self.edit_button.setEnabled(False)
        self.save_button.setEnabled(True)
        self.cancel_button.setEnabled(True)
        self.clear_record()




    def edit_condition_or_record_info(self):
        if self.save_button.isEnabled():
            InfoBar.warning(title='警告', content='请先保存/取消当前数据', duration=3000, parent=self)
            return
        selected_row=self.table_widget.currentRow() #获取当前选中行
        #判断是否有选中行，如果有的话进行编辑操作，如果没有选中的话，提示未选中行
        if selected_row==-1:
            InfoBar.warning(title='未选择目标',content='请选择要操作的行',duration=3000,parent=self)
            return
        self.backfill_data(selected_row) #获取当前行数据并回填输入框
        InfoBar.success(title='数据回填成功', content='数据回填成功，请修改后点击【保存】', duration=3000, parent=self)
        self.table_widget.setSelectionMode(QAbstractItemView.NoSelection) #禁止选中行
        self.add_button.setEnabled(False)
        self.save_button.setEnabled(True)
        self.cancel_button.setEnabled(True)

    def delete_condition_and_record_info(self):
        selected_row=self.table_widget.currentRow()
        # 判断是否有选中行，如果有的话进行删除操作，如果没有选中的话，提示未选中行
        if selected_row == -1:
            InfoBar.warning(title='未选择目标', content='请选择要删除的行', duration=3000, parent=self)
            return
        selected_row_data = self.condition_and_record[selected_row]
        selected_condition_id = selected_row_data['condition_id']
        w=MessageBox(title='删除确认',content=f'是否确认要删除条件ID为{selected_condition_id}的数据？',parent=self)
        w.yesButton.setText('是')
        w.cancelButton.setText('否')
        if w.exec():
            with IgnitionRecordDB() as recdb:
                recdb.delete_record(selected_condition_id)
            with IgnitionConditionDB() as condb:
                condb.delete_condition(selected_condition_id)
            self.load_data()
            self.populate_table()
        self.table_widget.setCurrentCell(-1,-1)





    def on_table_selection_changed(self,selected,deselected):
        '''定义当选中表格中行时触发的效果'''
        #如果是取消选中行，则跳过；如果选中了新行，则继续往下走
        '''if not selected:
            return
        #如果【保存】按钮是启用状态，则代表正在编辑，提示必须先保存，禁止切换选中
        if self.save_button.isEnabled():
            self.table_widget.setCurrentItem(None)
            #self.table_widget.selectionModel().select(selected,self.table_widget.selectionModel().SelectionFlag.Deselect)
            #self.table_widget.selectionModel().select(deselected,self.table_widget.selectionModel().SelectionFlag.Select)
            InfoBar.warning(title='警告',content='请先完成当前数据的修改并保存',duration=3000,parent=self)
            return
        #如果当前有选中行，则启用修改按钮；否则禁用修改按钮
        whether_selection=self.table_widget.currentRow()!=-1
        self.edit_button.setEnabled(whether_selection)'''
        selected_row = self.table_widget.currentRow()  # 获取当前选中行
        # 获取当前行数据并回填输入框
        self.backfill_data(selected_row)
        if not selected:
            return




    #定义点击【保存】按钮后的逻辑
    def modified_and_save(self):
        if self.add_button.isEnabled() and not self.edit_button.isEnabled():
            condition_infos = self.get_condition_infos()
            errors = self._vertify_information(condition_infos)
            if not errors:
                w_add = MessageBox(title='新增确认', content='是否确认要新增一条数据？', parent=self)
                if w_add.exec():
                    try:
                        with IgnitionConditionDB() as db:
                            condition_id = db.add_ignition_condition(condition_infos)
                        record_infos = self.get_record_infos(condition_id)
                        with IgnitionRecordDB() as db:
                            db.add_ignition_record(record_infos)
                        self.load_data()
                        self.populate_table()
                        self.clear_record()
                        self.edit_button.setEnabled(True)
                        self.save_button.setEnabled(False)
                        self.cancel_button.setEnabled(False)
                        self.table_widget.setSelectionMode(QAbstractItemView.SingleSelection)  # 恢复单行选中功能
                        InfoBar.success(title='保存数据成功', content=f'成功保存条件ID为{condition_id}的数据',
                                        duration=3000,
                                        parent=self)
                    except Exception as e:
                        InfoBar.error(title='保存数据失败', content=str(e), duration=3000, parent=self)
            else:
                error_message = '\n'.join(errors)
                InfoBar.error(title='输入有误', content=error_message, duration=3000, parent=self)
        if not self.add_button.isEnabled() and self.edit_button.isEnabled():
            try:
                # start=time.time()#时间性能监控，开始时间
                condition_infos = self.get_condition_infos()
                # print(f'取条件数据用时：{time.time()-start:.3f}s')
                record_infos = self.get_record_infos(self.selected_condition_id)
                # print(f'取记录数据用时：{time.time()-start:.3f}s')
                with IgnitionConditionDB() as condb:
                    condb.update_condition(condition_infos, self.selected_condition_id)
                # print(f'更新条件数据用时：{time.time()-start:.3f}s')
                with IgnitionRecordDB() as recdb:
                    recdb.update_record(record_infos, self.selected_condition_id)
                # print(f'更新记录数据用时：{time.time()-start:.3f}s')
                self.load_data()
                self.populate_table()
                self.clear_record()
                self.table_widget.setSelectionMode(QAbstractItemView.SingleSelection) #恢复单行可选状态
                self.table_widget.clearSelection()  # 清除高亮
                self.table_widget.setCurrentCell(-1, -1)  # 设定焦点位置
                self.add_button.setEnabled(True)
                self.save_button.setEnabled(False)
                self.cancel_button.setEnabled(False)
                InfoBar.success(title='修改成功', content='成功修改并保存数据', duration=3000, parent=self)
            except Exception as e:
                InfoBar.error(title='修改失败', content=str(e), duration=3000, parent=self)


    def cancel_save(self):
        '''取消按钮逻辑'''
        #当点击取消时，弹出二次确认窗口
        w=MessageBox(title='取消确认',content='是否确定要取消本次操作？',parent=self)
        if w.exec():
            InfoBar.success(title='确认取消',content='已成功取消本次操作',duration=3000,parent=self)
            self.add_button.setEnabled(True)
            self.edit_button.setEnabled(True)
            self.save_button.setEnabled(False)
            self.cancel_button.setEnabled(False)
            self.clear_record() # 输入的记录内容清除
            self.table_widget.setSelectionMode(QAbstractItemView.SingleSelection)  # 恢复单行选中功能
            self.table_widget.clearSelection()  # 清除高亮
            self.table_widget.setCurrentCell(-1, -1)  # 设定焦点位置


    #获取当前选中行的数据，并回填输入框
    def backfill_data(self,selected_row):
        row_data:dict = self.condition_and_record[selected_row]  # 从内存列表中取出完整数据

        # 对数据库中的时间格式进行转换（由timedelta转为QTime）
        time_val = row_data['ignition_time']
        if hasattr(time_val, 'seconds'):
            total_sec = time_val.seconds
            h = total_sec // 3600
            m = (total_sec % 3600) // 60
            s = total_sec % 60
            self.q_time = QTime(h, m, s)
        else:
            self.q_time = QTime.fromString(str(time_val), 'HH:mm:ss')

        # 回填数据到输入框
        self.selected_condition_id = row_data['condition_id']
        self.ignition_time_input.setTime(self.q_time)
        self.ignition_mode_combo.setCurrentText(str(row_data['ignition_mode']))
        self.busbar_voltage_input.setText(
            str(row_data['busbar_voltage']) if row_data['busbar_voltage'] is not None else '')
        self.busbar_current_input.setText(
            str(row_data['busbar_current']) if row_data['busbar_current'] is not None else '')
        self.transient_voltage_input.setText(
            str(row_data['transient_voltage']) if row_data['transient_voltage'] is not None else '')
        self.steady_voltage_input.setText(
            str(row_data['steady_voltage']) if row_data['steady_voltage'] is not None else '')
        self.fc_tgt_input.setText(str(row_data['fc_tgt']) if row_data['fc_tgt'] is not None else '')
        self.ol_ifc_input.setText(str(row_data['ol_ifc']) if row_data['ol_ifc'] is not None else '')
        self.heating_current_input.setText(
            str(row_data['heating_current']) if row_data['heating_current'] is not None else '')
        self.heating_current2_input.setText(
            str(row_data['heating_current2']) if row_data['heating_current2'] is not None else '')
        self.keep_alive_current_input.setText(
            str(row_data['keep_alive_current']) if row_data['keep_alive_current'] is not None else '')
        self.excitation_current_input.setText(
            str(row_data['excitation_current']) if row_data['excitation_current'] is not None else '')
        self.anode_current_limit_input.setText(
            str(row_data['anode_current_limit']) if row_data['anode_current_limit'] is not None else '')
        self.system_power_limit_input.setText(
            str(row_data['system_power_limit']) if row_data['system_power_limit'] is not None else '')
        self.pid_proportional_constant_input.setText(
            str(row_data['pid_proportional_constant']) if row_data['pid_proportional_constant'] is not None else '')
        self.thruster_duration_input.setText(
            str(row_data['thruster_duration']) if row_data['thruster_duration'] is not None else '')
        self.pi_cdt_input.setText(str(row_data['pi_cdt']) if row_data['pi_cdt'] is not None else '')
        self.anode_duration_input.setText(
            str(row_data['anode_duration']) if row_data['anode_duration'] is not None else '')
        self.sv_mbs_input.setText(row_data['sv_mbs'])
        self.condition_notes_input.setText(row_data['condition_notes'])
        self.oscilloscope1_drawnumber_input.setText(row_data['oscilloscope1_drawnumber'])
        self.oscilloscope2_drawnumber_input.setText(row_data['oscilloscope2_drawnumber'])
        self.flow_adjustment_time_input.setText(row_data['flow_adjustment_time'])
        self.heat_traffic_input.setText(row_data['heat_traffic'])
        self.heat_duration_input.setText(row_data['heat_duration'])
        self.p1_anode_surge_current_input.setText(row_data['p1_anode_surge_current'])
        self.p1_maximum_anode_voltage_input.setText(row_data['p1_maximum_anode_voltage'])
        self.p1_minimum_holding_current_input.setText(row_data['p1_minimum_holding_current'])
        self.p1_bus_current_surge_input.setText(row_data['p1_bus_current_surge'])
        self.p2_anode_transient_voltage_input.setText(row_data['p2_anode_transient_voltage'])
        self.p3_anode_surge_current_input.setText(row_data['p3_anode_surge_current'])
        self.p3_maximum_anode_voltage_input.setText(row_data['p3_maximum_anode_voltage'])
        self.p3_minimum_anode_voltage_input.setText(row_data['p3_minimum_anode_voltage'])
        self.p3_bus_current_surge_input.setText(row_data['p3_bus_current_surge'])
        self.p3_minimum_bus_current_input.setText(row_data['p3_minimum_bus_current'])
        self.p4_transient_voltage_input.setText(row_data['p4_transient_voltage'])
        self.p4_anode_steady_current_input.setText(row_data['p4_anode_steady_current'])
        self.p4_bus_current_input.setText(row_data['p4_bus_current'])
        self.p4_pp_anode_current_input.setText(row_data['p4_pp_anode_current'])
        self.p4_pp_bus_current_input.setText(row_data['p4_pp_bus_current'])
        self.p4_pp_busbar_voltage_input.setText(row_data['p4_pp_busbar_voltage'])
        self.p4_pp_keep_alive_current_input.setText(row_data['p4_pp_keep_alive_current'])
        self.thrust_input.setText(row_data['thrust'])
        self.p4_traffic_input.setText(row_data['p4_traffic'])
        self.test_conclusion_input.setText(row_data['test_conclusion'])
        self.record_notes_input.setText(row_data['record_notes'])




    # 获取点火条件输入框中的值
    def get_condition_infos(self):
        return {
            'project_id': self.project_id,
            'ignition_time': self.ignition_time_input.time.toString('HH:mm'),
            'ignition_mode_id': self.get_mode_id(),
            'busbar_voltage': to_none(self.busbar_voltage_input.text().strip()),
            'busbar_current': to_none(self.busbar_current_input.text().strip()),
            'transient_voltage': to_none(self.transient_voltage_input.text().strip()),
            'steady_voltage': to_none(self.steady_voltage_input.text().strip()),
            'fc_tgt': to_none(self.fc_tgt_input.text().strip()),
            'ol_ifc': to_none(self.ol_ifc_input.text().strip()),
            'heating_current': to_none(self.heating_current_input.text().strip()),
            'heating_current2': to_none(self.heating_current2_input.text().strip()),
            'keep_alive_current': to_none(self.keep_alive_current_input.text().strip()),
            'excitation_current': to_none(self.excitation_current_input.text().strip()),
            'anode_current_limit': to_none(self.anode_current_limit_input.text().strip()),
            'system_power_limit': to_none(self.system_power_limit_input.text().strip()),
            'pid_proportional_constant': to_none(self.pid_proportional_constant_input.text().strip()),
            'thruster_duration': to_none(self.thruster_duration_input.text().strip()),
            'pi_cdt': to_none(self.pi_cdt_input.text().strip()),
            'anode_duration': to_none(self.anode_duration_input.text().strip()),
            'sv_mbs': self.sv_mbs_input.text().strip(),
            'condition_notes': self.condition_notes_input.text().strip()
        }

    # 获取点火记录输入框中的值
    def get_record_infos(self, condition_id=None):
        return {
            'condition_id': condition_id,
            'oscilloscope1_drawnumber': self.oscilloscope1_drawnumber_input.text().strip(),
            'oscilloscope2_drawnumber': self.oscilloscope2_drawnumber_input.text().strip(),
            'flow_adjustment_time': self.flow_adjustment_time_input.text().strip(),
            'heat_traffic': self.heat_traffic_input.text().strip(),
            'heat_duration': self.heat_duration_input.text().strip(),
            'p1_anode_surge_current': self.p1_anode_surge_current_input.text().strip(),
            'p1_maximum_anode_voltage': self.p1_maximum_anode_voltage_input.text().strip(),
            'p1_minimum_holding_current': self.p1_minimum_holding_current_input.text().strip(),
            'p1_bus_current_surge': self.p1_bus_current_surge_input.text().strip(),
            'p2_anode_transient_voltage': self.p2_anode_transient_voltage_input.text().strip(),
            'p3_anode_surge_current': self.p3_anode_surge_current_input.text().strip(),
            'p3_maximum_anode_voltage': self.p3_maximum_anode_voltage_input.text().strip(),
            'p3_minimum_anode_voltage': self.p3_minimum_anode_voltage_input.text().strip(),
            'p3_bus_current_surge': self.p3_bus_current_surge_input.text().strip(),
            'p3_minimum_bus_current': self.p3_minimum_bus_current_input.text().strip(),
            'p4_transient_voltage': self.p4_transient_voltage_input.text().strip(),
            'p4_anode_steady_current': self.p4_anode_steady_current_input.text().strip(),
            'p4_bus_current': self.p4_bus_current_input.text().strip(),
            'p4_pp_anode_current': self.p4_pp_anode_current_input.text().strip(),
            'p4_pp_bus_current': self.p4_pp_bus_current_input.text().strip(),
            'p4_pp_busbar_voltage': self.p4_pp_busbar_voltage_input.text().strip(),
            'p4_pp_keep_alive_current': self.p4_pp_keep_alive_current_input.text().strip(),
            'thrust': self.thrust_input.text().strip(),
            'p4_traffic': self.p4_traffic_input.text().strip(),
            'test_conclusion': self.test_conclusion_input.text().strip(),
            'record_notes': self.record_notes_input.text().strip()
        }

    # 定义时间改变时的触发效果
    def on_time_change(self, time: QTime):
        time_str = time.toString('HH:mm')
        #self.time_str = time_str

    # 获取点火模式对应的ID
    def get_mode_id(self):
        with IgnitionModeDB() as db:
            ignition_mode = self.ignition_mode_combo.text()
            self.ignition_mode_id = db.fetch_mode_id(ignition_mode)
            print(self.ignition_mode_id)
            return self.ignition_mode_id

    # 从数据表中获取点火条件+点火记录
    @timer
    def load_data(self):
        with IgnitionConditionDB() as db:
            self.condition_and_record = db.get_condition_and_record(self.project_id) or []

    # 展示表格数据
    @timer
    def populate_table(self):
        self.table_widget.setUpdatesEnabled(False) #开始渲染前，暂停表格刷新
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed) #开始setItem前，禁用ResizeToContents
        try:
            self.table_widget.setRowCount(len(self.condition_and_record))
            for row, condition_and_record_info in enumerate(self.condition_and_record):
                self.setup_table_row(row, condition_and_record_info)
        finally:
            self.table_widget.setUpdatesEnabled(True) #渲染完成后，再开启刷新
            self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)



    def setup_table_row(self, row, condition_and_record_info):
        '''往表格的单元格中放参数'''
        for col, key in enumerate(
                ['ignition_time', 'ignition_mode', 'busbar_voltage', 'busbar_current',
                 'transient_voltage', 'steady_voltage', 'fc_tgt', 'ol_ifc', 'heating_current', 'heating_current2',
                 'keep_alive_current', 'excitation_current', 'anode_current_limit', 'system_power_limit',
                 'pid_proportional_constant', 'thruster_duration', 'pi_cdt', 'anode_duration', 'sv_mbs',
                 'condition_notes', 'oscilloscope1_drawnumber', 'oscilloscope2_drawnumber', 'flow_adjustment_time',
                 'heat_traffic', 'heat_duration', 'p1_anode_surge_current', 'p1_maximum_anode_voltage',
                 'p1_minimum_holding_current', 'p1_bus_current_surge', 'p2_anode_transient_voltage',
                 'p3_anode_surge_current', 'p3_maximum_anode_voltage', 'p3_minimum_anode_voltage',
                 'p3_bus_current_surge', 'p3_minimum_bus_current', 'p4_transient_voltage', 'p4_anode_steady_current',
                 'p4_bus_current', 'p4_pp_anode_current', 'p4_pp_bus_current', 'p4_pp_busbar_voltage',
                 'p4_pp_keep_alive_current', 'thrust','p4_traffic','test_conclusion','record_notes']):
            value=condition_and_record_info.get(key,'')
            if value is None:
                value=''
            item=QTableWidgetItem(str(value))
            self.table_widget.setItem(row,col,item)

    #定义一个清空record记录输入框中参数的方法
    def clear_record(self):
        layout=self.record_card_widget.layout()
        for i in range(layout.count()):
            item=layout.itemAt(i)
            if item:
                widget=item.widget()
                if isinstance(widget,LineEdit):
                    widget.clear()







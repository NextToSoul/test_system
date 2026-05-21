from PySide6.QtCore import QDate
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QGridLayout
from qfluentwidgets import MessageBoxBase, LineEdit, ComboBox, FastCalendarPicker, StrongBodyLabel, SubtitleLabel, \
    InfoBar, InfoBarPosition

from database.item_db import itemDB
from database.ppcu_db import ppcuDB
from database.thruster_db import thrusterDB
from database.feedsystem_db import feedsystemDB

class BaseProjectDialog(MessageBoxBase):
    def __init__(self,title,parent=None):
        super().__init__(parent)
        self.title=title
        self.setup_ui()

    def setup_ui(self):
        self.titalLabel=SubtitleLabel(self.title,self)
        self.viewLayout.addWidget(self.titalLabel)
        #创建栅格布局
        grid_layout=QGridLayout()
        self.viewLayout.addLayout(grid_layout)#将栅格布局嵌套进MessageBoxBase默认的垂直布局里

        #创建字段
        #self.project_id_input=LineEdit(self)
        self.project_name_input=LineEdit(self)
        self.ppcu_number_combo=ComboBox(self)
        self.ppcu_nums()
        self.ppcu_number_combo.setCurrentIndex(-1)
        self.ppcu_number_combo.setText('请选择PPCU编号')
        self.thruster_number_combo=ComboBox(self)
        self.thruster_nums()
        self.thruster_number_combo.setCurrentIndex(-1)
        self.thruster_number_combo.setText('请选择推力器编号')
        self.feedsystem_number_combo=ComboBox(self)
        self.feedsystem_nums()
        self.feedsystem_number_combo.setCurrentIndex(-1)
        self.feedsystem_number_combo.setText('请选择贮供编号')
        self.working_fluid_combo=ComboBox(self)
        self.working_fluid_combo.addItems(['氪气','氙气'])
        self.working_fluid_combo.setCurrentIndex(-1)
        self.working_fluid_combo.setText('请选择工质')
        self.sw_version_input=LineEdit(self)#版本号
        self.picker=FastCalendarPicker(self)
        self.picker.setText('请选择日期')
        self.picker.dateChanged.connect(self.on_date_change)
        self.ignition_location_input=LineEdit(self)

        #以列表+元组的形式，添加字段到网格布局
        fields=[
            #('项目ID:',self.project_id_input),
            ('项目名称:',self.project_name_input),
            ('PPCU编号:',self.ppcu_number_combo),
            ('推力器编号:',self.thruster_number_combo),
            ('贮供编号:',self.feedsystem_number_combo),
            ('工质:',self.working_fluid_combo),
            ('软件版本号:',self.sw_version_input),
            ('点火日期:',self.picker),
            ('点火地点:',self.ignition_location_input)
        ]
        for row,(label_text,widget) in enumerate(fields):
            label=StrongBodyLabel(label_text,self)#设置label加粗样式
            grid_layout.addWidget(label,row,0)
            grid_layout.addWidget(widget,row,1)
        #设置列拉伸
        grid_layout.setColumnStretch(1,1)
        #设置左对齐
        grid_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.yesButton.setText('确定')
        self.cancelButton.setText('取消')
        #设置输入框宽度
        for widget in [self.project_name_input,self.ppcu_number_combo,self.thruster_number_combo,self.feedsystem_number_combo,self.working_fluid_combo,self.sw_version_input,self.picker,self.ignition_location_input]:
            widget.setMinimumWidth(200)

        #将焦点定位到项目名称输入框
        self.project_name_input.setFocus()
        #确保确定按钮不会自动对焦
        self.yesButton.setDefault(False)
        self.yesButton.setAutoDefault(False)

    #数据验证方法
    def _confirm_data(self):
        errors=[]
        if not self.project_name_input.text().strip():
            errors.append('请输入项目名称')
        if self.ppcu_number_combo.currentIndex()==-1:
            errors.append('请选择PPCU编号')
        if self.thruster_number_combo.currentIndex()==-1:
            errors.append('请选择推力器编号')
        if self.feedsystem_number_combo.currentIndex()==-1:
            errors.append('请选择贮供编号')
        if self.working_fluid_combo.currentIndex()==-1:
            errors.append('请选择工质')
        if not self.sw_version_input.text().strip():
            errors.append('请输入版本号')
        if self.picker.date.isNull():
            errors.append('请选择日期')
        if not self.ignition_location_input.text().strip():
            errors.append('请输入点火地点')
        return errors

    def accept(self):
        #对填入的数据进行验证
        errors=self._confirm_data()
        if errors:
            error_message='\n'.join(errors)
            InfoBar.error(
                title='输入有误',         #提示标题
                content=error_message,  #提示的内容
                orient=Qt.Horizontal,   #水平显示
                isClosable=True,        #显示关闭按钮
                position=InfoBarPosition.BOTTOM_RIGHT,#弹出位置，右下角
                parent=self,            #父窗口
                duration=3000           #持续时间
            )
            return
        #验证通过，接受并关闭对话框
        super().accept()




    def get_project_info(self):
        '''获取项目信息'''
        return {
            'project_name': self.project_name_input.text().strip(),
            'ppcu_id':self.get_ppcuID(),
            'thruster_id':self.get_thrusterID(),
            'feedsystem_id':self.get_feedsystemID(),
            'working_fluid':self.working_fluid_combo.currentText(),
            'sw_version':self.sw_version_input.text().strip(),
            'ignition_date':self.selected_date_str,
            'ignition_location':self.ignition_location_input.text().strip()
        }







    #设置日期改变触发时的连接
    def on_date_change(self,date:QDate):
        date_str=date.toString('yyyy-MM-dd')
        print(date_str)
        self.selected_date_str=date_str

    #获取PPCU编号所对应的ID
    def get_ppcuID(self):
        ppcu_number = self.ppcu_number_combo.currentText()
        with ppcuDB() as db:
            self.ppcu_id=db.fetch_ppcuID(ppcu_number)
            return self.ppcu_id

    #获取推力器编号所对应的ID
    def get_thrusterID(self):
        thruster_number=self.thruster_number_combo.currentText()
        with thrusterDB() as db:
            self.thruster_id=db.fetch_thrusterID(thruster_number)
            return self.thruster_id

    #获取贮供编号所对应的ID
    def get_feedsystemID(self):
        feedsystem_number=self.feedsystem_number_combo.currentText()
        with feedsystemDB() as db:
            self.feedsystem_id=db.fetch_feedsystemID(feedsystem_number)
            return self.feedsystem_id

    #获取ppcu的编号
    def ppcu_nums(self):
        with ppcuDB() as db:
            self.ppcus_dict=db.fetch_ppcus()

        #清空下拉框
        self.ppcu_number_combo.clear()
        #循环添加
        for i,j in enumerate(self.ppcus_dict):
            ppcu_num=j['ppcu_number']
            self.ppcu_number_combo.addItem(ppcu_num)

    #获取推力器编号
    def thruster_nums(self):
        with thrusterDB() as db:
            self.thrusters_dicct=db.fetch_thrusters()

        #清空下拉框
        self.thruster_number_combo.clear()
        #循环添加
        for i in self.thrusters_dicct:
            thruster_num=i['thruster_number']
            self.thruster_number_combo.addItem(thruster_num)

    #获取贮供编号
    def feedsystem_nums(self):
        with feedsystemDB() as db:
            self.feedsystems_dict=db.fetch_feedsystems()

        #清空下拉框
        self.feedsystem_number_combo.clear()
        #循环添加
        for i in self.feedsystems_dict:
            feedsystem_num=i['feedsystem_number']
            self.feedsystem_number_combo.addItem(feedsystem_num)

class AddProjectDialog(BaseProjectDialog):
    def __init__(self,parent=None):
        super().__init__('新建项目',parent)
        self.project_id=None
        self.yesButton.setText('添加')

class UpdateProjectDialog(BaseProjectDialog):
    def __init__(self,project_id,parent=None):
        super().__init__('编辑项目',parent)
        self.project_id=project_id
        self.yesButton.setText('更新')

    #获取project_id所对应的项目信息,并填入对应的控件
    def set_project_info(self,info):
        self.project_name_input.setText(info['project_name'])
        self.ppcu_number_combo.setCurrentText(info['ppcu_number'])
        self.thruster_number_combo.setCurrentText(info['thruster_number'])
        self.feedsystem_number_combo.setCurrentText(info['feedsystem_number'])
        self.working_fluid_combo.setCurrentText(info['working_fluid'])
        self.sw_version_input.setText(info['sw_version'])
        self.picker.setDate(QDate(info['ignition_date']))
        self.ignition_location_input.setText(info['ignition_location'])





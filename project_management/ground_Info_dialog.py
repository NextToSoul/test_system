import sys

from qfluentwidgets import MessageBoxBase, SubtitleLabel, LineEdit, StrongBodyLabel,InfoBar
from PySide6.QtWidgets import QGridLayout, QApplication

from database.ground_info_db import GroundInfoDB
from utils.custom_function import is_double


class GroundInformationBox(MessageBoxBase):

    def __init__(self,project_id,parent=None):
        super().__init__(parent)
        #self.title=title
        self.project_id=project_id
        self.setup_ui()

    def setup_ui(self):
        self.title_label=SubtitleLabel('接地记录',self)
        self.viewLayout.addWidget(self.title_label)
        #创建栅格布局,并将栅格布局添加到viewlayout垂直布局中
        grid_layout=QGridLayout()
        self.viewLayout.addLayout(grid_layout)
        #创建字段
        self.project_id_le=LineEdit(self) #项目ID
        self.mc_sc_le=LineEdit(self) #大仓-小仓
        self.ppcu_coldplate_le=LineEdit(self) #PPCU-冷板
        self.ppcu_thruster_le=LineEdit(self) #PPCU-推力器
        self.ppcu_feedsystem_le=LineEdit(self) #PPCU-贮供
        self.busneg_feedsystem_le=LineEdit(self) #母线负-冷板
        self.oc_feedsystem_le=LineEdit(self) #OC负-冷板
        self.ppcu_mc_le=LineEdit(self) #PPCU-大仓MΩ
        self.ppcu_sc_le=LineEdit(self) #PPCU-小仓MΩ
        self.commgnd_feedsystem_le=LineEdit(self) #通讯地-冷板
        self.grounding_notes_le=LineEdit(self) #备注

        fields=[
            ('项目ID:',self.project_id_le),
            ('大仓-小仓:',self.mc_sc_le),
            ('PPCU-冷板:',self.ppcu_coldplate_le),
            ('PPCU-推力器:',self.ppcu_thruster_le),
            ('PPCU-贮供:',self.ppcu_feedsystem_le),
            ('母线负-冷板:',self.busneg_feedsystem_le),
            ('OC负-冷板:',self.oc_feedsystem_le),
            ('PPCU-大仓MΩ:',self.ppcu_mc_le),
            ('PPCU-小仓MΩ:',self.ppcu_sc_le),
            ('通讯地-冷板:',self.commgnd_feedsystem_le),
            ('备注:',self.grounding_notes_le)
        ]
        for row,(label_text,widget) in enumerate(fields):
            label=StrongBodyLabel(label_text,self)
            grid_layout.addWidget(label,row,0)
            grid_layout.addWidget(widget,row,1)


        self.yesButton.setText('保存')
        self.cancelButton.setText('取消')
        grid_layout.setColumnStretch(1,1)
        #设置输入框列宽
        for widget in [self.project_id_le,self.mc_sc_le,self.ppcu_coldplate_le,self.ppcu_thruster_le,self.ppcu_feedsystem_le,self.busneg_feedsystem_le,self.oc_feedsystem_le,self.ppcu_mc_le,self.ppcu_sc_le,self.commgnd_feedsystem_le,self.grounding_notes_le]:
            widget.setMinimumWidth(200)

        self.mc_sc_le.setFocus() #设置光标初始位置
        self.yesButton.setDefault(False)
        self.cancelButton.setDefault(False)

        self.project_id_le.setText(str(self.project_id)) #获取项目ID
        self.project_id_le.setReadOnly(True)
        #判断数据库中是否已经存在某Project_id的接地信息，如果存在，则将数据库中的接地信息赋值给dialog输入框；如果不存在则正常打开dialog即可
        with GroundInfoDB() as db:
            if db.fetchbool_projectid_to_ground(self.project_id):
                data=db.fetch_projectid_to_ground(self.project_id)
                self.mc_sc_le.setText(str(data['mc_sc']) if data['mc_sc'] is not None else "")
                self.ppcu_coldplate_le.setText(str(data['ppcu_coldplate']) if data['ppcu_coldplate'] is not None else "")
                self.ppcu_thruster_le.setText(str(data['ppcu_thruster']) if data['ppcu_thruster'] is not None else "")
                self.ppcu_feedsystem_le.setText(str(data['ppcu_feedsystem']) if data['ppcu_feedsystem'] is not None else "")
                self.busneg_feedsystem_le.setText(str(data['busneg_feedsystem']) if data['busneg_feedsystem'] is not None else "")
                self.oc_feedsystem_le.setText(str(data['oc_feedsystem']) if data['oc_feedsystem'] is not None else "")
                self.ppcu_mc_le.setText(str(data['ppcu_mc']) if data['ppcu_mc'] is not None else "")
                self.ppcu_sc_le.setText(str(data['ppcu_sc']) if data['ppcu_sc'] is not None else "")
                self.commgnd_feedsystem_le.setText(str(data['commgnd_feedsystem']) if data['commgnd_feedsystem'] is not None else "")
                self.grounding_notes_le.setText(str(data['grounding_notes']) if data['grounding_notes'] is not None else "")

    #获取输入框中的值
    def get_grounding_info(self):
        return {
            'project_id':self.project_id_le.text().strip(),
            'mc_sc':self.mc_sc_le.text().strip(),
            'ppcu_coldplate':self.ppcu_coldplate_le.text().strip(),
            'ppcu_thruster':self.ppcu_thruster_le.text().strip(),
            'ppcu_feedsystem':self.ppcu_feedsystem_le.text().strip(),
            'busneg_feedsystem':self.busneg_feedsystem_le.text().strip(),
            'oc_feedsystem':self.oc_feedsystem_le.text().strip(),
            'ppcu_mc':self.ppcu_mc_le.text().strip(),
            'ppcu_sc':self.ppcu_sc_le.text().strip(),
            'commgnd_feedsystem':self.commgnd_feedsystem_le.text().strip(),
            'grounding_notes':self.grounding_notes_le.text().strip()
        }

    #对输入框中的值进行判断
    def _verify_information(self):
        error_data=[]
        if not is_double(self.mc_sc_le.text().strip()):
            error_data.append('【大仓-小仓】仅支持浮点型数字')
        if not is_double(self.ppcu_coldplate_le.text().strip()):
            error_data.append('【PPCU-冷板】仅支持浮点型数字')
        if not is_double(self.ppcu_thruster_le.text().strip()):
            error_data.append('【PPCU-推力器】仅支持浮点型数字')
        if not is_double(self.ppcu_feedsystem_le.text().strip()):
            error_data.append('【PPCU-贮供】仅支持浮点型数字')
        if not is_double(self.busneg_feedsystem_le.text().strip()):
            error_data.append('【母线负-冷板】仅支持浮点型数字')
        if not is_double(self.oc_feedsystem_le.text().strip()):
            error_data.append('【OC负-冷板】仅支持浮点型数字')
        if not is_double(self.ppcu_mc_le.text().strip()):
            error_data.append('【PPCU-大仓MΩ】仅支持浮点型数字')
        if not is_double(self.ppcu_sc_le.text().strip()):
            error_data.append('【PPCU-小仓MΩ】仅支持浮点型数字')
        if not is_double(self.commgnd_feedsystem_le.text().strip()):
            error_data.append('【通讯地-冷板】仅支持浮点型数字')
        return error_data

    #通过accept去进行数据校验，如果验证通过，则保存，否则提示错误信息
    def accept(self):
        errors=self._verify_information()
        if errors:
            error_message='\n'.join(errors)
            InfoBar.error(title='输入有误',content=error_message,duration=3000,parent=self)
        else:
            super().accept()

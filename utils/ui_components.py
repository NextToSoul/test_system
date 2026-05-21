from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QPainter, QColor, QBrush
from PySide6.QtWidgets import QWidget, QHBoxLayout, QHeaderView, QCheckBox
from qfluentwidgets import PushButton, setCustomStyleSheet, ToolButton, PrimaryToolButton, TableWidget
from qfluentwidgets import FluentIcon as FIF

from utils.custom_button_style import UPDATE_BUTTON_STYLE, DELETE_BUTTON_STYLE
#from project_management.project_interface import ProjectInterface



#创建包含【编辑】、【删除】等ToolBotton控件的窗体
def create_operation_widget(edit_callback,import_callbak,export_callbak,delete_callback):
    widget=QWidget()
    layout=QHBoxLayout(widget)
    layout.setContentsMargins(0,0,0,0)
    edit_primary_toolbutton=PrimaryToolButton(FIF.EDIT,widget)
    edit_primary_toolbutton.clicked.connect(edit_callback)
    import_primary_toolbutton=PrimaryToolButton(FIF.UP,widget) #导入按钮
    import_primary_toolbutton.clicked.connect(import_callbak)
    export_primary_toolbutton=PrimaryToolButton(FIF.DOWNLOAD,widget) #导出按钮
    export_primary_toolbutton.clicked.connect(export_callbak)
    delete_primary_toolbutton=PrimaryToolButton(FIF.DELETE,widget)
    delete_primary_toolbutton.clicked.connect(delete_callback)
    layout.addWidget(edit_primary_toolbutton)
    layout.addWidget(import_primary_toolbutton)
    layout.addWidget(export_primary_toolbutton)
    layout.addWidget(delete_primary_toolbutton)
    return widget

#创建包含【接地情况】、【记录】等pushButton控件集合的窗体
def create_action_widget(condition_callback,record_callback):
    widget =QWidget()
    action_layout =QHBoxLayout(widget)
    action_layout.setContentsMargins(0 ,0 ,0 ,0  )  # 设置布局的上下左右边距
    conditionButton =PushButton('接地情况' ,widget)
    conditionButton.adjustSize()
    # self.updateButton.setFixedWidth(40)
    setCustomStyleSheet(conditionButton ,UPDATE_BUTTON_STYLE ,UPDATE_BUTTON_STYLE)
    conditionButton.clicked.connect(condition_callback)
    recordButton =PushButton('记录' ,widget)
    recordButton.adjustSize()
    setCustomStyleSheet(recordButton ,DELETE_BUTTON_STYLE ,DELETE_BUTTON_STYLE)
    recordButton.clicked.connect(record_callback)
    action_layout.addWidget(conditionButton)
    # action_layout.addWidget(self.importButton)
    # action_layout.addWidget(self.exportButton)
    action_layout.addWidget(recordButton)
    return widget

#这是通过创建QCheckBox实体来实现表头首列勾选框的方案，但会有勾选框闪烁，无法选中等bug
'''class CustomHeaderView(QHeaderView):
    def __init__(self,orientation,parent=None):
        super().__init__(orientation,parent)

        #允许点击表头
        self.setSectionsClickable(True)
        #创建一个checkBox
        self.checkbox=QCheckBox(self)
        #设置样式
        self.checkbox.setStyleSheet('margin-left:10')
        self.checkbox.stateChanged.connect(self.check_all)
        #设置列宽并确保表格铺满
        self.sectionResized.connect(self.adjust_column_widths)
        self.geometriesChanged.connect(self.adjust_column_widths)

    def adjust_column_widths(self):
        #获取总宽度
        total_width=self.width()
        #设置第一列的宽度
        first_column_width=50
        #设置【操作项】列的宽度
        second_column_width=150
        #设置最后一列宽度
        last_column_width=150
        self.setSectionResizeMode(0,QHeaderView.ResizeMode.Fixed)#设置第一列宽度固定
        self.resizeSection(0,first_column_width)
        self.setSectionResizeMode(1,QHeaderView.ResizeMode.Fixed)
        self.resizeSection(1,second_column_width)
        self.setSectionResizeMode(self.count()-1,QHeaderView.ResizeMode.Fixed)
        self.resizeSection(self.count()-1,last_column_width)
        #设置中间列为伸缩模式，平均分配剩余宽度
        for i in range(2,self.count()-1):
            self.setSectionResizeMode(i,QHeaderView.ResizeMode.Stretch)


    def paintSection(self, painter, rect, logicalIndex, /):
        painter.save()#保存画笔状态
        super().paintSection(painter,rect,logicalIndex)
        painter.restore()#恢复画笔状态

        if logicalIndex==0:
            self.checkbox.setGeometry(rect)#设置复选框为矩形
            self.checkbox.setVisible(True)
        else:
            self.checkbox.setVisible(False)

    def check_all(self,state):
        #获取表格对象
        table_widget=self.parent()
        for row in range(table_widget.rowCount()):
            checkbox=table_widget.cellWidget(row,0)
            if checkbox:
                checkbox.setCheckState(Qt.CheckState(state))'''

#这是通过自己手动绘制勾选框方式来实现表头首列勾选框的方案，这种方式就不会存在上面方案的bug
class CustomHeaderView(QHeaderView):
    def __init__(self,orientation,parent=None):
        super().__init__(orientation,parent)
        #设置表头列可以点击
        self.setSectionsClickable(True)

        #自己维护全选状态：0：未选中 1：半选 2：全选,设置初始化状态为未选中
        self.all_check_state=Qt.CheckState.Unchecked
        #监听布局自动列宽
        self.sectionResized.connect(self.adjust_column_widths)#当某列大小变化时。。。
        self.geometriesChanged.connect(self.adjust_column_widths)#当全局变化时。。。

    def adjust_column_widths(self):
        '''设置第0列、第1列、最后1列固定列宽，其余列拉伸'''
        col_cnt =self.count()
        if col_cnt<2:
            return
        #第0列列宽固定
        self.setSectionResizeMode(0,QHeaderView.ResizeMode.Fixed)
        self.resizeSection(0,50)
        #第1列列宽固定
        self.setSectionResizeMode(1,QHeaderView.ResizeMode.Fixed)
        self.resizeSection(1,100)
        #最后一列列宽固定
        last_idx=col_cnt-1
        self.setSectionResizeMode(last_idx,QHeaderView.ResizeMode.Fixed)
        self.resizeSection(last_idx,150)
        #其余列拉伸
        for i in range(2,last_idx):
            self.setSectionResizeMode(i,QHeaderView.ResizeMode.Stretch)

    # ========== 手绘勾选框、对勾 ==========
    def paintSection(self,painter, rect, logicalIndex):
        #绘制原生表头，文字、背景、分割线等完整保留
        super().paintSection(painter,rect,logicalIndex)
        #只在第0列绘制勾选框,遇到其他列直接跳过不进行设置
        if logicalIndex!=0:
            return
        #定义勾选框大小
        check_size =16
        #设置勾选框水平垂直居中
        x=rect.center().x()-check_size//2
        y=rect.center().y()-check_size//2
        #绘制勾选框
        check_rect=QRect(x,y,check_size,check_size)

        #绘制勾选框外框
        painter.save()
        painter.setRenderHints(QPainter.Antialiasing)
        painter.setPen(Qt.gray)#设置画笔属性
        painter.setBrush(QBrush(Qt.white))#设置填充颜色
        painter.drawRect(check_rect)

        #根据状态绘制对勾/灰色半选块
        if self.all_check_state==Qt.CheckState.Checked:
            #绘制对勾
            painter.setPen(QColor("#007aff"))
            painter.drawLine(check_rect.left()+3,check_rect.top()+8,check_rect.left()+7,check_rect.bottom()-3)
            painter.drawLine(check_rect.left()+7,check_rect.bottom()-3,check_rect.right()-3,check_rect.top()+4)
        elif self.all_check_state==Qt.CheckState.PartiallyChecked:
            check_rect.adjusted(2,2,-2,-2)#绘制一个缩进后的小矩形，作为半选状态图

        painter.restore()

    # ========== 点击表头0列 → 切换全选状态 ==========
    def mousePressEvent(self, event):
        """点击表头，判断是否点在第0列勾选框区域"""
        pos=event.pos()#获取鼠标点击位置的坐标
        click_col=self.logicalIndexAt(pos)#根据鼠标点击位置坐标获取列号

        if click_col==0:
        # 切换状态：未选 → 全选 → 未选 循环
            if self.all_check_state==Qt.CheckState.Unchecked:
                self.all_check_state=Qt.CheckState.Checked
            else:
                self.all_check_state=Qt.CheckState.Unchecked

            #执行全选/取消全选
            self.toggle_all_row_check()
            #刷新表头绘制
            self.update()
            return
        super().mousePressEvent(event)


    # ========== 同步表格所有列勾选框 ==========
    def toggle_all_row_check(self):
        table_widget=self.parent()
        if not table_widget:
            return
        target_state=self.all_check_state
        for row in range(table_widget.rowCount()):
            w=table_widget.cellWidget(row,0)
            if w and hasattr(w,'setCheckState'):
                w.setCheckState(target_state)

#自定义接地记录表的表头
class CustomGroundHeaderView(QHeaderView):
    def __init__(self,orientation,parent=None):
        super().__init__(orientation,parent)

        self.sectionResized.connect(self.adjust_columns_width)
        self.geometriesChanged.connect(self.adjust_columns_width)

    #定义当某列或者全局发生变化时，列宽的自适应样式
    def adjust_columns_width(self):
        col_count=self.count()

        #设置最后一列固定列宽
        last_col=col_count-1
        self.setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.resizeSection(last_col,150)
        self.setStretchLastSection(True)
        for i in range(0,last_col):
            self.setSectionResizeMode(i,QHeaderView.ResizeMode.ResizeToContents)






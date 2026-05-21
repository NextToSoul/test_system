BUTTON_STYLE='''
QpushButton{
    border:none;
    padding:5px 10px;
    font-family:'Segoe UI','Microsoft YaHei';
    font-size:14px;
    color:white;
    border-radius:5px;
}
QpushButton:hover{
    background-color:rgba(255,255,255,0.1);
}
QpushButton:pressed{
    background-color:rgba(255,255,255,0.2);
}

'''
#添加按钮
ADD_BUTTON_STYLE=BUTTON_STYLE+"""
QPushButton{
    background-color:#0d6efd;
}
QPushButton:hover{
    background-color:#0b5ed7;
}
QPushButton{
    background-color:#0a58ca;
}

"""

#删除按钮
DELETE_BUTTON_STYLE=BUTTON_STYLE+"""
QPushButton{
    background-color:#dc3545;
}
QPushButton:hover{
    background-color:#bb2d3b;
}
QPushButton:pressed{
    background-color:b02a37;
}
"""

#批量删除按钮
BATCH_DELETE_BUTTON_STYLE=BUTTON_STYLE+"""
QPushButton{
    background-color:#fd7e14;
}
QPushButton:hover{
    background-color:#e96b10;
}
QPushButton:pressed{
    background-color:#dc680f;
}
"""

#更新按钮
UPDATE_BUTTON_STYLE=BUTTON_STYLE+"""
QPushButton{
    background-color:#198754;
}
QPushButton:hover{
    background-color:#157347;
}
QPushButton:pressed{
    background-color:#146c43;
}
"""

#导入按钮
IMPORT_BUTTON_STYLE=BUTTON_STYLE+"""
QPushButton{
    background-color:#6f42c1;
}
QPushButton:hover{
    background-color:#5936a2;
}
QPushButton:pressed{
    background-color:#4a2d8e;
}
"""

#导出按钮
EXPORT_BUTTON_STYLE=BUTTON_STYLE+"""
QPushButton{
    background-color:#20c997;
}
QPushButton:hover{
    background-color:#1aa179;
}
QPushButton:pressed{
    background-color:#198b6d;
}
"""
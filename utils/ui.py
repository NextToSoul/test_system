from qfluentwidgets import FastCalendarPicker

class MyFastCalendarPicker(FastCalendarPicker):
    def __init__(self, parent=None):
        super().__init__(parent)

    def reset(self):
        super().reset()
        self.setText('请选择日期')
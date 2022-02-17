from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

class RadioChannelListGuiWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self, None)
        self.setWindowTitle("Channel List")
        self.setGeometry(0,0,180,200)

        self.channel_scroll_bar()

        self.show()

    def channel_scroll_bar(self):
        self.channel_list = QListWidget(self)
        self.channel_list.setGeometry(20,20,140,160)
        self.channel_list.itemClicked.connect(self.channel_clicked_return_channel)
        self.channel_list.itemClicked.connect(self.close)

        # ___Test Item___
        for i in range(10):
            self.channel_list.addItem(QListWidgetItem("channel " +  str(i)))
        # _______________

        scroll_bar = QScrollBar(self)
        self.channel_list.setVerticalScrollBar(scroll_bar)

    def add_channel_list(self, in_func):
        self.channel_list.addItem(QListWidgetItem(in_func))

    def channel_clicked_return_channel(self):
        # __Test__
        print(str(self.channel_list.currentItem().text())) 
        # ________
        return (str(self.channel_list.currentItem().text())) 
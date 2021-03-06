# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets
from sys import platform as _platform

class ConnectionSettingsDialog(QtWidgets.QDialog):
    def __init__(self, _parent, _batchconnection):
        super(QtWidgets.QDialog, self).__init__(_parent)
        # create dialog screen for changing connection parameters
        
        self.parent = _parent
        self.batchconnection = _batchconnection
        self.setWindowTitle(self.tr("Connection settings"))
        vbox = QtWidgets.QVBoxLayout()            
        
        hbox = QtWidgets.QHBoxLayout()
        text = "Time needed for a single transport action"
        label = QtWidgets.QLabel(text)
        self.spinbox0 = QtWidgets.QSpinBox()
        self.spinbox0.setAccelerated(True)
        self.spinbox0.setMaximum(999)
        self.spinbox0.setMinimum(1)
        self.spinbox0.setValue(self.batchconnection[2])
        label.setToolTip(text)
        self.spinbox0.setToolTip(text)
        if (self.batchconnection[2] >= 100):
            self.spinbox0.setSingleStep(100)
        elif (self.batchconnection[2] >= 10):
            self.spinbox0.setSingleStep(10) 
        hbox.addWidget(self.spinbox0)  
        hbox.addWidget(label)
        hbox.addStretch(1)
        vbox.addLayout(hbox)

        hbox = QtWidgets.QHBoxLayout()
        text = "Time added for each additional cassette or wafer stack"
        label = QtWidgets.QLabel(text)
        self.spinbox1 = QtWidgets.QSpinBox()
        self.spinbox1.setAccelerated(True)
        self.spinbox1.setMaximum(999)
        self.spinbox1.setMinimum(0)
        self.spinbox1.setValue(self.batchconnection[3])
        label.setToolTip(text)
        self.spinbox1.setToolTip(text)
        if (self.batchconnection[3] >= 100):
            self.spinbox1.setSingleStep(100)
        elif (self.batchconnection[3] >= 10):
            self.spinbox1.setSingleStep(10) 
        hbox.addWidget(self.spinbox1)  
        hbox.addWidget(label)
        hbox.addStretch(1)
        vbox.addLayout(hbox)

        hbox = QtWidgets.QHBoxLayout()
        text = "Minimum number of cassettes or stacks needed to start transport"
        label = QtWidgets.QLabel(text)
        self.spinbox2 = QtWidgets.QSpinBox()
        self.spinbox2.setAccelerated(True)
        self.spinbox2.setMaximum(99)
        self.spinbox2.setMinimum(1)
        self.spinbox2.setValue(self.batchconnection[4])
        label.setToolTip(text)
        self.spinbox2.setToolTip(text)
        hbox.addWidget(self.spinbox2)  
        hbox.addWidget(label)
        hbox.addStretch(1)
        vbox.addLayout(hbox)

        hard_limit_check = False
        # if not integer then it is a hard transport limit
        if (self.batchconnection[4] % 1) > 0:
            hard_limit_check = True

        hbox = QtWidgets.QHBoxLayout()
        text = "Apply minimum transport limit irrespective of space at destination"
        label = QtWidgets.QLabel(text)
        self.hard_limit_boolean = QtWidgets.QCheckBox()
        self.hard_limit_boolean.setChecked(hard_limit_check)
        label.setToolTip(text)
        self.hard_limit_boolean.setToolTip(text)        
        label.mouseReleaseEvent = self.switch_hard_limit       
        hbox.addWidget(self.hard_limit_boolean)
        hbox.addWidget(label)
        hbox.addStretch(1)                 
        vbox.addLayout(hbox)

        hbox = QtWidgets.QHBoxLayout()
        text = "Maximum number of cassettes or stacks for one transport run"
        label = QtWidgets.QLabel(text)
        self.spinbox3 = QtWidgets.QSpinBox()
        self.spinbox3.setAccelerated(True)
        self.spinbox3.setMaximum(99)
        self.spinbox3.setMinimum(1)
        self.spinbox3.setValue(self.batchconnection[5])
        label.setToolTip(text)
        self.spinbox3.setToolTip(text)
        hbox.addWidget(self.spinbox3)  
        hbox.addWidget(label)
        hbox.addStretch(1)
        vbox.addLayout(hbox)

        hbox = QtWidgets.QHBoxLayout()
        text = "Apply current settings to all connections"
        label = QtWidgets.QLabel(text)
        self.boolean = QtWidgets.QCheckBox()
        self.boolean.setChecked(False)
        label.setToolTip(text)
        self.boolean.setToolTip(text)        
        label.mouseReleaseEvent = self.switch_boolean        
        hbox.addWidget(self.boolean)
        hbox.addWidget(label)
        hbox.addStretch(1)                 
        vbox.addLayout(hbox)

        ### Buttonbox for ok or cancel ###
        buttonbox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        buttonbox.accepted.connect(self.read)
        buttonbox.rejected.connect(self.reject)
        if _platform == "linux" or _platform == "linux2":
            buttonbox.layout().setDirection(QtWidgets.QBoxLayout.RightToLeft) 
        vbox.addWidget(buttonbox)

        self.setLayout(vbox)        

    def switch_boolean(self, event):
        # function for making QLabel near checkbox clickable
        self.boolean.setChecked(not self.boolean.isChecked())

    def switch_hard_limit(self, event):
        # function for making QLabel near checkbox clickable
        self.hard_limit_boolean.setChecked(not self.hard_limit_boolean.isChecked())

    def read(self):
        # read contents of each widget
        # update settings in batchconnection(s)

        if self.hard_limit_boolean.isChecked():        
            transport_min_limit = int(self.spinbox2.text()) + 0.1
        else:
            transport_min_limit = int(self.spinbox2.text())        
        
        if self.boolean.isChecked():
            for i in range(len(self.parent.tools_widget.batchconnections)):
                self.parent.tools_widget.batchconnections[i][2] = int(self.spinbox0.text())
                self.parent.tools_widget.batchconnections[i][3] = int(self.spinbox1.text())
                self.parent.tools_widget.batchconnections[i][4] = transport_min_limit
                self.parent.tools_widget.batchconnections[i][5] = int(self.spinbox3.text())
            
            self.parent.statusBar().showMessage(self.tr("All connection settings updated"))
        else:
            self.batchconnection[2] = int(self.spinbox0.text())
            self.batchconnection[3] = int(self.spinbox1.text())
            self.batchconnection[4] = transport_min_limit
            self.batchconnection[5] = int(self.spinbox3.text())
            self.parent.statusBar().showMessage(self.tr("Connection settings updated"))
        
        
        self.accept()
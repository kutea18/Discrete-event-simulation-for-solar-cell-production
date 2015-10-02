# -*- coding: utf-8 -*-
from __future__ import division
from PyQt4 import QtGui
from sys import platform as _platform

class ConnectionSettingsDialog(QtGui.QDialog):
    def __init__(self, _parent, _batchconnection):
        super(QtGui.QDialog, self).__init__(_parent)
        # create dialog screen for changing connection parameters
        
        self.parent = _parent
        self.batchconnection = _batchconnection
        self.setWindowTitle(self.tr("Connection settings"))
        vbox = QtGui.QVBoxLayout()            
        
        hbox = QtGui.QHBoxLayout()
        label = QtGui.QLabel("Time needed for a single transport action")
        self.spinbox0 = QtGui.QSpinBox()
        self.spinbox0.setAccelerated(True)
        self.spinbox0.setMaximum(999999999)
        self.spinbox0.setValue(self.batchconnection[2])
        label.setToolTip("Time needed for a single transport action")
        self.spinbox0.setToolTip("Time needed for a single transport action")
        if (self.batchconnection[2] >= 100):
            self.spinbox0.setSingleStep(100)
        elif (self.batchconnection[2] >= 10):
            self.spinbox0.setSingleStep(10) 
        hbox.addWidget(self.spinbox0)  
        hbox.addWidget(label)
        hbox.addStretch(1)
        vbox.addLayout(hbox)

        hbox = QtGui.QHBoxLayout()
        label = QtGui.QLabel("Time added for each additional batch")
        self.spinbox1 = QtGui.QSpinBox()
        self.spinbox1.setAccelerated(True)
        self.spinbox1.setMaximum(999999999)
        self.spinbox1.setValue(self.batchconnection[3])
        label.setToolTip("Time added for each additional batch")
        self.spinbox1.setToolTip("Time added for each additional batch")
        if (self.batchconnection[3] >= 100):
            self.spinbox1.setSingleStep(100)
        elif (self.batchconnection[3] >= 10):
            self.spinbox1.setSingleStep(10) 
        hbox.addWidget(self.spinbox1)  
        hbox.addWidget(label)
        hbox.addStretch(1)
        vbox.addLayout(hbox)

        hbox = QtGui.QHBoxLayout()
        label = QtGui.QLabel("Apply current settings to all connections")
        self.boolean = QtGui.QCheckBox()
        self.boolean.setChecked(False)
        label.setToolTip("Apply current settings to all connections")
        self.boolean.setToolTip("Apply current settings to all connections")        
        label.mouseReleaseEvent = self.switch_boolean        
        hbox.addWidget(self.boolean)
        hbox.addWidget(label)
        hbox.addStretch(1)                 
        vbox.addLayout(hbox)

        ### Buttonbox for ok or cancel ###
        buttonbox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
        buttonbox.accepted.connect(self.read)
        buttonbox.rejected.connect(self.reject)
        if _platform == "linux" or _platform == "linux2":
            buttonbox.layout().setDirection(QtGui.QBoxLayout.RightToLeft) 
        vbox.addWidget(buttonbox)

        self.setLayout(vbox)        

    def switch_boolean(self, event):
        # function for making QLabel near checkbox clickable
        self.boolean.setChecked(not self.boolean.isChecked())

    def read(self):
        # read contents of each widget
        # update settings in batchconnection(s)
        if self.boolean.isChecked():
            for i in range(len(self.parent.batchconnections)):
                self.parent.batchconnections[i][2] = int(self.spinbox0.text())
                self.parent.batchconnections[i][3] = int(self.spinbox1.text())
            
            self.parent.statusBar().showMessage(self.tr("All connection settings updated"))
        else:
            self.batchconnection[2] = int(self.spinbox0.text())
            self.batchconnection[3] = int(self.spinbox1.text())
            self.parent.statusBar().showMessage(self.tr("Connection settings updated"))
        
        
        self.accept()
# -*- coding: utf-8 -*-
from __future__ import division
from PyQt4 import QtGui
from batchlocations.Operator import Operator
from sys import platform as _platform

class dummy_env(object):
    
    def process(dummy0=None,dummy1=None):
        pass

    def now(self):
        pass
    
    def event(dummy0=None):
        pass

class OperatorSettingsDialog(QtGui.QDialog):
    def __init__(self, _parent):
        super(QtGui.QDialog, self).__init__(_parent)
        # create dialog screen for each parameter in curr_params
        
        self.parent = _parent

        # find out which operator was selected
        self.row = self.parent.operators_view.selectedIndexes()[0].row()

        env = dummy_env()
        curr_params = {}
        # load default settings list
        curr_params = Operator(env).params

        # update default settings list with currently stored settings
        curr_params.update(self.parent.operators[self.row][1])

        self.setWindowTitle(self.tr("Available settings"))
        vbox = QtGui.QVBoxLayout()

        ### Add specification text ###
        hbox = QtGui.QHBoxLayout()
        if 'specification' in curr_params:            
            spec = QtGui.QLabel(curr_params['specification'])           
            spec.setWordWrap(True)
            hbox.addWidget(spec)
            hbox.addStretch(1)
        else:
            title_label = QtGui.QLabel(self.tr("Edit settings:"))             
            hbox.addWidget(title_label)
            hbox.addStretch(1)
        vbox.addLayout(hbox)             
        
        self.strings = []
        for i in curr_params:
            if ("_desc" in i) | ('specification' in i):
                continue
            elif isinstance(curr_params[i], str):
                hbox = QtGui.QHBoxLayout()
                description = QtGui.QLabel(curr_params[i + "_desc"])
                self.strings.append(QtGui.QLineEdit(curr_params[i]))
                self.strings[-1].setObjectName(i)
                if i + "_desc" in curr_params:
                    self.strings[-1].setToolTip(curr_params[i + "_desc"])
                hbox.addWidget(self.strings[-1]) 
                hbox.addWidget(description)
                hbox.addStretch(1)                 
                vbox.addLayout(hbox)
        
        self.integers = []
        for i in curr_params:
            if isinstance(curr_params[i], int) & (not i == 'verbose'):
                hbox = QtGui.QHBoxLayout()
                description = QtGui.QLabel(curr_params[i + "_desc"])
                self.integers.append(QtGui.QSpinBox())
                self.integers[-1].setAccelerated(True)
                self.integers[-1].setMaximum(999999999)
                self.integers[-1].setValue(curr_params[i])
                self.integers[-1].setObjectName(i)
                if (curr_params[i] >= 100):
                    self.integers[-1].setSingleStep(100)
                elif (curr_params[i] >= 10):
                    self.integers[-1].setSingleStep(10)                     
                if i + "_desc" in curr_params:
                    self.integers[-1].setToolTip(curr_params[i + "_desc"])
                hbox.addWidget(self.integers[-1])  
                hbox.addWidget(description)
                hbox.addStretch(1)                 
                vbox.addLayout(hbox)

        self.doubles = []
        for i in curr_params:
            if isinstance(curr_params[i], float):
                hbox = QtGui.QHBoxLayout()
                description = QtGui.QLabel(curr_params[i + "_desc"])
                self.doubles.append(QtGui.QDoubleSpinBox())
                self.doubles[-1].setAccelerated(True)
                self.doubles[-1].setMaximum(999999999)
                self.doubles[-1].setValue(curr_params[i])
                self.doubles[-1].setSingleStep(0.1)
                self.doubles[-1].setObjectName(i)
                if i + "_desc" in curr_params:
                    self.doubles[-1].setToolTip(curr_params[i + "_desc"])
                hbox.addWidget(self.doubles[-1])
                hbox.addWidget(description)
                hbox.addStretch(1)                  
                vbox.addLayout(hbox)
        
        self.booleans = []
        for i in curr_params:
            if isinstance(curr_params[i], bool):
                hbox = QtGui.QHBoxLayout()
                description = QtGui.QLabel(curr_params[i + "_desc"])
                self.booleans.append(QtGui.QCheckBox())                
                self.booleans[-1].setChecked(curr_params[i])
                self.booleans[-1].setObjectName(i)
                if i + "_desc" in curr_params:
                    self.booleans[-1].setToolTip(curr_params[i + "_desc"])
                hbox.addWidget(self.booleans[-1])
                hbox.addWidget(description)
                hbox.addStretch(1)                 
                vbox.addLayout(hbox)

        ### Widget for scrollable area ###
        widget = QtGui.QWidget()
        widget.setLayout(vbox)
        scroll = QtGui.QScrollArea()      
        scroll.setWidget(widget)       

        container = QtGui.QVBoxLayout()         
        container.addWidget(scroll)

        ### Buttonbox for ok or cancel ###
        hbox = QtGui.QHBoxLayout()
        buttonbox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
        buttonbox.accepted.connect(self.read)
        buttonbox.rejected.connect(self.reject)
        if _platform == "linux" or _platform == "linux2":
            buttonbox.layout().setDirection(QtGui.QBoxLayout.RightToLeft)
        hbox.addStretch(1) 
        hbox.addWidget(buttonbox)
        hbox.addStretch(1)
        hbox.setContentsMargins(0,0,0,4)                
        container.addLayout(hbox)        
        container.setContentsMargins(0,0,0,0)

        self.setLayout(container)
        self.setMinimumWidth(spec.width()+40)

    def read(self):
        # read contents of each widget
        # update settings in self.operators[self.row] of parent
        new_params = {}
        for i in self.strings:
            new_params[str(i.objectName())] = str(i.text())

        for i in self.integers:
            new_params[str(i.objectName())] = int(i.text())

        for i in self.doubles:
            new_params[str(i.objectName())] = float(i.text())

        for i in self.booleans:
            new_params[str(i.objectName())] = i.isChecked()
        
        self.parent.operators[self.row][1].update(new_params)
        self.parent.load_definition_operators(False)

        # select row again after reloading operator definitions
        index = self.parent.operators_model.index(self.row, 0)
        self.parent.operators_view.setCurrentIndex(index)
        self.parent.statusBar().showMessage(self.tr("Operator settings updated"))
        self.accept()
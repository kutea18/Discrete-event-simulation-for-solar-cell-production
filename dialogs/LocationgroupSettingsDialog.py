# -*- coding: utf-8 -*-
from __future__ import division
from blockdiag import parser, builder, drawer
from PyQt4 import QtGui, QtCore, QtSvg
from batchlocations.WaferSource import WaferSource
from batchlocations.WaferUnstacker import WaferUnstacker
from batchlocations.WaferBin import WaferBin
from batchlocations.BatchTex import BatchTex
from batchlocations.BatchClean import BatchClean
from batchlocations.TubeFurnace import TubeFurnace
from batchlocations.SingleSideEtch import SingleSideEtch
from batchlocations.TubePECVD import TubePECVD
from batchlocations.PrintLine import PrintLine
from batchlocations.Buffer import Buffer
from batchlocations.IonImplanter import IonImplanter
from batchlocations.SpatialALD import SpatialALD
from batchlocations.InlinePECVD import InlinePECVD

class dummy_env(object):
    
    def process(dummy0=None,dummy1=None):
        pass

    def now(self):
        pass
    
    def event(dummy0=None):
        pass

class LocationgroupSettingsDialog(QtGui.QDialog):
    def __init__(self, _parent):
        super(QtGui.QDialog, self).__init__(_parent)
        # create dialog screen for each parameter in curr_params
        
        self.parent = _parent

        # find out which batchlocation was selected
        self.row = self.parent.batchlocations_view.selectedIndexes()[0].row()      
        batchlocation = self.parent.batchlocations[self.parent.locationgroups[self.row][0]]

        env = dummy_env()
        curr_params = {}
        curr_diagram = None
        # load default settings list
        if (batchlocation[0] == "WaferSource"):
            curr_params = WaferSource(env).params
            curr_diagram  = WaferSource(env).diagram
        elif (batchlocation[0] == "WaferUnstacker"):
            curr_params = WaferUnstacker(env).params
            curr_diagram  = WaferUnstacker(env).diagram            
        elif (batchlocation[0] == "BatchTex"):
            curr_params = BatchTex(env).params
            curr_diagram  = BatchTex(env).diagram            
        elif (batchlocation[0] == "BatchClean"):
            curr_params = BatchClean(env).params            
            curr_diagram  = BatchClean(env).diagram            
        elif (batchlocation[0] == "TubeFurnace"):
            curr_params = TubeFurnace(env).params
            curr_diagram  = TubeFurnace(env).diagram            
        elif (batchlocation[0] == "SingleSideEtch"):
            curr_params = SingleSideEtch(env).params
            curr_diagram  = SingleSideEtch(env).diagram            
        elif (batchlocation[0] == "TubePECVD"):
            curr_params = TubePECVD(env).params
            curr_diagram  = TubePECVD(env).diagram            
        elif (batchlocation[0] == "PrintLine"):
            curr_params = PrintLine(env).params            
            curr_diagram  = PrintLine(env).diagram            
        elif (batchlocation[0] == "WaferBin"):
            curr_params = WaferBin(env).params
            curr_diagram  = WaferBin(env).diagram            
        elif (batchlocation[0] == "Buffer"):
            curr_params = Buffer(env).params            
            curr_diagram  = Buffer(env).diagram            
        elif (batchlocation[0] == "IonImplanter"):
            curr_params = IonImplanter(env).params
            curr_diagram  = IonImplanter(env).diagram            
        elif (batchlocation[0] == "SpatialALD"):
            curr_params = SpatialALD(env).params            
            curr_diagram  = SpatialALD(env).diagram            
        elif (batchlocation[0] == "InlinePECVD"):
            curr_params = InlinePECVD(env).params 
            curr_diagram  = InlinePECVD(env).diagram            
        else:
            return                         
        
        # update default settings list with currently stored settings
        curr_params.update(batchlocation[1])
        
        self.setWindowTitle(self.tr("Available settings"))
        vbox = QtGui.QVBoxLayout()

        ### Add diagram ###
        hbox = QtGui.QHBoxLayout()
        tree = parser.parse_string(curr_diagram)
        diagram = builder.ScreenNodeBuilder.build(tree)
        draw = drawer.DiagramDraw('SVG', diagram, filename="")
        draw.draw()
        svg_string = draw.save()

        svg_widget = QtSvg.QSvgWidget()
        svg_widget.load(QtCore.QString(svg_string).toLocal8Bit())

        hbox.addWidget(svg_widget)
        hbox.addStretch(1)            
        vbox.addLayout(hbox)

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
        self.integers = []
        self.doubles = []
        self.booleans = []
        
        for i in sorted(curr_params.keys()):
        # Make QLineEdits for strings (excluding name)
            if ("_desc" in i) | ('specification' in i) | ('name' in i):
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
        
        for i in sorted(curr_params.keys()):
        # Make QSpinBox or QDoubleSpinbox for integers and doubles
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
            elif isinstance(curr_params[i], float):
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
        
        for i in sorted(curr_params.keys()):
        # Make QCheckBox for booleans
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
        buttonbox.layout().setDirection(QtGui.QBoxLayout.RightToLeft)
        hbox.addStretch(1) 
        hbox.addWidget(buttonbox)
        hbox.addStretch(1)                 
        hbox.setContentsMargins(0,0,0,4)                
        container.addLayout(hbox)        
        container.setContentsMargins(0,0,0,0)

        self.setLayout(container)
        if (svg_widget.width() > spec.width()):
            self.setMinimumWidth(svg_widget.width()+40)
        else:
            self.setMinimumWidth(spec.width()+40)

    def read(self):
        # read contents of each widget
        # update settings in self.batchlocations[self.modified_batchlocation_number] of parent
        new_params = {}
        for i in self.strings:
            new_params[str(i.objectName())] = str(i.text())

        for i in self.integers:
            new_params[str(i.objectName())] = int(i.text())

        for i in self.doubles:
            new_params[str(i.objectName())] = float(i.text())

        for i in self.booleans:
            new_params[str(i.objectName())] = i.isChecked()
        
        for i in self.parent.locationgroups[self.row]:
            self.parent.batchlocations[i][1].update(new_params)
        
        self.parent.load_definition_batchlocations(False)

        if self.row: # expand row again after reloading definitions
            index = self.parent.batchlocations_model.index(self.row, 0)
            self.parent.batchlocations_view.setExpanded(index, True)
        
        self.parent.statusBar().showMessage(self.tr("Location group settings updated"))
        self.accept()
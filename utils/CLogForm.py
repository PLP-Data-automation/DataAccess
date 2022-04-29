from PyQt5 import QtCore, QtWidgets, QtGui
import os

class UILogForm(object):
    def setupUI(self, DialogWindow):
        DialogWindow.setWindowTitle( "Authentication" )
        layout              = QtWidgets.QVBoxLayout()
        sublayout_top       = QtWidgets.QHBoxLayout()
        sublayout_bot       = QtWidgets.QHBoxLayout()

        layout.addLayout( sublayout_top )
        layout.addLayout( sublayout_bot )

        self.loadCred      = QtWidgets.QPushButton()
        self.loadCred.setText( "Load Credentials" )
        self.newCred        = QtWidgets.QPushButton()
        self.newCred.setText( "New Credentials" )
        
        sublayout_top.addWidget( QtWidgets.QLabel( "Select an authentication method:" ) )
        sublayout_bot.addWidget( self.loadCred )
        sublayout_bot.addWidget( self.newCred )

        DialogWindow.setLayout( layout )
        QtCore.QMetaObject.connectSlotsByName( DialogWindow )
        
        

class CLogForm( QtWidgets.QDialog, UILogForm ):
    def __init__(self, parent=None):
        super( QtWidgets.QDialog, self ).__init__( parent=parent )
        iconpath = os.path.join( os.path.dirname( os.path.realpath( __file__ ) ), "icon.png" )
        self.setWindowIcon( QtGui.QIcon( iconpath ) )
        self.setupUI( self )
        self.method = None
        self.loadCred.clicked.connect( self.loadCredentials )
        self.newCred.clicked.connect( self.newCredentials )

        
        

    def loadCredentials(self):
        self.method = "load"
        self.close()

    def newCredentials(self):
        self.method = "new"
        self.close()
        
def Dialog():
    app = QtWidgets.QApplication( [] )
    dialog = CLogForm()
    dialog.exec()
    return dialog.method

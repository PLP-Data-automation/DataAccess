from PyQt5 import QtCore, QtWidgets, QtGui
import os

class UILogInForm(object):
    def setupUI(self, DialogWindow, files):
        DialogWindow.setWindowTitle( "Load Credentials" )
        layout              = QtWidgets.QVBoxLayout()
        subLayout_form      = QtWidgets.QHBoxLayout()
        subLayout_labels    = QtWidgets.QVBoxLayout()
        subLayout_boxes     = QtWidgets.QVBoxLayout()
        subLayout_buttons   = QtWidgets.QHBoxLayout()

        subLayout_form.addLayout( subLayout_labels )
        subLayout_form.addLayout( subLayout_boxes )
        layout.addLayout( subLayout_form )
        layout.addLayout( subLayout_buttons )

        self.file       = QtWidgets.QComboBox()
        self.file.addItems(files)
        self.password   = QtWidgets.QLineEdit()
        self.password.setEchoMode( QtWidgets.QLineEdit.EchoMode.Password )
        
        subLayout_boxes.addWidget( self.file )
        subLayout_boxes.addWidget( self.password )

        subLayout_labels.addWidget( QtWidgets.QLabel( "Select your credentials" ) )
        subLayout_labels.addWidget( QtWidgets.QLabel( "Password" ) )

        OK      = QtWidgets.QDialogButtonBox.StandardButton.Ok
        CANCEL  = QtWidgets.QDialogButtonBox.StandardButton.Cancel
        self.buttons = QtWidgets.QDialogButtonBox( OK | CANCEL )
        subLayout_buttons.addWidget( self.buttons )
        
        DialogWindow.setLayout( layout )
        QtCore.QMetaObject.connectSlotsByName( DialogWindow )

class CLogInForm( QtWidgets.QDialog, UILogInForm ):
    def __init__(self, path, parent=None):
        super( QtWidgets.QDialog, self ).__init__( parent=parent )
        iconpath = os.path.join( os.path.dirname( os.path.realpath( __file__ ) ), "icon.png" )
        self.setWindowIcon( QtGui.QIcon( iconpath ) )
        self.val    = None
        self.loc    = None
        self.dir, self.files = self.getFiles( path )
        self.setupUI( self, self.files )
        self.buttons.accepted.connect( self.getSelected )
        self.buttons.rejected.connect( self.getRejected )
        
    def getFiles(self, path):
        if not os.path.exists( path ):
            os.makedirs( path, exist_ok=True )
        for dir,_,files in os.walk( path ):
            return dir, files

    def getSelected(self):
        file = self.file.currentText()
        if file != "":
            self.val = self.password.text()
            self.loc = os.path.join( self.dir, file )
        self.close()

    def getRejected(self):
        self.val    = None
        self.loc    = None
        self.close()
        
def Dialog( path ):
    app = QtWidgets.QApplication( [] )
    dialog = CLogInForm( path )
    dialog.exec()
    return bytes( dialog.val, encoding='utf-8' ), dialog.loc

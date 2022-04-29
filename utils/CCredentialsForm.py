from PyQt5 import QtCore, QtWidgets, QtGui
import os

class UICredentialsForm(object):
    def setupUI(self, DialogWindow):
        DialogWindow.setWindowTitle( "New Credentials" )
        layout              = QtWidgets.QVBoxLayout()
        subLayout_form      = QtWidgets.QHBoxLayout()
        subLayout_labels    = QtWidgets.QVBoxLayout()
        subLayout_boxes     = QtWidgets.QVBoxLayout()
        subLayout_buttons   = QtWidgets.QHBoxLayout()

        subLayout_form.addLayout( subLayout_labels )
        subLayout_form.addLayout( subLayout_boxes )
        layout.addLayout( subLayout_form )
        layout.addLayout( subLayout_buttons )

        self.account    = QtWidgets.QLineEdit()
        self.username   = QtWidgets.QLineEdit()
        self.password   = QtWidgets.QLineEdit()
        self.password.setEchoMode( QtWidgets.QLineEdit.EchoMode.Password )
        self.devid      = QtWidgets.QLineEdit()
        self.dusername  = QtWidgets.QLineEdit()
        self.dpassword  = QtWidgets.QLineEdit()
        self.dpassword.setEchoMode( QtWidgets.QLineEdit.EchoMode.Password )

        self.cnamefile  = QtWidgets.QLineEdit()
        self.cpassword  = QtWidgets.QLineEdit()
        self.cpassword.setEchoMode( QtWidgets.QLineEdit.EchoMode.Password )


        subLayout_boxes.addWidget( self.account )
        subLayout_boxes.addWidget( self.username )
        subLayout_boxes.addWidget( self.password )
        subLayout_boxes.addWidget( self.devid )
        subLayout_boxes.addWidget( self.dusername )
        subLayout_boxes.addWidget( self.dpassword )
        subLayout_boxes.addWidget( QtWidgets.QLabel( "" ) )
        subLayout_boxes.addWidget( self.cnamefile )
        subLayout_boxes.addWidget( self.cpassword )

        subLayout_labels.addWidget( QtWidgets.QLabel( "T2M Account" ) )
        subLayout_labels.addWidget( QtWidgets.QLabel( "T2M Username" ) )
        subLayout_labels.addWidget( QtWidgets.QLabel( "T2M Password" ) )
        subLayout_labels.addWidget( QtWidgets.QLabel( "T2M Developer ID" ) )
        subLayout_labels.addWidget( QtWidgets.QLabel( "Device Username" ) )
        subLayout_labels.addWidget( QtWidgets.QLabel( "Device Password" ) )
        subLayout_labels.addWidget( QtWidgets.QLabel( "" ) )
        subLayout_labels.addWidget( QtWidgets.QLabel( "Credentials name" ) )
        subLayout_labels.addWidget( QtWidgets.QLabel( "Credentials password" ) )

        OK      = QtWidgets.QDialogButtonBox.StandardButton.Ok
        CANCEL  = QtWidgets.QDialogButtonBox.StandardButton.Cancel
        self.buttons = QtWidgets.QDialogButtonBox( OK | CANCEL )
        subLayout_buttons.addWidget( self.buttons )
        
        DialogWindow.setLayout( layout )
        QtCore.QMetaObject.connectSlotsByName( DialogWindow )

class CCredentialsForm( QtWidgets.QDialog, UICredentialsForm ):
    def __init__(self, parent=None):
        super( QtWidgets.QDialog, self ).__init__( parent=parent )
        iconpath = os.path.join( os.path.dirname( os.path.realpath( __file__ ) ), "icon.png" )
        self.setWindowIcon( QtGui.QIcon( iconpath ) )
        self.setupUI( self )
        self.buttons.accepted.connect( self.getSelected )
        self.buttons.rejected.connect( self.getRejected )
        self.val = None
        self.cname = None
        self.cpswd = None

    def getSelected(self):
        self.val = {
            "t2maccount"        : self.account.text(),
            "t2musername"       : self.username.text(),
            "t2mpassword"       : self.password.text(),
            "t2mdeveloperid"    : self.devid.text(),
            "t2mdeviceusername" : self.dusername.text(),
            "t2mdevicepassword" : self.dpassword.text()
        }
        name = self.cnamefile.text()
        pswd = self.cpassword.text()
        if not "" in [ name, pswd ]:
            self.cname = name
            self.cpswd = pswd
            self.close()

    def getRejected(self):
        self.val = None
        self.cname = None
        self.cpswd = None
        self.close()
        
def Dialog():
    app = QtWidgets.QApplication( [] )
    dialog = CCredentialsForm()
    dialog.exec()
    return dialog.val, bytes( dialog.cpswd, encoding='utf-8' ), dialog.cname

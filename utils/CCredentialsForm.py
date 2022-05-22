"""
Author: Fuentes Juvera, Luis
E-mail: luis.fuju@outlook.com
username: LuisDFJ

CCredentialsForm Module: Creates a GUI for entering credentials.

Dumps credentials: t2maccount, t2musername, t2mpassword, t2mdeveloperid
t2mdeviceusername, t2mdevicepassword.

Classes
-------
UICredentialsForm( DialogWIndow : QtWidgets.QWidget | None )
CCredentialsForm( parent : QtWidgets.QWidget | None )

Functions
---------
Dialog(  ) -> tuple( dict, bytes )

"""

from PyQt5 import QtCore, QtWidgets, QtGui
import os

class UICredentialsForm(object):
    """
    Graphic setup of credentials form.

    Attributes
    ----------
    account : QtWidgets.QLineEdit
        Line for t2maccount.
    username : QtWidgets.QLineEdit
        Line for t2musername.
    password : QtWidgets.QLineEdit
        Line for t2mpassword.
    devid : QtWidgets.QLineEdit
        Line for t2mdeveloperid.
    dusername : QtWidgets.QLineEdit
        Line for t2mdeviceusername.
    dpassword : QtWidgets.QLineEdit
        Line for t2mdevicepassword.

    Methods
    -------
    setupUI( DialogWindow ) -> None
    """
    def setupUI(self, DialogWindow) -> None:
        """
        Graphic setup of credentials form.

        Parameters
        ----------
        DialogWindow : QtWidgets.QWidget
            Parent QWidget.

        """
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
    """
    Logical control of credentials form.

    Attributes
    ----------
    val : dict | None
        Variable reserved for credentials dict.
    cname : str | None
        Variable reserved for naming credentials.
    cpswd : str | None
        Variable reserved for encrypting credentials.

    Methods
    -------
    getSelected( ) -> None:
        Callback when devices selected.
    getRejected( ) -> None:
        Callback when operation canceled.

    """
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

    def getSelected(self) -> None:
        """
        Callback when devices selected.
        """
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

    def getRejected(self) -> None:
        """
        Callback when operation canceled.
        """
        self.val = None
        self.cname = None
        self.cpswd = None
        self.close()
        
def Dialog():
    """
    Dialog box wrapper for credentials form.

    Returns
    -------
    tuple( dict | None, bytes | None, str | None )
        Selected credentials and dump parameters.

    """
    app = QtWidgets.QApplication( [] )
    dialog = CCredentialsForm()
    dialog.exec()
    return dialog.val, bytes( dialog.cpswd, encoding='utf-8' ), dialog.cname

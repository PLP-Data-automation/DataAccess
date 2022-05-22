"""
Author: Fuentes Juvera, Luis
E-mail: luis.fuju@outlook.com
username: LuisDFJ

CLogForm Module: Creates a GUI for Log.

Promps form to use new credentials or load
previous ones on dump path.

Classes
-------
UILogInForm( DialogWIndow )
CLogForm( parent )

Functions
---------
Dialog( path : str )

"""

from PyQt5 import QtCore, QtWidgets, QtGui
import os

class UILogForm(object):
    """
    Graphic setup of Log In form.

    Attributes
    ----------
    loadCred : QtWidgets.QPushBotton
        Load credentials.
    newCred : QtWidgets.QPushBotton
        Create new credentials.
    
    Methods
    -------
    setupUI( DialogWindow ) -> None
    """
    def setupUI(self, DialogWindow):
        """
        Graphic setup of Log In form.

        Parameters
        ----------
        DialogWindow : QtWidgets.QWidget
            Parent QWidget.

        """
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
    """
    Logical control of Log Form.

    Attributes
    ----------
    method : str | None
        Variable reserved for log method.

    Methods
    -------
    loadCredentials( ) -> None:
        Load method selection.
    newCredentials( ) -> None:
        New method selection.

    """
    def __init__(self, parent=None):
        """
        Logical control of Log Form.

        Parameters
        ----------
        parent : QtWidgets.QWidget | None
            Parent Widget.

        """
        super( QtWidgets.QDialog, self ).__init__( parent=parent )
        iconpath = os.path.join( os.path.dirname( os.path.realpath( __file__ ) ), "icon.png" )
        self.setWindowIcon( QtGui.QIcon( iconpath ) )
        self.setupUI( self )
        self.method = None
        self.loadCred.clicked.connect( self.loadCredentials )
        self.newCred.clicked.connect( self.newCredentials )

    def loadCredentials(self) -> None:
        """
        Load method selection
        """
        self.method = "load"
        self.close()

    def newCredentials(self) -> None:
        """
        New method selection
        """
        self.method = "new"
        self.close()
        
def Dialog():
    """
    Dialog box wrapper for Log form.

    Returns
    -------
    str | None
        Method type.

    """
    app = QtWidgets.QApplication( [] )
    dialog = CLogForm()
    dialog.exec()
    return dialog.method

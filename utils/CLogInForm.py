"""
Author: Fuentes Juvera, Luis
E-mail: luis.fuju@outlook.com
username: LuisDFJ

CLogInForm Module: Creates a GUI for Log In.

Promps form to use existing credentials on 
dump path.

Classes
-------
UILogInForm( DialogWIndow, files : list )
CLogInForm( path : str, parent )

Functions
---------
Dialog( path : str )

"""

from PyQt5 import QtCore, QtWidgets, QtGui
import os

class UILogInForm(object):
    """
    Graphic setup of Log In form.

    Attributes
    ----------
    file : QtWidgets.QComboBox
        Name of the credentials file.
    password : str
        Password to unlock credentials.
    
    Methods
    -------
    setupUI( DialogWindow, files:str ) -> None
    """
    def setupUI(self, DialogWindow, files : list) -> None:
        """
        Graphical setup for Log In form.

        Parameters
        ----------
        DialogWindow : QtWidgets.QWidget
            Parent QWidget.
        files : list
            List of credentials files.
        """
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
    """
    Logical control of Log In Form.

    Attributes
    ----------
    val : str | None
        Variable reserved for key.
    loc : str | None
        Variable reserved for credentials path.

    Methods
    -------
    getFiles(path : str) -> tuple( [str, list] ):
        Search all files available in directory.
    getSelected( ) -> None:
        On close callback.
    getRejected( ) -> None:
        On close callback.

    """
    def __init__(self, path : str, parent=None) -> None:
        """
        Logical control of Log In Form.

        Parameters
        ----------
        path : str
            Path for searching credentials.
        parent : QtWidgets.QWidget | None
            Parent Widget.

        """
        super( QtWidgets.QDialog, self ).__init__( parent=parent )
        iconpath = os.path.join( os.path.dirname( os.path.realpath( __file__ ) ), "icon.png" )
        self.setWindowIcon( QtGui.QIcon( iconpath ) )
        self.val    = None
        self.loc    = None
        self.dir, self.files = self.getFiles( path )
        self.setupUI( self, self.files )
        self.buttons.accepted.connect( self.getSelected )
        self.buttons.rejected.connect( self.getRejected )
        
    def getFiles(self, path : str):
        """
        Search all files available in directory.

        Parameters
        ----------
        path : str

        Returns
        -------
        tuple( [ str, list ] )
            dir, files

        """
        if not os.path.exists( path ):
            os.makedirs( path, exist_ok=True )
        for dir,_,files in os.walk( path ):
            return dir, files

    def getSelected(self) -> None:
        """
        On close callback.
        """
        file = self.file.currentText()
        if file != "":
            self.val = self.password.text()
            self.loc = os.path.join( self.dir, file )
        self.close()

    def getRejected(self) -> None:
        """
        On close callback.
        """
        self.val    = None
        self.loc    = None
        self.close()
        
def Dialog( path : str ):
    """
    Dialog box wrapper for Log In form.

    Parameters
    ----------
    path : str
        Path to search credentials.
    
    Returns
    -------
    tuple( bytes, str )
        Encoded key, path to selected credentials.

    """
    app = QtWidgets.QApplication( [] )
    dialog = CLogInForm( path )
    dialog.exec()
    return bytes( dialog.val, encoding='utf-8' ), dialog.loc

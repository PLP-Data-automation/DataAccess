"""
Author: Fuentes Juvera, Luis
E-mail: luis.fuju@outlook.com
username: LuisDFJ

CEwonSelectForm Module: Creates a GUI for Ewon selection.

Promps form to select available devices.

Classes
-------
UIEwonSelectForm( DialogWIndow, ewons : list )
CEwonSelectForm( ewons : list, parent : QtWidgets.QWidget | None )

Functions
---------
Dialog( selection_list : list )

"""

from PyQt5 import QtCore, QtWidgets, QtGui
import os

class UIEwonSelectForm(object):
    """
    Graphic setup of Ewon Selection form.

    Attributes
    ----------
    Selector : QtWidgets.QListWidget
        Selected devices.
    
    Methods
    -------
    setupUI( DialogWindow, ewons : list ) -> None
    """
    def setupUI(self, DialogWindow, ewons : list ):
        """
        Graphic setup of Ewon Selection form.

        Parameters
        ----------
        DialogWindow : QtWidgets.QWidget
            Parent QWidget.
        ewons : list[str]
            Available devices.

        """
        DialogWindow.setWindowTitle( "Select Device" )
        layout = QtWidgets.QVBoxLayout( DialogWindow )
        subLayout_1 = QtWidgets.QHBoxLayout()
        subLayout_2 = QtWidgets.QHBoxLayout()

        layout.addLayout( subLayout_1 )
        layout.addLayout( subLayout_2 )

        self.Selector = QtWidgets.QListWidget()
        self.Selector.addItems( ewons )
        self.Selector.setSelectionMode( QtWidgets.QAbstractItemView.SelectionMode.ExtendedSelection )
        width   = self.Selector.sizeHintForColumn(0) + 2 * self.Selector.frameWidth() + 50
        height  = self.Selector.sizeHintForRow(0) * 3 + 2 * self.Selector.frameWidth()
        self.Selector.setFixedSize( width, height )

        OK = QtWidgets.QDialogButtonBox.StandardButton.Ok
        CANCEL = QtWidgets.QDialogButtonBox.StandardButton.Cancel
        self.okButton = QtWidgets.QDialogButtonBox( OK | CANCEL )

        subLayout_1.addWidget( QtWidgets.QLabel( "Select your ewon devices: " ) )
        subLayout_1.addWidget( self.Selector )
        
        subLayout_2.addWidget( self.okButton )
        
        DialogWindow.setLayout( layout )
        QtCore.QMetaObject.connectSlotsByName( DialogWindow )

class CEwonSelectForm( QtWidgets.QDialog, UIEwonSelectForm ):
    """
    Logical control of Ewon Selection Form.

    Attributes
    ----------
    val : list | None
        Variable reserved for selected devices.

    Methods
    -------
    getSelected( ) -> None:
        Callback when devices selected.
    getRej( ) -> None:
        Callback when operation canceled.

    """
    def __init__(self, ewons : list=[], parent=None):
        """
        Logical control of Ewon Selection Form.

        Parameters
        ----------
        ewons : list
            List of devices.
        parent : QtWidgets.QWidget | None
            Parent Widget.

        """
        super( QtWidgets.QDialog, self ).__init__( parent=parent )
        iconpath = os.path.join( os.path.dirname( os.path.realpath( __file__ ) ), "icon.png" )
        self.setWindowIcon( QtGui.QIcon( iconpath ) )
        self.setupUI( self, ewons )
        self.okButton.accepted.connect( self.getSelected )
        self.okButton.rejected.connect( self.getRej )
        self.val = None

    def getSelected(self) -> None:
        """
        Callback when devices selected.
        """
        selections = []
        for item in self.Selector.selectedItems():
            selections.append( item.text() )
        self.val = selections
        self.close()

    def getRej(self) -> None:
        """
        Callback when operation canceled.
        """
        self.val = None
        self.close()
        
def Dialog( selection_list : list ):
    """
    Dialog box wrapper for Ewon Selection form.

    Returns
    -------
    list | None
        Selected devices.

    """
    app = QtWidgets.QApplication( [] )
    dialog = CEwonSelectForm( selection_list )
    dialog.exec()
    return dialog.val

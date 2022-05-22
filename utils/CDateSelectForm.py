"""
Author: Fuentes Juvera, Luis
E-mail: luis.fuju@outlook.com
username: LuisDFJ

CDateSelectForm Module: Creates a GUI for date selection.

Promps calendar to select the time interval to fetch information
from devices.

Classes
-------
CCalendarWidget(  )
UIDateSelectForm( DialogWIndow : QtWidgets.QWidget | None )
CDateSelectForm( parent : QtWidgets.QWidget | None )

Functions
---------
Dialog( ) -> str | None

"""

from PyQt5 import QtCore, QtWidgets, QtGui
import os

class CCalendarWidget( QtWidgets.QCalendarWidget ):
    """
    Widget for selecting multiple dates using shift key.

    Methods
    -------
    format_range( format ) -> None
    date_is_clicked( date ) -> None

    """
    def __init__(self):
        super( CCalendarWidget, self ).__init__()
        self.s_date = None
        self.e_date = None

        self.setMaximumDate( QtCore.QDate().currentDate() )
        self.highlight_format = QtGui.QTextCharFormat()
        self.highlight_format.setBackground(self.palette().brush( QtGui.QPalette.Highlight ))
        self.highlight_format.setForeground(self.palette().color( QtGui.QPalette.HighlightedText ))
        self.clicked.connect(self.date_is_clicked)

    def format_range(self, format):
        if self.s_date and self.e_date:
            d_low   = min(self.s_date, self.e_date)
            d_high  = max(self.s_date, self.e_date)
            while d_low <= d_high:
                self.setDateTextFormat( d_low, format )
                d_low = d_low.addDays(1)

    def date_is_clicked(self, date):
        self.format_range( QtGui.QTextCharFormat() )
        if QtWidgets.QApplication.instance().keyboardModifiers() & QtCore.Qt.ShiftModifier and self.s_date:
            self.e_date = date
            self.format_range( self.highlight_format )
        else:
            self.s_date = date
            self.e_date = None


class UIDateSelectForm(object):
    """
    Graphic setup of date selection form.

    Attributes
    ----------
    Calendar : CCalendarWidget
        Calendar for multiple selection.
    
    Methods
    -------
    setupUI( DialogWindow ) -> None
    """
    def setupUI(self, DialogWindow ) -> None:
        """
        Graphic setup of date selection form.

        Parameters
        ----------
        DialogWindow : QtWidgets.QWidget
            Parent QWidget.

        """
        DialogWindow.setWindowTitle( "Select Date" )
        layout = QtWidgets.QVBoxLayout( DialogWindow )
        subLayout_1 = QtWidgets.QHBoxLayout()
        subLayout_2 = QtWidgets.QHBoxLayout()

        layout.addLayout( subLayout_1 )
        layout.addLayout( subLayout_2 )

        self.calendar = CCalendarWidget()

        OK = QtWidgets.QDialogButtonBox.StandardButton.Ok
        CANCEL = QtWidgets.QDialogButtonBox.StandardButton.Cancel
        self.okButton = QtWidgets.QDialogButtonBox( OK | CANCEL )

        subLayout_1.addWidget( self.calendar )
        subLayout_2.addWidget( self.okButton )
        DialogWindow.setLayout( layout )

        QtCore.QMetaObject.connectSlotsByName( DialogWindow )

class CDateSelectForm( QtWidgets.QDialog, UIDateSelectForm ):
    """
    Logical control of date selection form.

    Attributes
    ----------
    val : str | None
        Variable reserved for selected date interval.

    Methods
    -------
    getSelected( ) -> None:
        Callback when devices selected.
    getRej( ) -> None:
        Callback when operation canceled.

    """
    def __init__(self, parent=None):
        super( QtWidgets.QDialog, self ).__init__( parent=parent )
        iconpath = os.path.join( os.path.dirname( os.path.realpath( __file__ ) ), "icon.png" )
        self.setWindowIcon( QtGui.QIcon( iconpath ) )
        self.setupUI( self, None )
        self.okButton.accepted.connect( self.getSelected )
        self.okButton.rejected.connect( self.getRej )
        self.val = None

    def getSelected(self) -> None:
        """
        Callback when devices selected.
        """
        currDate = QtCore.QDate().currentDate()
        d2s = currDate.daysTo( self.calendar.s_date if self.calendar.s_date else currDate )
        d2e = currDate.daysTo( self.calendar.e_date if self.calendar.e_date else currDate )

        d_low   = min( min( d2s, d2e ), -1 )
        d_high  = max( max( d2s, d2e ),  0 )

        self.val = f"$st_d{ abs( d_low ) }$et_d{ abs( d_high ) }"
        self.close()

    def getRej(self) -> None:
        """
        Callback when operation canceled.
        """
        self.val = None
        self.close()
        
def Dialog():
    """
    Dialog box wrapper for date selection form.

    Returns
    -------
    str | None
        Selected date.

    """
    app = QtWidgets.QApplication( [] )
    dialog = CDateSelectForm()
    dialog.exec()
    return dialog.val


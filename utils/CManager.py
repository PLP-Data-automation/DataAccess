"""
Author: Fuentes Juvera, Luis
E-mail: luis.fuju@outlook.com
username: LuisDFJ

CManager Module: High-level abstraction for accessing m2web resources.

CManager uses Mid-Level abstraction and forms to set a session and prompt
the selection panels for accessing the ewon devices.

Classes
-------
CManager( path : str, url : str ) 

"""
from DataAccess.utils.CQuery       import CQuery
from DataAccess.utils.CQueryCore   import CQueryCore
from DataAccess.utils.CCredentials import CCredentials
from DataAccess.utils.CTableUtils  import CTableUtils
from DataAccess.utils.CEwonSelectForm  import Dialog as selectDialog
from DataAccess.utils.CLogForm         import Dialog as logDialog
from DataAccess.utils.CLogInForm       import Dialog as loginDialog
from DataAccess.utils.CCredentialsForm import Dialog as credDialog
from DataAccess.utils.CDateSelectForm  import Dialog as dateDialog

import os
import pandas

class CManager(CQueryCore):
    """
    CManager Module: High-level abstraction for accessing m2web resources.

    CManager uses Mid-Level abstraction and forms to set a session and prompt
    the selection panels for accessing the ewon devices.

    Attributes
    ----------
    path : str
        Path for dumping credentials.
    cred : CCredentials
        Credential manager object.
    key : str
        Credentials encryption password.
    
    Methods
    -------
    getLogIn(self, path : str) -> None
        Log In abstraction.
    getCredentials(self, key : str, mode : bool=True ) -> dict
        getCredentials from credentials manager.
    selectewon( self, ewons : dict ) -> list
        Select Ewon abstraction.
    ewons(self) -> dict
        getewons() mid-level wrapper.
    getTable(self, AST_Param : str, date_dialog : bool=True ) -> pandas.DataFrame
        Get Table wrapper.


    """
    def __init__(self, path : str, url : str="https://m2web.talk2m.com/"):
        """
        CManager Module: High-level abstraction for accessing m2web resources.

        Parameters
        ----------
        path : str
            Path for dumping credentials.
        url : str
            m2web REST API Domain.
        """
        super().__init__( url=url )
        self.path = path

    def getLogIn(self, path : str) -> None:
        """
        Log In abstraction.

        Promps credential manager forms, for creating or loading
        a credential bundle. Save credential bundle in key, cred

        Parameters
        ----------
        path : str
            Path to dump credentials.
        """
        mode = logDialog()
        if mode == "load":
            password, credpath = loginDialog( path )
            cred = CCredentials( credpath )
        elif mode == "new":
            credentials, password, credpath = credDialog()
            credpath = os.path.join( path, credpath )
            cred = CCredentials( credpath )
            cred.dump( password, credentials )
        self.key    = password
        self.cred   = cred

    def getCredentials(self, key : str, mode : bool=True ) -> dict:
        """
        getCredentials from credentials manager.

        Credntials decrypted from manager using key. Mode selects
        type of credentials to gather.

        Parameters
        ----------
        key : str
            Credentials password.
        mode : bool
            Select if account credentials [true] or
            device credentials [false]
        
        Returns
        -------
        dict
            Credentials deencrypted.

        """
        params = self.cred.load( key )
        credentials = {}
        device_credentials = {}
        for token in params.keys():
            if token in [ "t2maccount", "t2musername", 't2mpassword', 't2mdeveloperid' ]:
                credentials[ token ] = params[ token ]
            elif token in ['t2mdeviceusername', 't2mdevicepassword']:
                device_credentials[ token ] = params[ token ]
        if mode:
            return credentials
        else:
            return device_credentials

    def selectewon( self, ewons : dict ) -> list:
        """
        Select Ewon abstraction.

        Promps devices on a selectable form. Encodes the selections
        on a dictionary.

        Parameters
        ----------
        ewon : dict
            Dictionary of available ewons.
            { "<name>": { "id": ..., "encodedName": ... }, ... }
        
        Returns
        -------
        list
            List of selected ewons.
            [ { "id": ..., "encodedName": ... }, ... ]

        """
        ewon_names = list( ewons.keys() )
        selected_ewons = []
        for ewon_name in selectDialog( ewon_names ):
            selected_ewons.append( ewons.get( ewon_name, {} ) )
        return selected_ewons

    def ewons(self) -> dict:
        """
        getewons() mid-level wrapper.

        Gets complete ewons list. Format to per name dictionary
        structure:
            { "<name>": { 
                "id": ...,
                "encodedName": ...
                }, 
              ...
            }

        Returns
        -------
        dict
            Dictionary of available ewons.
            { "<name>": { "id": ..., "encodedName": ... }, ... }
        
        """
        ewons_dict = self.getewons()
        ewons = {}
        if ewons_dict != None:
            for ewon in ewons_dict.get( "ewons", [] ):
                ewons[ ewon["name"] ] = { 
                    'id':           ewon["id"], 
                    'encodedName':  ewon["encodedName"],
                    'm2webServer':  "https://{}/".format( ewon["m2webServer"] )
                }
        return ewons

    def getTable(self, AST_Param : str, date_dialog : bool=True ) -> pandas.DataFrame:
        """
        Get Table wrapper.

        Lowlevel call to getTable on each selected device (CQuery type).

        Parameters
        ----------
        AST_Param : str
            Data Table format for m2web api.
        date_dialog : bool
            Prompt date form.

        Returns
        -------
        pandas.DataFrame
            Combines tables from different sources.

        """
        if date_dialog: AST_Param = f"{AST_Param}{dateDialog()}"
        data_frames = {}
        for device in self.devices:
            with device:
                df = device.getTable( AST_Param )
            name = device.ewon.get("encodedName", "" )
            data_frames[ name ] = df
        
        tableUtil = CTableUtils()
        return tableUtil.combine_tables( data_frames )

    def __enter__(self):
        print( "Loggin In " )
        self.getLogIn( self.path )
        self.login( self.getCredentials( self.key ) )
        
        selected_ewons = self.selectewon( self.ewons() )
        
        self.devices = []
        for ewon in selected_ewons:
            target_domain = ewon.get( "m2webServer", None )
            if target_domain != None:
                self.devices.append( CQuery( self.cred, self.key, ewon, url=target_domain ) )

        return self
        

    def __exit__(self, exc_type, exc_value , exc_traceback):
        print( "Loggin Out" )
        self.key = None
        self.logout()


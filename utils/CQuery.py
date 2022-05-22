"""
Author: Fuentes Juvera, Luis
E-mail: luis.fuju@outlook.com
username: LuisDFJ

CQuery Module: Mid-level abstraction for accessing Ewon devices.

Classes
-------
CQuery( cred : CCredentials, key : str, ewon : dict, url : str="https://m2web.talk2m.com/")

"""
from utils.CQueryCore import CQueryCore
from utils.CCredentials import CCredentials
import pandas

class CQuery(CQueryCore):
    """
    CQuery Module: Mid-level abstraction for accessing Ewon devices.

    Attributes
    ----------
    cred : CCredentials
        Credential manager object.
    key : str
        Credentials encryption password.
    ewon : dict
        Ewon device dictionary.

    Methods
    -------
    getCredentials( key : str, mode : bool=True ) -> dict
        getCredentials from credentials manager.
    getTable( AST_Param : str ) -> pandas.DataFrame
        Get table with AST format.


    """
    def __init__(self, cred : CCredentials, key : str, ewon : dict, url : str="https://m2web.talk2m.com/"):
        """
        Query for getting ewon data.

        Parameters
        ----------
        cred : CCredentials
            Credential manager object.
        key : str
            Credentials encryption password.
        ewon : dict
            Ewon device dictionary.
        url : str
            m2web REST API domain.
        """
        super().__init__( url=url )
        self.cred = cred
        self.key = key
        self.ewon = ewon

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

    def getTable(self, AST_Param : str ) -> pandas.DataFrame:
        """
        Get table with AST format.

        Parameters
        ----------
        AST_Param : str
            Table format.

        Returns
        -------
        pandas.DataFrame

        """
        params = { "AST_Param": AST_Param }
        params.update( self.getCredentials( self.key, False ) )
        return self.getdata( self.ewon, params )

    def __enter__(self):
        print( "Loggin In - {}".format( self.ewon.get( "encodedName", "" ) ) )
        self.login( self.getCredentials( self.key ) )
        return self
        

    def __exit__(self, exc_type, exc_value , exc_traceback):
        print( "Loggin Out" )
        self.key = None
        self.logout()


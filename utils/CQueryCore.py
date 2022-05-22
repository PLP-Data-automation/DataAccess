"""
Author: Fuentes Juvera, Luis
E-mail: luis.fuju@outlook.com
username: LuisDFJ

CQueryCore Module: Low-level abstraction for m2web REST API.

CQueryCore manages sessions and API calls: getInfo, getEwons,
getData. Main Domain is set to "https://m2web.talk2m.com/".
Some devices may use their region-specific domain.

Classes
-------
CQueryCore( )

"""

import requests
import pandas as pd
from io import StringIO
from functools import reduce
from urllib.parse import urljoin

class CQueryCore(object):
    """
    CQueryCore Module: Low-level abstraction for m2web REST API.

    CQueryCore manages sessions and API calls: getInfo, getEwons,
    getData. Main Domain is set to "https://m2web.talk2m.com/".
    Some devices may use their region-specific domain.

    Attributes
    ----------
    DOMAIN_URL : str
        m2web API domain
    LOGIN : str
        API path for login
    LOGOUT : str
        API path for logout
    GETINFO : str
        API path for getInfo
    GETEWONS : str
        API path for getEwons
    GETDATA : str
        API path for getData
    BINFILE : str
        Default historical log path.
    session : str
        Session number
    devid : str
        Developer id number

    Methods
    -------
    getSessionParams() -> dict
        Get current session params. Session and Dev ID.
    login(params : dict) -> None
        LogIn API call.
    logout() -> None
        LogOut API call.
    getinfo() -> None
        Get Info API call.
    getewons() -> None
        Get Ewons API call.
    getdata( ewon : dict, params : dict) ->  pd.DataFrame
        Get Data API call.
    """
    def __init__(self, url : str="https://m2web.talk2m.com/"):
        """
        Constructor of CQueryCore

        Parameters
        ----------
        url : str
            Default "https://m2web.talk2m.com/".m2web API domain.
        
        """
        self.DOMAIN_URL = url
        self.LOGIN      = "t2mapi/login"
        self.LOGOUT     = "t2mapi/logout"
        self.GETINFO    = "t2mapi/getaccountinfo"
        self.GETEWONS   = "t2mapi/getewons"
        self.GETDATA    = "t2mapi/get/"
        self.BINFILE    = "rcgi.bin/ParamForm"
        
        self.session    = None
        self.devid      = None

    def getSessionParams(self) -> dict:
        """
        Get current session params. Session and Dev ID.
        """
        return { "t2msession": self.session, "t2mdeveloperid": self.devid }

    def _query( self, api : str, params : dict ) -> dict:
        url     = urljoin( self.DOMAIN_URL, api )
        res     = requests.post( url, data=params )
        jres    = res.json()
        return jres

    def login(self, params : dict) -> None:
        """
        LogIn API call.

        Creates a session number if login succeded.

        Parameters
        ----------
        params : dict
            Credentials in dictionary format.
            { "t2maccount": ..., "t2musername: ... }
        """
        jres    = self._query( self.LOGIN, params )
        if jres.get( "success", False ):
            self.session    = jres.get( "t2msession", None )
            self.devid      = params.get( "t2mdeveloperid", None )
        else:
            self.session = None
            self.devid   = None

    def logout(self) -> None:
        """
        LogOut API call.

        Closes session if session has been created.

        """
        if self.session != None and self.devid != None:
            jres    = self._query( self.LOGOUT, self.getSessionParams() )
            if jres.get( "success", False ):
                print( "Successful LogOut" )
                self.session = None
                self.devid   = None

    def getinfo(self) -> None:
        """
        Get Info API call.

        Gathers account information, available pools, acounts, etc.

        """
        if self.session != None and self.devid != None:
            jres    = self._query( self.GETINFO, self.getSessionParams() )
            if jres.get( "success", False ):
                return jres
            else:
                return None
                
    def getewons(self) -> None:
        """
        Get Devices API call.

        Gathers active devices information: Domain, state, name.

        """
        if self.session != None and self.devid != None:
            jres    = self._query( self.GETEWONS, self.getSessionParams() )
            if jres.get( "success", False ):
                return jres
            else:
                return None
    
    def getdata(self, ewon : dict, params : dict) ->  pd.DataFrame:
        """
        Get Data API call.

        Gathers historical data and saves it in a DataFrame.

        Parameters
        ----------
        ewon : dict
            Dictionary with devices info.
        params : dict
            Dictionary with credentials and query type.

        Returns
        -------
        pandas.DataFrame

        """
        name    = "{}/".format( ewon.get( "encodedName", "" ) )
        url     = reduce( urljoin, [self.DOMAIN_URL, self.GETDATA, name, self.BINFILE ] )
        param   = {}
        param.update( self.getSessionParams() )
        param.update( params )
        res     = requests.post( url, data=param )
        data    = StringIO( res.text )
        df      = pd.read_csv( data, delimiter=";" )
        return df
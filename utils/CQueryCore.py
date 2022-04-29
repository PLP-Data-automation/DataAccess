from functools import reduce
import requests
from urllib.parse import urljoin
import pandas as pd
from io import StringIO

class CQueryCore(object):
    def __init__(self, url="https://m2web.talk2m.com/"):
        self.DOMAIN_URL = url
        self.LOGIN      = "t2mapi/login"
        self.LOGOUT     = "t2mapi/logout"
        self.GETINFO    = "t2mapi/getaccountinfo"
        self.GETEWONS   = "t2mapi/getewons"
        self.GETDATA    = "t2mapi/get/"
        self.BINFILE    = "rcgi.bin/ParamForm"
        
        self.session    = None
        self.devid      = None

    def getSessionParams(self):
        return { "t2msession": self.session, "t2mdeveloperid": self.devid }

    def _query( self, api, params ):
        url     = urljoin( self.DOMAIN_URL, api )
        res     = requests.post( url, data=params )
        jres    = res.json()
        return jres

    def login(self, params):
        jres    = self._query( self.LOGIN, params )
        if jres.get( "success", False ):
            self.session    = jres.get( "t2msession", None )
            self.devid      = params.get( "t2mdeveloperid", None )
        else:
            self.session = None
            self.devid   = None

    def logout(self):
        if self.session != None and self.devid != None:
            jres    = self._query( self.LOGOUT, self.getSessionParams() )
            if jres.get( "success", False ):
                print( "Successful LogOut" )
                self.session = None
                self.devid   = None

    def getinfo(self):
        if self.session != None and self.devid != None:
            jres    = self._query( self.GETINFO, self.getSessionParams() )
            if jres.get( "success", False ):
                return jres
            else:
                return None
                
    def getewons(self):
        if self.session != None and self.devid != None:
            jres    = self._query( self.GETEWONS, self.getSessionParams() )
            if jres.get( "success", False ):
                return jres
            else:
                return None
    
    def getdata(self, ewon, params):
        name    = "{}/".format( ewon.get( "encodedName", "" ) )
        url     = reduce( urljoin, [self.DOMAIN_URL, self.GETDATA, name, self.BINFILE ] )
        param   = {}
        param.update( self.getSessionParams() )
        param.update( params )
        res     = requests.post( url, data=param )
        data    = StringIO( res.text )
        df      = pd.read_csv( data, delimiter=";" )
        return df
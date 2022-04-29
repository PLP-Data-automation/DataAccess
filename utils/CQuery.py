from utils.CQueryCore import CQueryCore
from utils.CCredentials import CCredentials
from utils.CEwonSelectForm import Dialog as selectDialog
from utils.CLogForm import Dialog as logDialog
from utils.CLogInForm import Dialog as loginDialog
from utils.CCredentialsForm import Dialog as credDialog

import os

class CQuery(CQueryCore):
    def __init__(self, path, url="https://m2web.talk2m.com/"):
        super().__init__( url=url )
        self.path = path

    def getLogIn(self, path):
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

    def getCredentials(self, key, mode=True ):
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

    def selectewon( self, ewons ):
        ewon_names = list( ewons.keys() )
        ewon_name = selectDialog( ewon_names )
        selected_ewon = ewons.get( ewon_name, {} )
        return selected_ewon

    def ewons(self):
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

    def getTable(self, AST_Param ):
        params = { "AST_Param": AST_Param }
        params.update( self.getCredentials( self.key, False ) )
        return self.getdata( self.selected_ewon, params )

    def __enter__(self):
        print( "Loggin In " )
        self.getLogIn( self.path )
        self.login( self.getCredentials( self.key ) )
        self.selected_ewon = self.selectewon( self.ewons() )
        target_domain = self.selected_ewon.get( "m2webServer", None )
        if target_domain != None:
            if  target_domain != self.DOMAIN_URL:
                self.logout()
                self.DOMAIN_URL = target_domain
                self.login( self.getCredentials( self.key ) )
        else:
            self.logout()
        return self
        

    def __exit__(self, exc_type, exc_value , exc_traceback):
        print( "Loggin Out" )
        self.key = None
        self.logout()


from ast import AST
from utils.CQuery import CQuery
from utils.CQueryCore import CQueryCore
from utils.CCredentials import CCredentials
from utils.CTableUtils import CTableUtils
from utils.CEwonSelectForm import Dialog as selectDialog
from utils.CLogForm import Dialog as logDialog
from utils.CLogInForm import Dialog as loginDialog
from utils.CCredentialsForm import Dialog as credDialog
from utils.CDateSelectForm import Dialog as dateDialog

import os

class CManager(CQueryCore):
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
        selected_ewons = []
        for ewon_name in selectDialog( ewon_names ):
            selected_ewons.append( ewons.get( ewon_name, {} ) )
        return selected_ewons

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

    def getTable(self, AST_Param, date_dialog=True ):
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


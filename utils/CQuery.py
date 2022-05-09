from utils.CQueryCore import CQueryCore

class CQuery(CQueryCore):
    def __init__(self, cred, key, ewon, url="https://m2web.talk2m.com/"):
        super().__init__( url=url )
        self.cred = cred
        self.key = key
        self.ewon = ewon

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

    def getTable(self, AST_Param ):
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


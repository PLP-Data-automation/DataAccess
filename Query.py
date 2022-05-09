import os 
import json
from utils.CManager import CManager
from utils.CTableUtils import CTableUtils


class Query( CManager ):
    def __init__(self, path, url="https://m2web.talk2m.com/"):
        super().__init__(path, url)

def filterTable( df ):
    col = "DISPONIBILIDAD"
    rows = []
    flag = False
    disponibility_1 = 0
    for i, row in df.iterrows():
        disponibility = row[ col ]
        if disponibility == 0 and flag: 
            if disponibility_1 == 100: rows.append( i - 2 )
            elif disponibility_1 > 0: rows.append( i - 1 )
        if disponibility != 0: flag = True
        disponibility_1 = disponibility
    
    rows = [i for i in rows if i >= 0]
    dt = df.iloc[rows]
    dt.reset_index( drop=True, inplace=True )
    return dt

def reduceTable( df ):
    config_path = os.path.join( os.path.dirname( os.path.realpath( __file__ ) ), "config.json" )
    with open( config_path, "r" ) as file:
        config = json.load( file )
    rcols = config.get( "columns-reduced", [] )
    util = CTableUtils()
    return util.reduce_table( df, rcols )

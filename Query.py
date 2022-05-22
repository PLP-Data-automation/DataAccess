"""
Author: Fuentes Juvera, Luis
E-mail: luis.fuju@outlook.com
username: LuisDFJ

Query Module: High-level abstraction for fetching IIoT Modules.

Classes
-------
Query( path : str, url : str )

Functions
---------
filterTable( df : pandas.DataFrame ) -> pandas.DataFrame
reduceTable( df : pandas.DataFrame ) -> pandas.DataFrame
run_query( mode : list = [ "full", "full-filter", "reduced", "reduced-filter" ] ) -> dict

"""

import os
import json
import pandas
from utils.CManager import CManager
from utils.CTableUtils import CTableUtils

LOCAL_PATH = os.path.join( os.path.dirname( os.path.realpath( __file__ ) ), "dump" )

class Query( CManager ):
    """
    Class used for fetching Ewon evices.

    Parameters
    ----------
    path : str
        Default LOCAL_PATH. Path to dump credentials.
    url : str
        Default https://m2web.talk2m.com/. Main domain pague.

    """
    def __init__(self, path=LOCAL_PATH, url="https://m2web.talk2m.com/"):
        super().__init__(path, url)


def filterTable( df : pandas.DataFrame, col : str = "DISPONIBILIDAD" ) -> pandas.DataFrame:
    """
    Function to filter results tables.

    Interates through the dataframe (df) and collects valid rows when
    end of shift is detected.

    Parameters
    ----------
    df : pandas.DataFrame
        Table as a DataFrame.
    col : str
        Default DISPONIBILIDAD. Column to detect end of shift.

    Returns
    -------
    pandas.DataFrame
        Filtered Table.

    """
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


def reduceTable( df : pandas.DataFrame ) -> pandas.DataFrame:
    """
    Function to reduce unnecessary columns on DataFrame.

    Reads desired columns on config.json file. Reduces current
    DataFrame to valid columns only.

    Parameters
    ----------
    df : pandas.DataFrame
        Table as a Dataframe

    Returns
    -------
    pandas.DataFrame
        Reduced Table

    """
    config_path = os.path.join( os.path.dirname( os.path.realpath( __file__ ) ), "config.json" )
    with open( config_path, "r" ) as file:
        config = json.load( file )
    rcols = config.get( "columns-reduced", [] )
    util = CTableUtils()
    return util.reduce_table( df, rcols )


def run_query( mode : list = [ "full", "full-filter", "reduced", "reduced-filter" ] ) -> dict:
    """
    Function wrapper to run Query and select type of output.

    Runs safely a Query object on $dtHT$ftT mode. Filters
    and reduces tables as requested.

    Parameters
    ----------
    mode : list
        Available modes: full, full-filter, reduced, reduced-filter.
        List of any desired mode.

    Returns
    -------
    dict
        Dict of DataFrames per mode.


    """
    try:
        with Query() as q:
            df = q.getTable( "$dtHT$ftT" )
    except Exception:
        print( "Closing program!" )

    fdf = filterTable( df )
    results = {}
    
    if "full" in mode:
        results[ "full" ] = df
    if "reduced" in mode:
        results[ "reduced" ] = reduceTable( df )
    if "full-filter" in mode:
        results[ "full-filter" ] = fdf
    if "reduced-filter" in mode:
        results[ "reduced-filter" ] = reduceTable( fdf )
    
    return results






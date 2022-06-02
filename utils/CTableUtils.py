"""
Author: Fuentes Juvera, Luis
E-mail: luis.fuju@outlook.com
username: LuisDFJ

CTableUtils Module: High-level abstraction for combining and reducing columns.

Main calls CTableUtils.reduce_table and CTableUtils.combine_table. Checks columns
that match on all tables. Reduce table to especified columns.

Classes
-------
CTableUtils( )

"""

import pandas
import numpy

class CTableUtils():
    """
    Table Utils for formating multi-source tables and reduce tables.

    Main calls CTableUtils.reduce_table and CTableUtils.combine_table. Checks columns
    that match on all tables. Reduce table to especified columns.

    Methods
    -------
    reduce_table( df : pandas.DataFrame, cols : list ) -> pandas.DataFrame
    combine_tables( data_frames : dict ) -> pandas.DataFrame

    """
    def __init__( self ):
        pass

    def reduce_table( self, df : pandas.DataFrame, cols : list, kcols : list = [] ) -> pandas.DataFrame:
        """
        Cuts columns not included in cols list.

        Appends LEGEND, TimeInt and TimeStr to the list of cols for metadata.

        Parameters
        ----------
        df : pandas.DataFrame
        cols : list
            List of desired columns. Do not include LEGEND, TimeInt or TimeStr
        kcols : list
            List of columns to strictly keep.
        Returns
        -------
        pandas.DataFrame

        """
        ncols = [ "LEGEND", "TimeInt", "TimeStr" ] + cols
        rcols = [ col.lower() for col in ncols ]
        common_cols = [ col for col in list( df.columns ) if col.lower() in rcols ]
        dt = df[ common_cols ]
        dt['TimeStr'] = pandas.to_datetime( dt['TimeInt'], unit='s' )
        for col in kcols:
            if col not in common_cols:
                dt[col] = numpy.nan
        return dt

    def combine_tables( self, data_frames : dict ) -> pandas.DataFrame:
        """
        Creates LEGEND columns in tables. Join matching columns.

        Parameters
        ----------
        data_frames : dict
            Dictionary of DataFrames with their LEGEND as key.
            { "Torcedora+2" : pandas.DataFrame, ... }
        
        Returns
        -------
        pandas.DataFrame
        
        """
        df_l = self._get_df_legend( data_frames )
        cols = self._get_common_cols( df_l )
        dfs = []
        for df in df_l:
            dfs.append( df[ cols ] )
        return pandas.concat( dfs )

    def _get_df_legend( self, data_frames ):
        dfs = []
        for name in data_frames.keys():
            df = data_frames[ name ]
            df.insert( 0, "LEGEND", [ name for _ in range( df.shape[0] ) ] )
            dfs.append( df )
        return dfs

    def _get_common_cols( self, dfs ):
        cols = [ list( df.columns ) for df in dfs ]
        ucols = []
        for col in cols:
            for item in col:
                if item not in ucols: ucols.append( item )
        fcols = []
        for item in ucols:
            flag = True
            for col in cols: 
                if item not in col: flag = False
            if flag: fcols.append( item )
        return fcols

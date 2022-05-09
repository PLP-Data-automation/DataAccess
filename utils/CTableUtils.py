import pandas

class CTableUtils():
    def __init__( self ):
        pass

    def reduce_table( self, df, cols ):
        ncols = [ "LEGEND", "TimeInt", "TimeStr" ] + cols
        rcols = [ col.lower() for col in ncols ]
        common_cols = [ col for col in list( df.columns ) if col.lower() in rcols ]
        return df[ common_cols ]

    def combine_tables( self, data_frames ):
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

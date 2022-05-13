#import sys
#sys.path.append( r"C:\projects\IIoT-PLP\DataLayer" )

from Query import Query, filterTable, reduceTable

try:
    with Query() as q:
        df = q.getTable( "$dtHT$ftT" )
        #df = f.getTable( "$dtHT$ftT$st_d3", False )
        #df = filterTable( f.getTable( "$dtHT$ftT" ) )
        #df = reduceTable( filterTable( f.getTable( "$dtHT$ftT" ) ) )
    #df.to_csv( "TORCEDORAS_FILTER.csv" )
    print( df )
except Exception:
    print( "Closing program!" )






#import sys
#sys.path.append( r"C:\projects\IIoT-PLP\DataLayer" )

#$st _s/m/h/d100
#$et _s/m/h/d0

from Query import Query, filterTable, reduceTable

with Query( r"C:\projects\IIoT-PLP\DataLayer\dump" ) as f:
    df = f.getTable( "$dtHT$ftT" )
    df = f.getTable( "$dtHT$ftT$st_d3", False )
    df = filterTable( f.getTable( "$dtHT$ftT" ) )
    df = reduceTable( filterTable( f.getTable( "$dtHT$ftT" ) ) )

print( df )



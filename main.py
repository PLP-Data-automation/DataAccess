#import sys
#sys.path.append( r"C:\projects\IIoT-PLP\DataLayer" )
#from Query import Query, filterTable

#$st _s/m/h/d100
#$et _s/m/h/d0
from Query import Query, filterTable

with Query( r"C:\projects\IIoT-PLP\DataLayer\dump" ) as f:
    #df = filterTable( f.getTable( "$dtHT$ftT$st_d3" ) )
    df = filterTable( f.getTable( "$dtHT$ftT$" ) )

df.to_csv( r".\table_f_s.csv" )
print( df )

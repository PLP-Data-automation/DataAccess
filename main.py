from DataAccess.Query import run_query
import time
import os

if not os.path.exists( "log" ):
  os.makedirs( "log" )

try:
    results = run_query()
    df_full         = results["full"]
    df_full_filter  = results["full-filter"]
    df_redu         = results["reduced"]
    df_redu_filter  = results["reduced-filter"]

    print( df_full )
    print( df_full_filter )
    print( df_redu )
    print( df_redu_filter )
    
    t = time.localtime()
    timestamp = time.strftime('%b-%d-%Y_%H%M', t)
    
    df_full.to_csv( f"log/Full_{timestamp}.csv" )
    df_full_filter.to_csv( f"log/Full_Filter_{timestamp}.csv" )
    df_redu.to_csv( f"log/Reduced_{timestamp}.csv" )
    df_redu_filter.to_csv( f"log/Reduced_Filter_{timestamp}.csv" )

    print( timestamp )

except UnboundLocalError:
    print( "Loading failed!" )
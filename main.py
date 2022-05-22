"""
Author: Fuentes Juvera, Luis
E-mail: luis.fuju@outlook.com
username: LuisDFJ

Example usage: High-level abstraction for fetching IIoT Modules.

Running modes: full, full-filter, reduced, reduced-filter.
Saving results on ./log/Full_%b_%d_%Y_%H%M.csv ... 

"""

from DataAccess.Query import run_query
import time
import os

if __name__ == "__main__":
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
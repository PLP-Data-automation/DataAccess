from DataAccess.Query import run_query

results = run_query()
df_full         = results["full"]
df_full_filter  = results["full-filter"]
df_redu         = results["reduced"]
df_redu_filter  = results["reduced-filter"]

print( df_full )
print( df_full_filter )
print( df_redu )
print( df_redu_filter )
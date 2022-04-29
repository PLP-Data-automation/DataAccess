from utils.CQuery import CQuery

class Query( CQuery ):
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


from_tname='processed_tomography_data'
from_sname='isa'
to_tname='Processed_Tomography_Data'
to_sname='Beta_Cell'

def move_table(catalog,f,t, exclude=[], post=False):
    sys_cols=['RID','RCT','RCB','RMB','RMT']
    from_sname,from_tname = f
    to_sname,to_tname = t

    from_cols = [i.name  for i in catalog.getCatalogModel().schemas[from_sname].tables[from_tname].column_definitions
                 if not (i.name in sys_cols or i.name in exclude) ]
    to_cols =[i.name  for i in catalog.getCatalogModel().schemas[to_sname].tables[to_tname].column_definitions if not i.name in sys_cols]

    from_cols.sort()
    to_cols.sort()

    print(from_cols)
    print(to_cols)

    map_uri='RID,RCT,RCB'
    for f,t in zip(from_cols,to_cols):
        map_uri+= ',{}:={}'.format(t,f)

    data = catalog.get('/attribute/{}:{}/'.format(from_sname,from_tname) + map_uri).json()
    if post:
        catalog.post("/entity/{}:{}?nondefaults=RID,RCT,RCB".format(to_sname,to_tname), json=data)
    return


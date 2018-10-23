import requests
import re


def is_pure_binary(table):
    """
    Check to see if the table has the propoerties of a pure binary association.  That is it only has two foreign keys:
      1. It only has two foreign keys,
      2. There is a uniqueness constraint on the two keys.
      3. NULL values are not allowed in the foreign keys.
    :param table:
    :return:
    """
    # table has only two foreign_key constraints.
    if len(table.foreign_keys) != 2:
        return False

    # Each constraint is over only one column.
    if len(table.foreign_keys[0].foreign_key_columns) != 1:
        return False
    if len(table.foreign_keys[1].foreign_key_columns) != 1:
        return False

    fk0 = table.foreign_keys[0].foreign_key_columns[0]['column_name']
    fk1 = table.foreign_keys[1].foreign_key_columns[0]['column_name']
    c = False

    # There is a uniqeness constraint on the pair of fkey columns.
    for i in table.keys:
        if fk0 in i.unique_columns and fk1 in i.unique_columns:
            c = True
    if not c:
        return False

    # Null is not allowed on the column.
    if table.column_definitions[fk0].nullok:
        return False
    if table.column_definitions[fk1].nullok:
        return False

    return True


def get_collection(catalog, rid):
    model_root = catalog.getCatalogModel()
    tables = {}
    collection = rid_to_table(catalog, rid)
    for fk in collection.referenced_by:
        atable = model_root.schemas[fk.sname].tables[fk.tname]
        if is_pure_binary(atable):
            print('assocation table {}:{}'.format(fk.sname, fk.tname))
            out_fkey = atable.foreign_keys[1]
            print(out_fkey.referenced_columns)
            sname = out_fkey.referenced_columns[0]['schema_name']
            tname = out_fkey.referenced_columns[0]['table_name']
            if sname == collection.sname and tname == collection.name:
                out_fkey = atable.foreign_keys[0]
                sname = out_fkey.referenced_columns[0]['schema_name']
                tname = out_fkey.referenced_columns[0]['table_name']
            target_table = model_root.schemas[sname].tables[tname]
            print('target table', target_table.name)
            tables[sname + ':' + tname] = catalog.getPathBuilder().schemas[sname].tables[tname].entities()
        else:
                print('not atable')
    return tables


RID_regex = '([A-Za-z0-9]{1,4})(-[A-Za-z0-9]{4,4})*(@([A-Za-z0-9]{1,4})(-[A-Za-z0-9]{4,4})*)?'
snapshot_regex = '@([A-Za-z0-9]{1,4})(-[A-Za-z0-9]{4,4})*)?'
catalog_regex = '/catalog/(?P<catalog_id>[0-9]+)((@(?P<snapshot_id>([A-Za-z0-9]{1,4})(-[A-Za-z0-9]{4,4})*))?)/entity/(?P<schema>.+):(?P<table>.+)/'


def rid_to_table(catalog, rid_url):
    # Go to the resolver and get the id record.
    r = requests.get(rid_url, allow_redirects=False)
    url = r.headers['location']

    # Parse up the URL to pull out the table and schema name.
    s = re.search(catalog_regex, url)
    return catalog.getCatalogModel().schemas[s['schema']].tables[s['table']]

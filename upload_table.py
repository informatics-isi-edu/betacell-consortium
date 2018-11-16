from goodtables import validate
from deriva_csv import table_schema_from_catalog

def validate_table(table_loc, server, catalog_id, schema_name, table_name):
    table_schema = table_schema_from_catalog(server, catalog_id, schema_name, table_name)

    report = validate('invalid.csv', schema=table_schema_from_catalog(server, catalog_id, schema_name, table_name)

    if report['valid']:

    return
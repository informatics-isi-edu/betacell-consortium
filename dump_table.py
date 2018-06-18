from deriva.core import HatracStore, ErmrestCatalog, ErmrestSnapshot, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
import re

# Simple helper routines to dump the current contents of a table.

def dump_table(table):
        tab = {
            'display' : table.display,
            'table_display' : table.table_display
        }
        return tab

def dump_foreign_keys(table):
    fks =  [
        {
            'foreign_key_columns': [ c['column_name'] for c in i.foreign_key_columns],
            'pk_schema': i.referenced_columns[0]['schema_name'],
            'pk_table': i.referenced_columns[0]['table_name'],
            'pk_columns': [ c['column_name'] for c in i.referenced_columns],
            'constraint_names': i.names,
            'annotations': i.annotations,
            'on_update' : i.on_update, 'on_delete': i.on_delete,
            'comment': i.comment
        } for i in table.foreign_keys
    ]
    return fks

def dump_keys(table):
    keys = [
        {
            'key_columns': i.unique_columns,
            'names': i.names,
            'annotations': i.annotations,
            'comment': i.comment
        } for i in table.keys
    ]
    return keys

def dump_columns(table):
    cols = [
        {
            'name' : i.name,
            'type' : { 'typename': i.type.typename, 'is_array': i.type.is_array},
            'nullok': i.nullok,
        'annotations' : i.annotations
        }
    for i in table.column_definitions
    ]
    return cols

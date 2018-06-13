%load_ext autoreload
%autoreload 2

from deriva.core import HatracStore, ErmrestCatalog, ErmrestSnapshot, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
import em.builtin_types as typ
import csv
import re


from bdbag import bdbag_api as bdb

def create_column_and_make_visible(catalog, table, col_def):
    # add the column on the server
    new_col = table.create_column(catalog, col_def)

    table.visible_columns["entry"].append(col_def['name'])
    table.visible_columns["*"].append(col_def['name'])
    table.apply(catalog)
    return new_col


def delete_column(catalog,table,col_def):
    # delete column from the table
    # Remove column from visible columns list if it was there
    return

def create_fkey_column_and_make_visible(catalog, table, col_def, domain_table, domain_col):
 """Create a column which is a simple foreign key and make it visible.

    Parameters:
      catalog: ErmrestCatalog instance
      table: ermrest_model.Table instance to which we will add a column
      col_def: as from ermrest_model.Column.define()
      domain_table: ermrest_column.Table instance
      domain_col: ermrest_column.Column instance found in domain_table

    A new column will be added to table based on col_def and then
    constrained as a foreign key referencing domain_col which must be
    a simple key in domain_table.

    Visible column and visible foreign key annotations will be
    adjusted to make the new linkage visible from both tables.

    Returns:
      (new_col, new_fkey)

 """
 # make sure domain_col is really a key
 domain_key = None
 for key in domain_table.keys:
   if key.unique_columns == [domain_col.name]:
     domain_key = key
     break
 assert domain_key is not None

 # add the column on the server
 new_col = table.create_column(catalog, col_def)

 # now add the foreign key reference constraint on the server
 fkey_def = ermrest_model.ForeignKey.define(
   [new_col.name],
   domain_table.sname,
   domain_table.tname,
   [domain_col],
   on_update='CASCADE',
   on_delete='SET NULL',
   constraint_name=[ [table.sname, "%s_%s_fkey" % (table.name, new_col.name)] ],
 )
 new_fkey = table.create_fkey(catalog, fkey_def)

 # now extend visible columns for the modified table
 if table.visible_columns:
   for context, config in table.visible_columns.items():
     if context == "filter":
       # we need to access child list of faceting conjunction
       config = config["and"]
       config.append(
         {
           "source": [ new_fkey.names[0], "RID" ],
           "entity": True,
           "markdown_name": new_col.name
         }
       )
     else:
       config.append( new_fkey.names[0] )
   table.apply(catalog)

 # now extend visible foreign keys on the referenced table
 if domain_table.visible_foreign_keys:
   for context, config in domain_table.visible_foreign_keys.items():
     config.append( new_fkey.names[0] )
   domain_table.apply(catalog)

 return new_col, new_fkey


model_root = catalog.getCatalogModel()

experiment = model_root.table('isa', 'experiment')
biosample = model_root.table('isa', 'biosample')
dataset = model_root.table('isa', 'dataset')

for i in ['histone_modification', 'strandedness', 'rnaseq_selection', 'molecule_type']
delcolumn = experiment.column_definitions['histone_modification']
delcolumn.delete(catalog, table = experiment)
delcolumn = experiment.column_definitions['strandedness']
delcolumn.delete(catalog, table = experiment)


column_def = em.Column.define(
    "capillary_number",
    em.builtin_types.int2,
    nullok=False,
    comment="ID number of the capillary constaining the biosample.",
    annotations={},
    acls={},
    acl_bindings={},
)

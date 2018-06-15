%load_ext autoreload
%autoreload 2

from deriva.core import HatracStore, ErmrestCatalog, ErmrestSnapshot, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
import re

def create_column_and_make_visible(catalog, table, col_def):
    # add the column on the server
    new_col = table.create_column(catalog, col_def)

    table.visible_columns["entry"].append(col_def['name'])
    table.visible_columns["*"].append(col_def['name'])
    table.apply(catalog)
    return new_col


def create_fkey_column_and_make_visible(catalog, table, col_def, domain_table, domain_col):
 """Create a column which is a simple foreign key and make it visible.

    Parameters:
      catalog: ErmrestCatalog instance
      table: ermrest_model.Table instance to which we will add a column
      col_def: as from ermrest_model.Column.define)
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

server = 'pbcconsortium.isrd.isi.edu'
credential = get_credential(server)
catalog = ErmrestCatalog('https', server, 1, credentials=credential)
model_root = catalog.getCatalogModel()

experiment = model_root.table('isa', 'experiment')
biosample = model_root.table('isa', 'biosample')
dataset = model_root.table('isa', 'dataset')
protocol = model_root.table('isa','protocol')
replicate = model_root.table('isa','replicate')
imaging_data = model_root.table('isa','imaging_data')

pb = catalog.getPathBuilder()
isa = pb.isa
pbexperiment = isa.experiment
pbbiosample = isa.biosample
pbdataset = isa.dataset
pbprotocol = isa.protocol


capillary_column_def = em.Column.define(
    "capillary_number", em.builtin_types.int2, nullok=True,
    comment="ID number of the capillary constaining the biosample."

)

bead_column_def = em.Column.define(
    "sample_position", em.builtin_types.int2, nullok=True,
    comment="Position in the capillary where the sample is located."
)

create_column_and_make_visible(catalog, biosample, capillary_column_def)
create_column_and_make_visible(catalog, biosample, bead_column_def)

# Protocol
treatment = em.Column.define(
    "treatment", em.builtin_types.text, nullok=True,
    comment="Treatment applied to a cell line."
)

treatment_concentration = em.Column.define(
    "treatment_concentration", em.builtin_types.float4, nullok=True,
    comment="Concentration of treatment applied to a cell line in mM."
)

timepoint = em.Column.define(
    "timepoint", em.builtin_types.int2, nullok=True,
    comment="Measured in minutes."
)

#delcolumn = protocol.column_definitions['chromatin_modifier']
#delcolumn.delete(catalog, table = protocol)

protocol.create_column(catalog, treatment)
protocol.create_column(catalog, treatment_concentration)
protocol.create_column(catalog, timepoint)

protocol.visible_columns['entry'] = ['RID', 'name', 'treatment', 'treatment_concentration', 'timepoint', 'protocol_url', 'description', 'file_url', 'filename']
protocol.visible_columns['detailed'] = [
    ['isa', 'protocol_pkey'],
    'name',
    'treatment'
    'treatment_concentration',
    'timepoint',
    'protocol_url',
    'description',
    'file_url',
    'filename',
    'byte_count',
    'submitted_on',
    'md5']
protocol.apply(catalog)


# Create the xray-tomography table


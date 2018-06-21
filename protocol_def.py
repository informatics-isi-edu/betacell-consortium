column_defs = [
    em.Column.define(
    'name',{'typename': 'text', 'is_array': False},
    nullok=False,
    annotations={}
    comment='Provide a name that uniquely identifies the protocol'),
    em.Column.define(
    'protocol_url',{'typename': 'text', 'is_array': False},
    nullok=True,
    annotations={}
    comment=None),
    em.Column.define(
    'description',{'typename': 'markdown', 'is_array': False},
    nullok=True,
    annotations={}
    comment=None),
    em.Column.define(
    'file_url',{'typename': 'text', 'is_array': False},
    nullok=True,
    annotations={'tag:isrd.isi.edu,2017:asset': {'filename_column': 'filename', 'byte_count_column': 'byte_count', 'url_pattern': '/hatrac/commons/documents/protocol/{{{md5}}}', 'md5': 'md5'}}
    comment=None),
    em.Column.define(
    'filename',{'typename': 'text', 'is_array': False},
    nullok=True,
    annotations={}
    comment=None),
    em.Column.define(
    'byte_count',{'typename': 'int4', 'is_array': False},
    nullok=True,
    annotations={}
    comment=None),
    em.Column.define(
    'md5',{'typename': 'text', 'is_array': False},
    nullok=True,
    annotations={}
    comment=None),
    em.Column.define(
    'assay_ids',{'typename': 'int4[]', 'is_array': False},
    nullok=True,
    annotations={}
    comment=None),
    em.Column.define(
    'timepoint',{'typename': 'int2', 'is_array': False},
    nullok=True,
    annotations={}
    comment='Measured in minutes.'),
    em.Column.define(
    'treatment_concentration',{'typename': 'float4', 'is_array': False},
    nullok=True,
    annotations={}
    comment='Concentration of treatment applied to a cell line in mM.'),
    em.Column.define(
    'treatment',{'typename': 'text', 'is_array': False},
    nullok=True,
    annotations={}
    comment='Treatment applied to a cell line.'),
key_defs = [
    em.Key.define(
        ['name'],
        constraint_names=[('isa', 'protocol_name_key')],
        annotation={},
        comment=None),
    em.Key.define(
        ['description'],
        constraint_names=[('isa', 'protocol_description_key')],
        annotation={},
        comment=None),
    em.Key.define(
        ['RID'],
        constraint_names=[('isa', 'protocol_pkey')],
        annotation={},
        comment=None),
]

fkey_defs = [
]
table_annotations =
{   'tag:isrd.isi.edu,2016:visible-columns': {   'compact': [   [   'isa',
                                                                    'protocol_pkey'],
                                                                'name',
                                                                'treatment',
                                                                'treatment_concentration',
                                                                'timepoint',
                                                                'description'],
                                                 'detailed': [   [   'isa',
                                                                     'protocol_pkey'],
                                                                 'name',
                                                                 'treatment',
                                                                 'treatment_concentration',
                                                                 'timepoint',
                                                                 'description'],
                                                 'entry': [   'RID',
                                                              'name',
                                                              'treatment',
                                                              'treatment_concentration',
                                                              'timepoint',
                                                              'protocol_url',
                                                              'description',
                                                              'file_url',
                                                              'filename'],
                                                 'filter': {   'and': [   {   'entity': True,
                                                                              'markdown_name': 'Protocol '
                                                                                               'Name',
                                                                              'open': False,
                                                                              'source': 'name'},
                                                                          {   'entity': True,
                                                                              'markdown_name': 'Treatment',
                                                                              'open': False,
                                                                              'source': 'treatment'},
                                                                          {   'entity': True,
                                                                              'markdown_name': 'Treatment '
                                                                                               'Concentration',
                                                                              'open': False,
                                                                              'source': 'concentration'},
                                                                          {   'entity': True,
                                                                              'markdown_name': 'Treatment '
                                                                                               'Concentration',
                                                                              'open': False,
                                                                              'source': 'timepoint'},
                                                                          {   'entity': True,
                                                                              'markdown_name': 'Protocol '
                                                                                               'Description',
                                                                              'open': False,
                                                                              'source': 'description'}]}},
    'tag:isrd.isi.edu,2016:visible-foreign-keys': {   'detailed': [   [   'isa',
                                                                          'experiment_protocol_fkey']],
                                                      'entry': [   [   'isa',
                                                                       'experiment_protocol_fkey']]},
    'tag:misd.isi.edu,2015:display': {'name': 'Protocol'}}

table_def = em.Table.define(
  protocol,
  column_defs,
  key_defs=key_defs,
  fkey_defs=fkey_defs,
  comment=None,
  acls=acls,
  acl_bindings=acl_bindings,
  annotations=table_annotations,
  provide_system=True
)

server = 'pbcconsortium.isrd.isi.edu'
credential = get_credential(server)
catalog = ErmrestCatalog('https', server, 1, credentials=credential)
model_root = catalog.getCatalogModel()
schema = model_root.schemas[schema_name]
table = schema.create_table(catalog, table_def)


import argparse
    from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
    import deriva.core.ermrest_model as em
    
column_defs = [
    em.Column.define(
            'name',em.builtin_types.{'typename': 'text', 'is_array': False},
            nullok=False,
            annotations={}
            comment='Provide a name that uniquely identifies the protocol'),
    
    em.Column.define(
            'protocol_url',em.builtin_types.{'typename': 'text', 'is_array': False},
            nullok=True,
            annotations={}
            comment=None),
    
    em.Column.define(
            'description',em.builtin_types.{'typename': 'markdown', 'is_array': False},
            nullok=True,
            annotations={}
            comment=None),
    
    em.Column.define(
            'file_url',em.builtin_types.{'typename': 'text', 'is_array': False},
            nullok=True,
            annotations={'tag:isrd.isi.edu,2017:asset': {'filename_column': 'filename', 'byte_count_column': 'byte_count', 'url_pattern': '/hatrac/commons/documents/protocol/{{{md5}}}', 'md5': 'md5'}}
            comment=None),
    
    em.Column.define(
            'filename',em.builtin_types.{'typename': 'text', 'is_array': False},
            nullok=True,
            annotations={}
            comment=None),
    
    em.Column.define(
            'byte_count',em.builtin_types.{'typename': 'int4', 'is_array': False},
            nullok=True,
            annotations={}
            comment=None),
    
    em.Column.define(
            'md5',em.builtin_types.{'typename': 'text', 'is_array': False},
            nullok=True,
            annotations={}
            comment=None),
    
    em.Column.define(
            'assay_ids',em.builtin_types.{'typename': 'int4[]', 'is_array': False},
            nullok=True,
            annotations={}
            comment=None),
    
    em.Column.define(
            'timepoint',em.builtin_types.{'typename': 'int2', 'is_array': False},
            nullok=True,
            annotations={}
            comment='Measured in minutes.'),
    
key_defs = [
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
    em.Key.define(
                ['name'],
                constraint_names=[('isa', 'protocol_name_key')],
                annotation={},
                comment=None),
]

fkey_defs = [
]

table_annotations =
{   'tag:isrd.isi.edu,2016:visible-columns': {   'compact': [   [   'isa',
                                                                    'protocol_pkey'],
                                                                'name',
                                                                {   'aggregate': 'array',
                                                                    'entity': True,
                                                                    'markdown_name': 'Treatment',
                                                                    'source': [   {   'inbound': [   'isa',
                                                                                                     'protocol_treatment_protocol_fkey']},
                                                                                  {   'outbound': [   'isa',
                                                                                                      'protocol_treatment_treatment_fkey']},
                                                                                  'RID']},
                                                                {   'aggregate': 'array',
                                                                    'entity': True,
                                                                    'markdown_name': 'Concentration',
                                                                    'source': [   {   'inbound': [   'isa',
                                                                                                     'protocol_treatment_protocol_fkey']},
                                                                                  'treatment_concentration']},
                                                                {   'aggregate': 'array',
                                                                    'entity': True,
                                                                    'source': [   'timepoint']},
                                                                'description'],
                                                 'detailed': [   [   'isa',
                                                                     'protocol_pkey'],
                                                                 'name',
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
                                                                              'source': [   {   'inbound': [   'isa',
                                                                                                               'protocol_treatment_protocol_fkey']},
                                                                                            {   'outbound': [   'isa',
                                                                                                                'protocol_treatment_treatment_fkey']},
                                                                                            'RID']},
                                                                          {   'entity': True,
                                                                              'markdown_name': 'Treatment '
                                                                                               'Concentration',
                                                                              'open': False,
                                                                              'source': [   {   'inbound': [   'isa',
                                                                                                               'protocol_treatment_protocol_fkey']},
                                                                                            'treatment_concentration'],
                                                                              'ux_mode': 'choices'},
                                                                          {   'entity': True,
                                                                              'markdown_name': 'Timepoint',
                                                                              'open': False,
                                                                              'source': 'timepoint',
                                                                              'ux_mode': 'choices'},
                                                                          {   'entity': True,
                                                                              'markdown_name': 'Protocol '
                                                                                               'Description',
                                                                              'open': False,
                                                                              'source': 'description'}]}},
    'tag:isrd.isi.edu,2016:visible-foreign-keys': {   'detailed': [   [   'isa',
                                                                          'protocol_treatment_protocol_fkey'],
                                                                      [   'isa',
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

def main():
    parser = argparse.ArgumentParser(description='Load foreign key defs for table isa:protocol')
    parser.add_argument('--server', default='pbcconsortium.isrd.isi.edu',
                            help='Catalog server name')
    args = parser.parse_args()

    server = args.server
    schema_name = 'isa'
    table_name = 'protocol'

    credential = get_credential(server)
    catalog = ErmrestCatalog('https', server, 1, credentials=credential)
    model_root = catalog.getCatalogModel()
    schema = model_root.schemas[schema_name]
    table = schema.tables[table_name]

    table = schema.create_table(catalog, table_def)


if __name__ == "__main__":
        main()

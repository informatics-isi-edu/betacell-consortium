import argparse
    from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
    import deriva.core.ermrest_model as em
    
column_defs = [
    em.Column.define(
            'dataset',em.builtin_types.{'typename': 'text', 'is_array': False},
            nullok=False,
            annotations={}
            comment='None'),
    
    em.Column.define(
            'anatomy',em.builtin_types.{'typename': 'text', 'is_array': False},
            nullok=True,
            annotations={}
            comment='None'),
    
    em.Column.define(
            'device',em.builtin_types.{'typename': 'text', 'is_array': False},
            nullok=True,
            annotations={}
            comment='None'),
    
    em.Column.define(
            'equipment_model',em.builtin_types.{'typename': 'text', 'is_array': False},
            nullok=True,
            annotations={}
            comment='None'),
    
    em.Column.define(
            'description',em.builtin_types.{'typename': 'markdown', 'is_array': False},
            nullok=True,
            annotations={}
            comment='None'),
    
    em.Column.define(
            'url',em.builtin_types.{'typename': 'text', 'is_array': False},
            nullok=True,
            annotations={'tag:isrd.isi.edu,2017:asset': {'filename_column': 'filename', 'byte_count_column': 'byte_count', 'url_pattern': '/hatrac/commons/data/{{{_dataset}}}/{{{_replicate}}}/{{{filename}}}', 'md5': 'md5'}}
            comment='None'),
    
    em.Column.define(
            'filename',em.builtin_types.{'typename': 'text', 'is_array': False},
            nullok=True,
            annotations={'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '[**{{filename}}**]({{{url}}})'}, 'detailed': {'markdown_pattern': '[**{{filename}}**]({{{url}}})'}}}
            comment='None'),
    
    em.Column.define(
            'file_type',em.builtin_types.{'typename': 'text', 'is_array': False},
            nullok=True,
            annotations={'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '{{{$fkeys.isa.xray_tomography_data_file_type_fkey.rowName}}}'}}}
            comment='None'),
    
    em.Column.define(
            'byte_count',em.builtin_types.{'typename': 'int8', 'is_array': False},
            nullok=True,
            annotations={}
            comment='None'),
    
    em.Column.define(
            'submitted_on',em.builtin_types.{'typename': 'timestamptz', 'is_array': False},
            nullok=True,
            annotations={}
            comment='None'),
    
    em.Column.define(
            'md5',em.builtin_types.{'typename': 'text', 'is_array': False},
            nullok=True,
            annotations={}
            comment='None'),
    
    em.Column.define(
            'file_id',em.builtin_types.{'typename': 'int4', 'is_array': False},
            nullok=True,
            annotations={}
            comment='None'),
    
    em.Column.define(
            'replicate',em.builtin_types.{'typename': 'text', 'is_array': False},
            nullok=True,
            annotations={}
            comment='None'),
    
key_defs = [
    em.Key.define(
                ['RID', 'dataset'],
                constraint_names=[('isa', 'xray_tomography_data_dataset_RID_key')],
                annotation={},
                comment='RID and dataset must be distinct.'),
    em.Key.define(
                ['url'],
                constraint_names=[('isa', 'xray_tomography_data_url_key')],
                annotation={},
                comment='Unique URL must be provided.'),
    em.Key.define(
                ['RID'],
                constraint_names=[('isa', 'xray_tomography_data_RIDkey1')],
                annotation={},
                comment=None),
]

fkey_defs = [
    em.ForeignKey.define(
            ['dataset'],
            'isa', 'dataset', ['RID'],
            constraint_names = [('isa', 'xray_tomography_dataset_fkey')],
        acls = {'insert': ['*'], 'update': ['*']},
        on_update = 'CASCADE',
        on_delete = 'RESTRICT',
        comment = 'Must be a valid reference to a dataset.',
    ),
    em.ForeignKey.define(
            ['device'],
            'vocab', 'image_creation_device_terms', ['dbxref'],
            constraint_names = [('isa', 'xray_tomography_data_device_fkey')],
        acls = {'insert': ['*'], 'update': ['*']},
        on_update = 'CASCADE',
        on_delete = 'RESTRICT',
        comment = 'Must be a valid reference to a device.',
    ),
    em.ForeignKey.define(
            ['replicate', 'dataset'],
            'isa', 'replicate', ['RID', 'dataset'],
            constraint_names = [('isa', 'xray_tomography_data_replicate_fkey')],
        acls = {'insert': ['*'], 'update': ['*']},
        on_update = 'CASCADE',
        on_delete = 'RESTRICT',
        comment = 'Must be a valid reference to a dataset.',
    ),
    em.ForeignKey.define(
            ['equipment_model'],
            'vocab', 'instrument_terms', ['dbxref'],
            constraint_names = [('isa', 'xray_tomography_data_equipment_model_fkey')],
        acls = {'insert': ['*'], 'update': ['*']},
        on_update = 'CASCADE',
        on_delete = 'RESTRICT',
        comment = 'Must be a valid reference to a dataset.',
    ),
]

table_annotations =
{   'tag:isrd.isi.edu,2016:visible-columns': {   'compact': [   [   'isa',
                                                                    'xray_tomography_data_pkey'],
                                                                'replicate_fkey',
                                                                'url',
                                                                [   'isa',
                                                                    'xray_tomography_data_file_type_fkey'],
                                                                'byte_count',
                                                                'md5',
                                                                'submitted_on'],
                                                 'detailed': [   [   'isa',
                                                                     'xray_tomography_data_pkey'],
                                                                 [   'isa',
                                                                     'xray_tomography_data_dataset_fkey'],
                                                                 [   'isa',
                                                                     'xray_tomography_data_replicate_fkey'],
                                                                 [   'isa',
                                                                     'xray_tomography_data_device_fkey'],
                                                                 'filename',
                                                                 [   'isa',
                                                                     'xray_tomography_data_file_type_fkey'],
                                                                 'byte_count',
                                                                 'md5',
                                                                 'submitted_on'],
                                                 'entry': [   'RID',
                                                              [   'isa',
                                                                  'xray_tomography_data_replicate_fkey'],
                                                              [   'isa',
                                                                  'xray_tomography_data_anatomy_fkey'],
                                                              [   'isa',
                                                                  'xray_tomography_data_device_fkey'],
                                                              [   'isa',
                                                                  'xray_tomography_data_equipment_model_fkey'],
                                                              'description',
                                                              'url',
                                                              [   'isa',
                                                                  'xray_tomography_data_file_type_fkey'],
                                                              'filename',
                                                              [   'isa',
                                                                  'xray_tomography_data_file_type_fkey'],
                                                              'byte_count',
                                                              'md5',
                                                              'submitted_on'],
                                                 'filter': {   'and': [   {   'entity': True,
                                                                              'markdown_name': 'File '
                                                                                               'Name',
                                                                              'open': False,
                                                                              'source': 'filename'},
                                                                          {   'entity': True,
                                                                              'markdown_name': 'Replicate',
                                                                              'open': True,
                                                                              'source': [   {   'outbound': [   'isa',
                                                                                                                'xray_tomography_data_replicate_fkey']},
                                                                                            'RID']},
                                                                          {   'entity': True,
                                                                              'markdown_name': 'Anatomy',
                                                                              'open': True,
                                                                              'source': [   {   'outbound': [   'isa',
                                                                                                                'xray_tomography_data_anatomy_fkey']},
                                                                                            'id']},
                                                                          {   'entity': True,
                                                                              'markdown_name': 'Imaging '
                                                                                               'Device',
                                                                              'open': True,
                                                                              'source': [   {   'outbound': [   'isa',
                                                                                                                'xray_tomography_data_device_fkey']},
                                                                                            'id']},
                                                                          {   'entity': True,
                                                                              'markdown_name': 'Equipment '
                                                                                               'Model',
                                                                              'open': True,
                                                                              'source': [   {   'outbound': [   'isa',
                                                                                                                'xray_tomography_data_equipment_model_fkey']},
                                                                                            'id']},
                                                                          {   'entity': True,
                                                                              'markdown_name': 'File '
                                                                                               'Type',
                                                                              'open': True,
                                                                              'source': [   {   'outbound': [   'isa',
                                                                                                                'xray_tomography_data_file_type_fkey']},
                                                                                            'id']},
                                                                          {   'entity': True,
                                                                              'markdown_name': 'Submitted '
                                                                                               'On',
                                                                              'open': False,
                                                                              'source': 'submitted_on'}]}},
    'tag:isrd.isi.edu,2016:visible-foreign-keys': {   'detailed': [   [   'isa',
                                                                          'thumbnail_thumbnail_of_fkey'],
                                                                      [   'isa',
                                                                          'mesh_data_derived_from_fkey']],
                                                      'entry': [   [   'isa',
                                                                       'thumbnail_thumbnail_of_fkey'],
                                                                   [   'isa',
                                                                       'mesh_data_derived_from_fkey']]}}

table_def = em.Table.define(
    xray_tomography_data,
    column_defs,
    key_defs=key_defs,
    fkey_defs=fkey_defs,
    comment='Table to hold X-Ray Tomography MRC files.',
    acls=acls,
    acl_bindings=acl_bindings,
    annotations=table_annotations,
    provide_system=True
)

def main():
    parser = argparse.ArgumentParser(description='Load foreign key defs for table isa:xray_tomography_data')
    parser.add_argument('--server', default='pbcconsortium.isrd.isi.edu',
                            help='Catalog server name')
    args = parser.parse_args()

    server = args.server
    schema_name = 'isa'
    table_name = 'xray_tomography_data'

    credential = get_credential(server)
    catalog = ErmrestCatalog('https', server, 1, credentials=credential)
    model_root = catalog.getCatalogModel()
    schema = model_root.schemas[schema_name]
    table = schema.tables[table_name]

    table = schema.create_table(catalog, table_def)


if __name__ == "__main__":
        main()

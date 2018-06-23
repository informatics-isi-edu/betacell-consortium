import argparse
    from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
    import deriva.core.ermrest_model as em
    
column_defs = [
    em.Column.define(
            'protocol',em.builtin_types.{'typename': 'text', 'is_array': False},
            nullok=False,
            annotations={}
            comment='Protocol Foreign key.'),
    
    em.Column.define(
            'treatment',em.builtin_types.{'typename': 'text', 'is_array': False},
            nullok=False,
            annotations={}
            comment='Treatment foreign key.'),
    
    em.Column.define(
            'treatment_concentration',em.builtin_types.{'typename': 'float4', 'is_array': False},
            nullok=True,
            annotations={}
            comment='Concentration of treatment applied to a cell line in mM.'),
    
key_defs = [
    em.Key.define(
                ['protocol', 'treatment'],
                constraint_names=[('isa', 'protocol_treatment_RID_key')],
                annotation={},
                comment='protocol and treatment must be distinct.'),
    em.Key.define(
                ['RID'],
                constraint_names=[('isa', 'protocol_treatment_RIDkey1')],
                annotation={},
                comment=None),
]

fkey_defs = [
    em.ForeignKey.define(
            ['treatment'],
            'vocab', 'treatment_terms', ['id'],
            constraint_names = [('isa', 'protocol_treatment_treatment_fkey')],
        acls = {'insert': ['*'], 'update': ['*']},
        comment = 'Must be a valid reference to a treatment.',
    ),
    em.ForeignKey.define(
            ['protocol'],
            'isa', 'protocol', ['RID'],
            constraint_names = [('isa', 'protocol_treatment_protocol_fkey')],
        acls = {'insert': ['*'], 'update': ['*']},
        on_delete = 'CASCADE',
    ),
]

table_annotations =
{   'tag:isrd.isi.edu,2016:visible-columns': {   'compact': [   'RID',
                                                                [   'isa',
                                                                    'protocol_treatment_protocol_fkey'],
                                                                [   'isa',
                                                                    'protocol_treatment_treatment_fkey'],
                                                                'treatment_concentration'],
                                                 'detailed': [   'RID',
                                                                 'RMT',
                                                                 [   'isa',
                                                                     'protocol_treatment_protocol_fkey'],
                                                                 [   'isa',
                                                                     'protocol_treatment_treatment_fkey'],
                                                                 'treatment_concentration'],
                                                 'entry': [   'RID',
                                                              [   'isa',
                                                                  'protocol_treatment_protocol_fkey'],
                                                              [   'isa',
                                                                  'protocol_treatment_treatment_fkey'],
                                                              'treatment_concentration'],
                                                 'filter': {   'and': [   {   'open': True,
                                                                              'source': [   {   'outbound': [   'isa',
                                                                                                                'protocol_treatment_treatment_fkey']},
                                                                                            'name']},
                                                                          {   'open': True,
                                                                              'source': [   'treatment_concentration']}]}}}

table_def = em.Table.define(
    protocol_treatment,
    column_defs,
    key_defs=key_defs,
    fkey_defs=fkey_defs,
    comment='Table of biological speciments from which biosamples will be created.',
    acls=acls,
    acl_bindings=acl_bindings,
    annotations=table_annotations,
    provide_system=True
)

def main():
    parser = argparse.ArgumentParser(description='Load foreign key defs for table isa:protocol_treatment')
    parser.add_argument('--server', default='pbcconsortium.isrd.isi.edu',
                            help='Catalog server name')
    args = parser.parse_args()

    server = args.server
    schema_name = 'isa'
    table_name = 'protocol_treatment'

    credential = get_credential(server)
    catalog = ErmrestCatalog('https', server, 1, credentials=credential)
    model_root = catalog.getCatalogModel()
    schema = model_root.schemas[schema_name]
    table = schema.tables[table_name]

    table = schema.create_table(catalog, table_def)


if __name__ == "__main__":
        main()

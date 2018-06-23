import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
    
visible_columns = \
{   'compact': [   ['isa', 'protocol_pkey'],
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
                       'source': ['timepoint']},
                   'description'],
    'detailed': [['isa', 'protocol_pkey'], 'name', 'timepoint', 'description'],
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
                                 'markdown_name': 'Protocol Name',
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
                                 'markdown_name': 'Treatment Concentration',
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
                                 'markdown_name': 'Protocol Description',
                                 'open': False,
                                 'source': 'description'}]}}
visible_foreign_keys = \
{   'detailed': [   ['isa', 'protocol_treatment_protocol_fkey'],
                    ['isa', 'experiment_protocol_fkey']],
    'entry': [['isa', 'experiment_protocol_fkey']]}
annotations = \
{   'tag:isrd.isi.edu,2016:table-display': {},
    'tag:isrd.isi.edu,2016:visible-columns': {   'compact': [   [   'isa',
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
column_annotations = \
{   'file_url': {   'tag:isrd.isi.edu,2017:asset': {   'byte_count_column': 'byte_count',
                                                       'filename_column': 'filename',
                                                       'md5': 'md5',
                                                       'url_pattern': '/hatrac/commons/documents/protocol/{{{md5}}}'}}}

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

        if len(visible_columns) > 0:
            for k, v in visible_columns.items():
                table.visible_columns[k] = v

        if len(visible_foreign_keys) > 0:
            for k, v in visible_foreign_keys.items():
                table.visible_foreign_keys[k] = v
        table.annotations['table_display'] = table_display

        table.apply(catalog)


if __name__ == "__main__":
        main()

from deriva.core import HatracStore, ErmrestCatalog, ErmrestSnapshot, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

server = 'pbcconsortium.isrd.isi.edu'
schema_name = 'isa'
table_name = 'protocol'

visible_columns = \
    {'compact': [['isa', 'protocol_pkey'],
                 'name',
                 'treatment',
                 'treatment_concentration',
                 'timepoint',
                 'description'],
     'detailed': [['isa', 'protocol_pkey'],
                  'name',
                  [['isa', 'protocol_treatment_protocol_fkey'], ['isa', 'protocol_treatment_treatment']],
                  {'source': [{'inbound': ['isa', 'protocol_treatment_protocol_fkey']},
                              {'outbound': ['isa', 'protocol_treatment_treatment_fkey']},
                              'name'],
                   'markdown_name': 'Treatment a GoGO'},
                  'treatment',
                  'treatment_concentration',
                  'timepoint',
                  'description'],
     'entry': ['RID',
               'name',
               'treatment',
                [['isa', 'protocol_treatment_protocol_fkey'],['isa', 'protocol_treatment_treatment']],
                {"source": [{"inbound": ["isa", "protocol_treatment_treatement_fkey"]}, "protocol"]},
               'treatment_concentration',
               'timepoint',
               'protocol_url',
               'description',
               'file_url',
               'filename'],
     'filter': {'and': [{'entity': True,
                         'markdown_name': 'Protocol Name',
                         'open': False,
                         'source': 'name'},
                        {'entity': True,
                         'markdown_name': 'Treatment',
                         'open': False,
                         'source': 'treatment'},
                        {'entity': True,
                         'markdown_name': 'Treatment Concentration',
                         'open': False,
                         'source': 'concentration'},
                        {'entity': True,
                         'markdown_name': 'Treatment Concentration',
                         'open': False,
                         'source': 'timepoint'},
                        {'entity': True,
                         'markdown_name': 'Protocol Description',
                         'open': False,
                         'source': 'description'}]}}

visible_foreign_keys = \
    {'detailed': [['isa', 'experiment_protocol_fkey'],
                  [['isa', 'protocol_treatment_protocol_fkey'],['isa', 'protocol_treatment_treatment']],
                  [['isa', 'protocol_treatment_protocol_fkey']]
                  ],
     'entry': [['isa', 'experiment_protocol_fkey'],
               [['isa', 'protocol_treatment_protocol_fkey'],['isa', 'protocol_treatment_treatment']]
     ]}

table_display = \
    {}
table_annotations = \
    {'tag:isrd.isi.edu,2016:table-display': {},
     'tag:isrd.isi.edu,2016:visible-columns': {'compact': [['isa',
                                                            'protocol_pkey'],
                                                           'name',
                                                           'treatment',
                                                           'treatment_concentration',
                                                           'timepoint',
                                                           'description'],
                                               'detailed': [['isa',
                                                             'protocol_pkey'],
                                                            'name',
                                                            'treatment',
                                                            'treatment_concentration',
                                                            'timepoint',
                                                            'description'],
                                               'entry': ['RID',
                                                         'name',
                                                         'treatment',
                                                         'treatment_concentration',
                                                         'timepoint',
                                                         'protocol_url',
                                                         'description',
                                                         'file_url',
                                                         'filename'],
                                               'filter': {'and': [{'entity': True,
                                                                   'markdown_name': 'Protocol '
                                                                                    'Name',
                                                                   'open': False,
                                                                   'source': 'name'},
                                                                  {'entity': True,
                                                                   'markdown_name': 'Treatment',
                                                                   'open': False,
                                                                   'source': 'treatment'},
                                                                  {'entity': True,
                                                                   'markdown_name': 'Treatment '
                                                                                    'Concentration',
                                                                   'open': False,
                                                                   'source': 'concentration'},
                                                                  {'entity': True,
                                                                   'markdown_name': 'Treatment '
                                                                                    'Concentration',
                                                                   'open': False,
                                                                   'source': 'timepoint'},
                                                                  {'entity': True,
                                                                   'markdown_name': 'Protocol '
                                                                                    'Description',
                                                                   'open': False,
                                                                   'source': 'description'}]}},
     'tag:isrd.isi.edu,2016:visible-foreign-keys': {'detailed': [['isa',
                                                                  'experiment_protocol_fkey']],
                                                    'entry': [['isa',
                                                               'experiment_protocol_fkey']]},
     'tag:misd.isi.edu,2015:display': {'name': 'Protocol'}}

table_acls = \
    {}
table_acl_bindings = \
    {}

column_annotations = \
    {'RCB': {},
     'RCT': {},
     'description': {},
     'file_url': {'tag:isrd.isi.edu,2017:asset': {'byte_count_column': 'byte_count',
                                                  'filename_column': 'filename',
                                                  'md5': 'md5',
                                                  'url_pattern': '/hatrac/commons/documents/protocol/{{{md5}}}'}},
     'filename': {},
     'md5': {},
     'name': {},
     'protocol_url': {},
     'timepoint': {},
     'treatment': {},
     'treatment_concentration': {}}


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

#table[table_display] = table_display

table.apply(catalog)

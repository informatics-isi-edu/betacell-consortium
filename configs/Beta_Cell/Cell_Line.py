import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'Cell_Line'
schema_name = 'Beta_Cell'

column_defs = [
    em.Column.define('Cell_Line_Id', em.builtin_types['text'],
        comment='ID of cell line being used.',
    ),
    em.Column.define('Species', em.builtin_types['text'],
        comment='Species of the specimen',
    ),
    em.Column.define('Anatomy', em.builtin_types['text'],
        comment='Anatomical region speciment was obtained from.',
    ),
    em.Column.define('Description', em.builtin_types['text'],
        comment='Description of the specimen.',
    ),
    em.Column.define('Protocol', em.builtin_types['text'],
        comment='Protocol used to create the cell line',
    ),
    em.Column.define('Collection_Date', em.builtin_types['date'],
    ),
]


key_defs = [
    em.Key.define(['RID'],
                   constraint_names=[('Beta_Cell', 'Cell_Line_Key')],
    ),
]


fkey_defs = [
    em.ForeignKey.define(['Anatomy'],
            'vocab', 'anatomy_terms', ['id'],
            constraint_names=[('Beta_Cell', 'Cell_Line_Anatomy_FKey')],
        acls={'insert': ['*'], 'update': ['*']},
    ),
    em.ForeignKey.define(['Species'],
            'vocab', 'species_terms', ['id'],
            constraint_names=[('Beta_Cell', 'Cell_Line_Species_FKey')],
        acls={'insert': ['*'], 'update': ['*']},
    ),
    em.ForeignKey.define(['Cell_Line_Id'],
            'vocab', 'cell_line_terms', ['id'],
            constraint_names=[('Beta_Cell', 'Cell_Line_Cell_Line_Terms_FKey')],
        acls={'insert': ['*'], 'update': ['*']},
        comment='Must be a valid reference to a cell line.',
    ),
    em.ForeignKey.define(['Protocol'],
            'Beta_Cell', 'Protocol', ['RID'],
            constraint_names=[('Beta_Cell', 'Cell_Line_Protocol_FKey')],
        acls={'insert': ['*'], 'update': ['*']},
    ),
]


visible_columns = \
{'*': [['Beta_Cell', 'Cell_Line_Key'],
       ['Beta_Cell', 'Cell_Line_Cell_Line_Terms_FKey'],
       ['Beta_Cell', 'Cell_Line_Species_FKey'],
       ['Beta_Cell', 'Cell_Line_Anatomy_FKey'],
       ['Beta_Cell', 'Cell_Line_Protocol_FKey'], 'Description',
       'Collection_Date'],
 'filter': {'and': [{'entity': True,
                     'markdown_name': 'Cell Line',
                     'open': True,
                     'source': [{'outbound': ['Beta_Cell',
                                              'Cell_Line_Cell_Line_Terms_FKey']},
                                'name']},
                    {'entity': True,
                     'markdown_name': 'Species',
                     'open': True,
                     'source': [{'outbound': ['Beta_Cell',
                                              'Cell_Line_Species_FKey']},
                                'name']},
                    {'entity': True,
                     'markdown_name': 'Anatomy',
                     'open': True,
                     'source': [{'outbound': ['Beta_Cell',
                                              'Cell_Line_Anatomy_FKey']},
                                'name']}]}}

visible_foreign_keys = \
{'*': [{'source': [{'inbound': ['Beta_Cell', 'Specimen_Cell_Line_FKey']},
                   'RID']}]}

table_comment = \
'Table of cultured  from which specimens  will be created.'

table_display = {}
table_acls = {}
table_acl_bindings = {}
table_annotations = {
    "tag:isrd.isi.edu,2016:table-display": table_display,
    "tag:isrd.isi.edu,2016:visible-foreign-keys": visible_foreign_keys,
    "table_display": table_display,
    "tag:isrd.isi.edu,2016:visible-columns": visible_columns,
}
column_comment = \
{'Anatomy': 'Anatomical region speciment was obtained from.',
 'Cell_Line_Id': 'ID of cell line being used.',
 'Description': 'Description of the specimen.',
 'Protocol': 'Protocol used to create the cell line',
 'Species': 'Species of the specimen'}

column_annotations = \
{}



table_def = em.Table.define(table_name,
    column_defs=column_defs,
    key_defs=key_defs,
    fkey_defs=fkey_defs,
    annotations=table_annotations,
    acls=table_acls,
    acl_bindings=table_acl_bindings,
    comment=table_comment,
    provide_system = True
)

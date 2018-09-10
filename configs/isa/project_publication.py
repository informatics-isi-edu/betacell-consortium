import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'project_publication'
schema_name = 'isa'

column_defs = [
    em.Column.define('id', em.builtin_types['serial4'],
        nullok=False,
    ),
    em.Column.define('project_id', em.builtin_types['int4'],
        nullok=False,
    ),
    em.Column.define('pmid', em.builtin_types['text'],
        nullok=False,
        annotations={'tag:misd.isi.edu,2015:display': {'name': 'PMID'}, 'tag:isrd.isi.edu,2016:column-display': {'*': {'markdown_pattern': '[{{{_pmid}}}](http://www.ncbi.nlm.nih.gov/pubmed/{{{_pmid}}})'}}},
    ),
]


key_defs = [
    em.Key.define(['RID'],
                   constraint_names=[('isa', 'project_publication_RID_key')],
    ),
    em.Key.define(['project_id', 'pmid'],
                   constraint_names=[('isa', 'project_publication_project_id_pmid_key')],
    ),
    em.Key.define(['id'],
                   constraint_names=[('isa', 'project_publication_pkey')],
    ),
]


fkey_defs = [
    em.ForeignKey.define(['project_id'],
            'isa', 'project', ['id'],
            constraint_names=[('isa', 'project_publication_project_id_fkey')],
        on_update='CASCADE',
        on_delete='CASCADE',
    ),
]


visible_columns = \
{'*': [['isa', 'project_publication_project_id_fkey'], 'pmid']}

visible_foreign_keys = {}
table_comment = \
None

table_display = \
{'compact': {'row_markdown_pattern': '[Link to PubMed '
                                     '(PMID:{{{_pmid}}})](http://www.ncbi.nlm.nih.gov/pubmed/{{{_pmid}}})'},
 'row_name': {'row_markdown_pattern': 'PMID:{{{_pmid}}}'}}

table_acls = {}
table_acl_bindings = {}
table_annotations = {
    "tag:isrd.isi.edu,2016:table-display": table_display,
    "tag:isrd.isi.edu,2016:visible-columns": visible_columns,
    "tag:isrd.isi.edu,2016:visible-foreign-keys": visible_foreign_keys,
}
column_comment = \
{'RCB': 'System-generated row created by user provenance.',
 'RCT': 'System-generated row creation timestamp.',
 'RID': 'System-generated unique row ID.',
 'RMB': 'System-generated row modified by user provenance.',
 'RMT': 'System-generated row modification timestamp'}

column_annotations = \
{'pmid': {'tag:isrd.isi.edu,2016:column-display': {'*': {'markdown_pattern': '[{{{_pmid}}}](http://www.ncbi.nlm.nih.gov/pubmed/{{{_pmid}}})'}},
          'tag:misd.isi.edu,2015:display': {'name': 'PMID'}}}



table_def = em.Table.define('project_publication',
    column_defs=column_defs,
    key_defs=key_defs,
    fkey_defs=fkey_defs,
    annotations=table_annotations,
    acls=table_acls,
    acl_bindings=table_acl_bindings,
    comment='None',
    provide_system = True
)

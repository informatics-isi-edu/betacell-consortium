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
    em.Key.define(['id'],
                   constraint_names=[('isa', 'project_publication_pkey')],
    ),
    em.Key.define(['project_id', 'pmid'],
                   constraint_names=[('isa', 'project_publication_project_id_pmid_key')],
    ),
    em.Key.define(['RID'],
                   constraint_names=[('isa', 'project_publication_RID_key')],
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


visible_columns=\
{'*': [['isa', 'project_publication_project_id_fkey'], 'pmid']}

visible_foreign_keys={}
table_display=\
{'compact': {'row_markdown_pattern': '[Link to PubMed '
                                     '(PMID:{{{_pmid}}})](http://www.ncbi.nlm.nih.gov/pubmed/{{{_pmid}}})'},
 'row_name': {'row_markdown_pattern': 'PMID:{{{_pmid}}}'}}

table_acls={}
table_acl_bindings=\
{'project_suppl_edit_guard': {'projection': [{'outbound': ['isa',
                                                           'project_publication_project_id_fkey']},
                                             {'outbound': ['isa',
                                                           'project_groups_fkey']},
                                             'groups'],
                              'projection_type': 'acl',
                              'scope_acl': ['https://auth.globus.org/6a96ec62-7032-11e8-9132-0a043b872764',
                                            'https://auth.globus.org/aa5a2f6e-53e8-11e8-b60b-0a7c735d220a',
                                            'https://auth.globus.org/9d596ac6-22b9-11e6-b519-22000aef184d'],
                              'types': ['update', 'delete']}}

table_annotations = {
    "tag:isrd.isi.edu,2016:table-display":table_display,
    "tag:isrd.isi.edu,2016:visible-columns":visible_columns,
    "tag:isrd.isi.edu,2016:visible-foreign-keys":visible_foreign_keys,
}
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

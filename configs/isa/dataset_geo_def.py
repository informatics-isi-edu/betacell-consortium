import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'dataset_geo'
schema_name = 'isa'

column_defs = [
    em.Column.define('dataset_id', em.builtin_types['int8'],
        nullok=False,
    ),
    em.Column.define('geo_gds', em.builtin_types['text'],
        annotations={'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '{{#geo_gds}}[Search GEO for {{{geo_gds}}}](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={{{geo_gds}}}){{/geo_gds}}'}}, 'tag:misd.isi.edu,2015:url': {'url': 'http://www.ncbi.nlm.nih.gov/sites/GDSbrowser?acc={geo_gds}', 'caption': 'GEO Curated'}},
        comment='http://www.ncbi.nlm.nih.gov/sites/GDSbrowser?acc=',
    ),
    em.Column.define('geo_gse', em.builtin_types['text'],
        annotations={'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '{{#geo_gse}}[Search GEO for {{{geo_gse}}}](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={{{geo_gse}}}){{/geo_gse}}'}}, 'tag:misd.isi.edu,2015:url': {'url': 'http://www.ncbi.nlm.nih.gov/geo/geo2r/?acc={geo_gse}', 'caption': 'GEO Submitted'}},
        comment='http://www.ncbi.nlm.nih.gov/geo/geo2r/?acc=',
    ),
]


key_defs = [
    em.Key.define(['dataset_id'],
                   constraint_names=[('isa', 'dataset_geo_pkey')],
    ),
    em.Key.define(['RID'],
                   constraint_names=[('isa', 'dataset_geo_RID_key')],
    ),
]


fkey_defs = [
    em.ForeignKey.define(['dataset_id'],
            'isa', 'dataset', ['id'],
            constraint_names=[('isa', 'dataset_geo_dataset_id_fkey')],
        on_update='CASCADE',
        on_delete='CASCADE',
    ),
]


visible_columns=\
{'compact': ['geo_gds', 'geo_gse'], 'detailed': ['geo_gds', 'geo_gse']}

visible_foreign_keys={}
table_display={}
table_acls={}
table_acl_bindings=\
{'dataset_tags_edit_guard': {'projection': [{'outbound': ['isa',
                                                          'dataset_geo_dataset_id_fkey']},
                                            {'outbound': ['isa',
                                                          'dataset_project_fkey']},
                                            {'outbound': ['isa',
                                                          'project_groups_fkey']},
                                            'groups'],
                             'projection_type': 'acl',
                             'scope_acl': ['https://auth.globus.org/6a96ec62-7032-11e8-9132-0a043b872764',
                                           'https://auth.globus.org/aa5a2f6e-53e8-11e8-b60b-0a7c735d220a',
                                           'https://auth.globus.org/9d596ac6-22b9-11e6-b519-22000aef184d'],
                             'types': ['update', 'delete']}}

table_annotations = {
    "tag:isrd.isi.edu,2016:visible-columns":visible_columns,
    "tag:isrd.isi.edu,2016:visible-foreign-keys":visible_foreign_keys,
    "tag:isrd.isi.edu,2016:table-display":table_display,
}
column_annotations = \
{'geo_gds': {'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '{{#geo_gds}}[Search '
                                                                                      'GEO '
                                                                                      'for '
                                                                                      '{{{geo_gds}}}](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={{{geo_gds}}}){{/geo_gds}}'}},
             'tag:misd.isi.edu,2015:url': {'caption': 'GEO Curated',
                                           'url': 'http://www.ncbi.nlm.nih.gov/sites/GDSbrowser?acc={geo_gds}'}},
 'geo_gse': {'tag:isrd.isi.edu,2016:column-display': {'compact': {'markdown_pattern': '{{#geo_gse}}[Search '
                                                                                      'GEO '
                                                                                      'for '
                                                                                      '{{{geo_gse}}}](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={{{geo_gse}}}){{/geo_gse}}'}},
             'tag:misd.isi.edu,2015:url': {'caption': 'GEO Submitted',
                                           'url': 'http://www.ncbi.nlm.nih.gov/geo/geo2r/?acc={geo_gse}'}}}



table_def = em.Table.define('dataset_geo',
    column_defs=column_defs,
    key_defs=key_defs,
    fkey_defs=fkey_defs,
    annotations=table_annotations,
    acls=table_acls,
    acl_bindings=table_acl_bindings,
    comment='references to external GEO numbers for curated (gds) and submitted (gse) data',
    provide_system = True
)

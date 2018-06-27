import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em

table_name = 'model'
schema_name = 'viz'

column_defs = [
    em.Column.define('id', em.builtin_types['serial4'],
        nullok = False,
        annotations = {'tag:isrd.isi.edu,2017:asset': {}, 'tag:misd.isi.edu,2015:display': {}, 'tag:isrd.isi.edu,2016:column-display': {}},
    ),
    em.Column.define('label', em.builtin_types['text'],
        nullok = False,
    ),
    em.Column.define('description', em.builtin_types['markdown'],
        nullok = True,
    ),
    em.Column.define('bg_color_r', em.builtin_types['int4'],
        nullok = True,
    ),
    em.Column.define('bg_color_g', em.builtin_types['int4'],
        nullok = True,
    ),
    em.Column.define('bg_color_b', em.builtin_types['int4'],
        nullok = True,
    ),
    em.Column.define('bounding_box_color_r', em.builtin_types['int4'],
        nullok = True,
    ),
    em.Column.define('bounding_box_color_g', em.builtin_types['int4'],
        nullok = True,
    ),
    em.Column.define('bounding_box_color_b', em.builtin_types['int4'],
        nullok = True,
    ),
    em.Column.define('show_bounding_box', em.builtin_types['boolean'],
        nullok = True,
    ),
    em.Column.define('rotate', em.builtin_types['boolean'],
        nullok = True,
    ),
    em.Column.define('volume', em.builtin_types['text'],
        nullok = True,
    ),
    em.Column.define('experiment', em.builtin_types['ermrest_rid'],
        nullok = True,
    ),
    em.Column.define('replicate', em.builtin_types['ermrest_rid'],
        nullok = True,
    ),
]


key_defs = [
    em.Key.define(['RID'],
                   constraint_names=[('viz', 'model_RID_key')],
    ),
    em.Key.define(['id'],
                   constraint_names=[('viz', 'model_pkey')],
    ),
]


fkey_defs = [
    em.ForeignKey.define(['replicate'],
            'isa', 'replicate', ['RID'],
            constraint_names = [('viz', 'model_replicate_fkey')],
        acls = {'insert': ['*'], 'update': ['*']},
        on_update = 'CASCADE',
        on_delete = 'SET NULL',
    ),
    em.ForeignKey.define(['experiment'],
            'isa', 'experiment', ['RID'],
            constraint_names = [('viz', 'model_experiment_fkey')],
        acls = {'insert': ['*'], 'update': ['*']},
        on_update = 'CASCADE',
        on_delete = 'SET NULL',
    ),
    em.ForeignKey.define(['volume'],
            'isa', 'imaging_data', ['RID'],
            constraint_names = [('viz', 'model_volume_fkey')],
        acls = {'insert': ['*'], 'update': ['*']},
    ),
]


visible_columns=\
{   'compact': [   ['viz', 'model_dataset_fkey'],
                   'label',
                   'description',
                   ['viz', 'model_derived_from_fkey'],
                   ['viz', 'model_experiment_fkey'],
                   ['viz', 'model_replicate_fkey'],
                   'protocol']}

visible_foreign_keys={}
table_display=\
{   'compact': {   'row_markdown_pattern': ':::iframe '
                                           '[{{{label}}}](/mesh-viewer/view.html?model=/ermrest/catalog/1/entity/viz:model_json/RID={{{_RID}}}){width=1024 '
                                           'height=768 .iframe} \n'
                                           ':::'}}

table_acls={}
table_acl_bindings={}
table_annotations = {
    "tag:isrd.isi.edu,2016:table-display": table_display,
    "tag:misd.isi.edu,2015:display" :
{'name': '3D Surface Models'}
    "table_display" :
{       'compact': {       'row_markdown_pattern': ':::iframe '
                                                   '[{{{label}}}](/mesh-viewer/view.html?model=/ermrest/catalog/1/entity/viz:model_json/RID={{{_RID}}}){width=1024 '
                                                   'height=768 .iframe} \n'
                                                   ':::'}}
    "tag:isrd.isi.edu,2016:visible-columns" : visible_columns,
    "tag:isrd.isi.edu,2016:visible-foreign-keys" : visible_foreign_keys,
}
column_annotations = \
{   'id': {   'tag:isrd.isi.edu,2016:column-display': {},
              'tag:isrd.isi.edu,2017:asset': {},
              'tag:misd.isi.edu,2015:display': {}}}



table_def = em.Table.define('model',
    column_defs=column_defs,
    key_defs=key_defs,
    fkey_defs=fkey_defs,
    annotations=table_annotations,
    acls=table_acls,
    acl_bindings=table_acl_bindings,
    comment='None',
    provide_system = True
)

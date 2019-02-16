import argparse
from attrdict import AttrDict
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

groups = {
    'pbcconsortium-reader': 'https://auth.globus.org/aa5a2f6e-53e8-11e8-b60b-0a7c735d220a',
    'pbcconsortium-curator': 'https://auth.globus.org/da80b96c-edab-11e8-80e2-0a7c1eab007a',
    'pbcconsortium-writer': 'https://auth.globus.org/6a96ec62-7032-11e8-9132-0a043b872764',
    'pbcconsortium-admin': 'https://auth.globus.org/80df6c56-a0e8-11e8-b9dc-0ada61684422',
    'isrd-staff': 'https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b',
    'isrd-testers': 'https://auth.globus.org/9d596ac6-22b9-11e6-b519-22000aef184d'
}

table_name = 'model'

schema_name = 'viz'

column_annotations = {
    'id': {
        chaise_tags.asset: {},
        chaise_tags.display: {},
        chaise_tags.column_display: {}
    },
    'RID': {},
    'RCB': {},
    'RMB': {},
    'RCT': {},
    'RMT': {}
}

column_comment = {
    'RID': 'System-generated unique row ID.',
    'RCB': 'System-generated row created by user provenance.',
    'RMB': 'System-generated row modified by user provenance.',
    'RCT': 'System-generated row creation timestamp.',
    'RMT': 'System-generated row modification timestamp'
}

column_acls = {}

column_acl_bindings = {}

column_defs = [
    em.Column.define(
        'id', em.builtin_types['serial4'], nullok=False, annotations=column_annotations['id'],
    ),
    em.Column.define('label', em.builtin_types['text'], nullok=False,
                     ),
    em.Column.define('description', em.builtin_types['markdown'],
                     ),
    em.Column.define('bg_color_r', em.builtin_types['int4'],
                     ),
    em.Column.define('bg_color_g', em.builtin_types['int4'],
                     ),
    em.Column.define('bg_color_b', em.builtin_types['int4'],
                     ),
    em.Column.define('bounding_box_color_r', em.builtin_types['int4'], default=255,
                     ),
    em.Column.define('bounding_box_color_g', em.builtin_types['int4'], default=255,
                     ),
    em.Column.define('bounding_box_color_b', em.builtin_types['int4'],
                     ),
    em.Column.define('show_bounding_box', em.builtin_types['boolean'],
                     ),
    em.Column.define('rotate', em.builtin_types['boolean'],
                     ),
    em.Column.define('volume', em.builtin_types['text'],
                     ),
    em.Column.define('biosample', em.builtin_types['text'],
                     ),
]

display = {'name': '3D Surface Models'}

visible_columns = {
    'filter': {
        'and': [
            {
                'source': [
                    {
                        'outbound': ['viz', 'model_biosample_fkey']
                    }, {
                        'outbound': ['Beta_Cell', 'biosample_specimen_fkey']
                    }, {
                        'outbound': ['isa', 'specimen_cell_line_fkey']
                    }, {
                        'outbound': ['isa', 'cell_line_cell_line_terms_fkey']
                    }, 'name'
                ],
                'markdown_name': 'Cell Line'
            },
            {
                'entity': True,
                'source': [
                    {
                        'outbound': ['viz', 'model_biosample_fkey']
                    }, {
                        'outbound': ['Beta_Cell', 'biosample_specimen_fkey']
                    }, {
                        'inbound': ['isa', 'specimen_compound_specimen_fkey']
                    }, {
                        'outbound': ['isa', 'specimen_compound_compound_fkey']
                    }, 'RID'
                ],
                'comment': 'Compound used to treat the cell line for the experiment',
                'aggregate': 'array',
                'markdown_name': 'Compound'
            },
            {
                'entity': True,
                'source': [
                    {
                        'outbound': ['viz', 'model_biosample_fkey']
                    }, {
                        'outbound': ['Beta_Cell', 'biosample_specimen_fkey']
                    }, {
                        'inbound': ['isa', 'specimen_compound_specimen_fkey']
                    }, 'compound_concentration'
                ],
                'comment': 'Concentration of compound applied to cell line in mM',
                'aggregate': 'array',
                'markdown_name': 'Concentration'
            },
            {
                'entity': True,
                'source': [
                    {
                        'outbound': ['viz', 'model_biosample_fkey']
                    }, {
                        'outbound': ['Beta_Cell', 'biosample_specimen_fkey']
                    }, 'timepoint'
                ],
                'comment': 'Measured in minutes'
            }
        ]
    },
    'compact': [
        ['viz', 'model_dataset_fkey'], 'label', 'description',
        {
            'source': [
                {
                    'outbound': ['viz', 'model_biosample_fkey']
                }, {
                    'outbound': ['Beta_Cell', 'biosample_specimen_fkey']
                }, {
                    'outbound': ['isa', 'specimen_cell_line_fkey']
                }, {
                    'outbound': ['isa', 'cell_line_cell_line_terms_fkey']
                }, 'name'
            ],
            'markdown_name': 'Cell Line'
        },
        {
            'entity': True,
            'source': [
                {
                    'outbound': ['viz', 'model_biosample_fkey']
                }, {
                    'outbound': ['Beta_Cell', 'biosample_specimen_fkey']
                }, {
                    'inbound': ['isa', 'specimen_compound_specimen_fkey']
                }, {
                    'outbound': ['isa', 'specimen_compound_compound_fkey']
                }, 'RID'
            ],
            'comment': 'Compound used to treat the cell line for the experiment',
            'aggregate': 'array',
            'markdown_name': 'Compound'
        },
        {
            'entity': True,
            'source': [
                {
                    'outbound': ['viz', 'model_biosample_fkey']
                }, {
                    'outbound': ['Beta_Cell', 'biosample_specimen_fkey']
                }, {
                    'inbound': ['isa', 'specimen_compound_specimen_fkey']
                }, 'compound_concentration'
            ],
            'comment': 'Concentration of compound applied to cell line in mM',
            'aggregate': 'array',
            'markdown_name': 'Concentration'
        },
        {
            'entity': True,
            'source': [
                {
                    'outbound': ['viz', 'model_biosample_fkey']
                }, {
                    'outbound': ['Beta_Cell', 'biosample_specimen_fkey']
                }, 'timepoint'
            ],
            'comment': 'Measured in minutes'
        }
    ],
    'detailed': [
        ['viz', 'model_dataset_fkey'], 'label', 'description', 'bg_color_r', 'bg_color_g',
        'bg_color_b', 'bounding_box_color_r', 'bounding_box_color_g', 'bounding_box_color_b',
        'show_bounding_box', 'rotate', 'volume',
        {
            'entity': True,
            'source': [
                {
                    'outbound': ['viz', 'model_biosample_fkey']
                }, {
                    'outbound': ['Beta_Cell', 'biosample_specimen_fkey']
                }, {
                    'outbound': ['isa', 'specimen_cell_line_fkey']
                }, {
                    'outbound': ['isa', 'cell_line_cell_line_terms_fkey']
                }, 'name'
            ],
            'markdown_name': 'Cell Line'
        },
        {
            'entity': True,
            'source': [
                {
                    'outbound': ['viz', 'model_biosample_fkey']
                }, {
                    'outbound': ['isa', 'experiment_protocol_fkey']
                }, {
                    'inbound': ['isa', 'protocol_treatment_protocol_fkey']
                }, {
                    'outbound': ['isa', 'protocol_treatment_treatment_fkey']
                }, 'RID'
            ],
            'aggregate': 'array',
            'markdown_name': 'Compound'
        },
        {
            'entity': True,
            'source': [
                {
                    'outbound': ['viz', 'model_biosample_fkey']
                }, {
                    'outbound': ['isa', 'experiment_protocol_fkey']
                }, {
                    'inbound': ['isa', 'protocol_treatment_protocol_fkey']
                }, 'treatment_concentration'
            ],
            'aggregate': 'array',
            'markdown_name': 'Concentration'
        }, ['viz', 'model_derived_from_fkey']
    ]
}

visible_foreign_keys = {
    'detailed': [{
        'source': [{
            'outbound': ['viz', 'model_biosammple_fkey']
        }, 'RID']
    }]
}

table_display = {
    'compact': {
        'row_markdown_pattern': ':::iframe [{{{label}}}](https://pbcconsortium.isrd.isi.edu/mesh-viewer/view.html#model_url=https://pbcconsortium.isrd.isi.edu/ermrest/catalog/1/attribute/viz:model/RID={{{_RID}}}/*&mesh_url=https://pbcconsortium.isrd.isi.edu/ermrest/catalog/1/attribute/viz:model/RID={{{_RID}}}/model_mesh:=viz:model_mesh_data/mesh:=mesh_data/$mesh/RID,url,filename,label,description,color_r:=model_mesh:color_r,color_g:=model_mesh:color_g,color_b:=model_mesh:color_b,opacity:=model_mesh:opacity){width=1024 height=768 .iframe} \n:::'
    }
}

export = {
    'templates': [
        {
            'name': 'default',
            'outputs': [
                {
                    'source': {
                        'api': 'entity',
                        'table': 'viz:model'
                    },
                    'destination': {
                        'name': 'surface-model',
                        'type': 'csv'
                    }
                },
                {
                    'source': {
                        'api': 'attribute',
                        'path': 'isa:mesh_data/url',
                        'table': 'viz:model_mesh_data'
                    },
                    'destination': {
                        'name': 'OBJS',
                        'type': 'download'
                    }
                }
            ],
            'format_name': 'BDBag',
            'format_type': 'BAG'
        }
    ]
}

table_annotations = {
    chaise_tags.export: export,
    chaise_tags.display: display,
    chaise_tags.table_display: table_display,
    chaise_tags.visible_columns: visible_columns,
    chaise_tags.visible_foreign_keys: visible_foreign_keys,
}

table_comment = None

table_acls = {}

table_acl_bindings = {}

key_defs = [
    em.Key.define(['id'], constraint_names=[('viz', 'model_pkey')],
                  ),
    em.Key.define(['RID'], constraint_names=[('viz', 'model_RID_key')],
                  ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['biosample'],
        'Beta_Cell',
        'Biosample', ['RID'],
        constraint_names=[('viz', 'model_biosample_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
]

table_def = em.Table.define(
    table_name,
    column_defs=column_defs,
    key_defs=key_defs,
    fkey_defs=fkey_defs,
    annotations=table_annotations,
    acls=table_acls,
    acl_bindings=table_acl_bindings,
    comment=table_comment,
    provide_system=True
)


def main(catalog, mode, replace=False):
    updater = CatalogUpdater(catalog)
    updater.update_table(mode, schema_name, table_def, replace=replace)


if __name__ == "__main__":
    host = 'pbcconsortium.isrd.isi.edu'
    catalog_id = 1
    mode, replace, host, catalog_id = parse_args(host, catalog_id, is_table=True)
    credential = get_credential(host)
    catalog = ErmrestCatalog('https', host, catalog_id, credentials=credential)
    main(catalog, mode, replace)


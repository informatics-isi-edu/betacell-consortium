import argparse
from attrdict import AttrDict
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

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
                'comment': 'Compound used to treat the cell line for the experiment',
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
                'aggregate': 'array',
                'markdown_name': 'Compound',
                'entity': True
            },
            {
                'comment': 'Concentration of compound applied to cell line in mM',
                'source': [
                    {
                        'outbound': ['viz', 'model_biosample_fkey']
                    }, {
                        'outbound': ['Beta_Cell', 'biosample_specimen_fkey']
                    }, {
                        'inbound': ['isa', 'specimen_compound_specimen_fkey']
                    }, 'compound_concentration'
                ],
                'aggregate': 'array',
                'markdown_name': 'Concentration',
                'entity': True
            },
            {
                'comment': 'Measured in minutes',
                'source': [
                    {
                        'outbound': ['viz', 'model_biosample_fkey']
                    }, {
                        'outbound': ['Beta_Cell', 'biosample_specimen_fkey']
                    }, 'timepoint'
                ],
                'entity': True
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
            'comment': 'Compound used to treat the cell line for the experiment',
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
            'aggregate': 'array',
            'markdown_name': 'Compound',
            'entity': True
        },
        {
            'comment': 'Concentration of compound applied to cell line in mM',
            'source': [
                {
                    'outbound': ['viz', 'model_biosample_fkey']
                }, {
                    'outbound': ['Beta_Cell', 'biosample_specimen_fkey']
                }, {
                    'inbound': ['isa', 'specimen_compound_specimen_fkey']
                }, 'compound_concentration'
            ],
            'aggregate': 'array',
            'markdown_name': 'Concentration',
            'entity': True
        },
        {
            'comment': 'Measured in minutes',
            'source': [
                {
                    'outbound': ['viz', 'model_biosample_fkey']
                }, {
                    'outbound': ['Beta_Cell', 'biosample_specimen_fkey']
                }, 'timepoint'
            ],
            'entity': True
        }
    ],
    'detailed': [
        ['viz', 'model_dataset_fkey'], 'label', 'description', 'bg_color_r', 'bg_color_g',
        'bg_color_b', 'bounding_box_color_r', 'bounding_box_color_g', 'bounding_box_color_b',
        'show_bounding_box', 'rotate', 'volume',
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
            'markdown_name': 'Cell Line',
            'entity': True
        },
        {
            'aggregate': 'array',
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
            'markdown_name': 'Compound',
            'entity': True
        },
        {
            'aggregate': 'array',
            'source': [
                {
                    'outbound': ['viz', 'model_biosample_fkey']
                }, {
                    'outbound': ['isa', 'experiment_protocol_fkey']
                }, {
                    'inbound': ['isa', 'protocol_treatment_protocol_fkey']
                }, 'treatment_concentration'
            ],
            'markdown_name': 'Concentration',
            'entity': True
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
        'row_markdown_pattern': ':::iframe [{{{label}}}](8/mesh-viewer/view.html?model=/ermrest/catalog/1/entity/viz:model_json/RID={{{_RID}}}){width=1024 height=76 .iframe} \n:::'
    }
}

export = {
    'templates': [
        {
            'outputs': [
                {
                    'source': {
                        'table': 'viz:model',
                        'api': 'entity'
                    },
                    'destination': {
                        'type': 'csv',
                        'name': 'surface-model'
                    }
                },
                {
                    'source': {
                        'path': 'isa:mesh_data/url',
                        'api': 'attribute',
                        'table': 'viz:model_mesh_data'
                    },
                    'destination': {
                        'type': 'download',
                        'name': 'OBJS'
                    }
                }
            ],
            'name': 'default',
            'format_name': 'BDBag',
            'format_type': 'BAG'
        }
    ]
}

table_annotations = {
    chaise_tags.export: export,
    chaise_tags.table_display: table_display,
    chaise_tags.display: display,
    chaise_tags.visible_foreign_keys: visible_foreign_keys,
    'table_display': {
        'compact': {
            'row_markdown_pattern': ':::iframe [{{{label}}}](/mesh-viewer/view.html?model=/ermrest/catalog/1/entity/viz:model_json/RID={{{_RID}}}){width=1024 height=768 .iframe} \n:::'
        }
    },
    chaise_tags.visible_columns: visible_columns,
}
table_comment = None
table_acls = {}
table_acl_bindings = {}

key_defs = [
    em.Key.define(['RID'], constraint_names=[('viz', 'model_RID_key')],
                  ),
    em.Key.define(['id'], constraint_names=[('viz', 'model_pkey')],
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
    server = 'pbcconsortium.isrd.isi.edu'
    catalog_id = 1
    mode, replace, server, catalog_id = parse_args(server, catalog_id, is_table=True)
    credential = get_credential(server)
    catalog = ErmrestCatalog('https', server, catalog_id, credentials=credential)
    main(catalog, mode, replace)


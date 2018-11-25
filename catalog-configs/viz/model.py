import argparse
from attrdict import AttrDict
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage import update_catalog

table_name = 'model'

schema_name = 'viz'

groups = AttrDict(
    {
        'admins': 'https://auth.globus.org/80df6c56-a0e8-11e8-b9dc-0ada61684422',
        'modelers': 'https://auth.globus.org/a45e5ba2-709f-11e8-a40d-0e847f194132',
        'curators': 'https://auth.globus.org/da80b96c-edab-11e8-80e2-0a7c1eab007a',
        'writers': 'https://auth.globus.org/6a96ec62-7032-11e8-9132-0a043b872764',
        'readers': 'https://auth.globus.org/aa5a2f6e-53e8-11e8-b60b-0a7c735d220a',
        'isrd': 'https://auth.globus.org/3938e0d0-ed35-11e5-8641-22000ab4b42b'
    }
)

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
        'id',
        em.builtin_types['serial4'],
        nullok=False,
        annotations=column_annotations['id'],
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
    em.Column.define(
        'RID',
        em.builtin_types['ermrest_rid'],
        nullok=False,
        comment=column_comment['RID'],
    ),
    em.Column.define(
        'RCB', em.builtin_types['ermrest_rcb'], comment=column_comment['RCB'],
    ),
    em.Column.define(
        'RMB', em.builtin_types['ermrest_rmb'], comment=column_comment['RMB'],
    ),
    em.Column.define(
        'RCT',
        em.builtin_types['ermrest_rct'],
        nullok=False,
        comment=column_comment['RCT'],
    ),
    em.Column.define(
        'RMT',
        em.builtin_types['ermrest_rmt'],
        nullok=False,
        comment=column_comment['RMT'],
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
        'bg_color_b', 'bounding_box_color_r', 'bounding_box_color_g',
        'bounding_box_color_b', 'show_bounding_box', 'rotate', 'volume',
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
        'row_markdown_pattern': ':::iframe [{{{label}}}](/mesh-viewer/view.html?model=/ermrest/catalog/1/entity/viz:model_json/RID={{{_RID}}}){width=1024 height=768 .iframe} \n:::'
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

key_defs = []

fkey_defs = []

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


def main(
    skip_args=False,
    mode='annotations',
    replace=False,
    server='pbcconsortium.isrd.isi.edu',
    catalog_id=1
):

    if not skip_args:
        mode, replace, server, catalog_id = update_catalog.parse_args(
            server, catalog_id, is_table=True
        )
    update_catalog.update_table(
        mode, replace, server, catalog_id, schema_name, table_name, table_def,
        column_defs, key_defs, fkey_defs, table_annotations, table_acls,
        table_acl_bindings, table_comment, column_annotations, column_acls,
        column_acl_bindings, column_comment
    )


if __name__ == "__main__":
    main()


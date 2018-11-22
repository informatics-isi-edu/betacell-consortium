import argparse
from attrdict import AttrDict
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
from deriva.utils.catalog.manage import update_catalog

table_names = [
    'landmark',
    'model_json',
    'model',
    'model_mesh_data',
]

groups = AttrDict({
    'admins':
    'https://auth.globus.org/80df6c56-a0e8-11e8-b9dc-0ada61684422',
    'modelers':
    'https://auth.globus.org/a45e5ba2-709f-11e8-a40d-0e847f194132',
    'curators':
    'https://auth.globus.org/da80b96c-edab-11e8-80e2-0a7c1eab007a',
    'writers':
    'https://auth.globus.org/6a96ec62-7032-11e8-9132-0a043b872764',
    'readers':
    'https://auth.globus.org/aa5a2f6e-53e8-11e8-b60b-0a7c735d220a',
    'isrd':
    'https://auth.globus.org/3938e0d0-ed35-11e5-8641-22000ab4b42b'
})

tags = AttrDict({
    'immutable':
    'tag:isrd.isi.edu,2016:immutable',
    'display':
    'tag:misd.isi.edu,2015:display',
    'visible_columns':
    'tag:isrd.isi.edu,2016:visible-columns',
    'visible_foreign_keys':
    'tag:isrd.isi.edu,2016:visible-foreign-keys',
    'foreign_key':
    'tag:isrd.isi.edu,2016:foreign-key',
    'table_display':
    'tag:isrd.isi.edu,2016:table-display',
    'table_alternatives':
    'tag:isrd.isi.edu,2016:table-alternatives',
    'column_display':
    'tag:isrd.isi.edu,2016:column-display',
    'asset':
    'tag:isrd.isi.edu,2017:asset',
    'export':
    'tag:isrd.isi.edu,2016:export',
    'generated':
    'tag:isrd.isi.edu,2016:generated',
    'bulk_upload':
    'tag:isrd.isi.edu,2017:bulk-upload'
})

display = {'name_style': {'underline_space': True, 'title_case': True}}

annotations = {
    'tag:misd.isi.edu,2015:display': display,
}

acls = {
    'insert': [
        groups.writers,
        'https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b',
        groups.readers,
        'https://auth.globus.org/9d596ac6-22b9-11e6-b519-22000aef184d'
    ],
    'update': [
        groups.writers,
        'https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b',
        groups.readers
    ],
    'delete': [
        groups.writers,
        'https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b',
        groups.readers
    ]
}

comment = None

schema_def = em.Schema.define(
        'pbcconsortium.isrd.isi.edu',
        comment=comment,
        acls=acls,
        annotations=annotations,
    )


def main():
    server = 'pbcconsortium.isrd.isi.edu'
    catalog_id = 1
    schema_name = 'viz'
    
    mode, replace, server, catalog_id = update_catalog.parse_args(server, catalog_id)
    update_catalog.update_schema(mode, replace, server, catalog_id, schema_name, schema_def, annotations, acls, comment)


if __name__ == "__main__":
    main()

import argparse
from attrdict import AttrDict
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

schema_name = 'common'

table_names = ['person', ]

annotations = {chaise_tags.display: {'name_style': {'underline_space': True, 'title_case': True}}}

acls = {
    'insert': [
        'https://auth.globus.org/6a96ec62-7032-11e8-9132-0a043b872764',
        'https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b',
        'https://auth.globus.org/aa5a2f6e-53e8-11e8-b60b-0a7c735d220a',
        'https://auth.globus.org/9d596ac6-22b9-11e6-b519-22000aef184d'
    ],
    'update': [
        'https://auth.globus.org/6a96ec62-7032-11e8-9132-0a043b872764',
        'https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b',
        'https://auth.globus.org/aa5a2f6e-53e8-11e8-b60b-0a7c735d220a'
    ],
    'delete': [
        'https://auth.globus.org/6a96ec62-7032-11e8-9132-0a043b872764',
        'https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b',
        'https://auth.globus.org/aa5a2f6e-53e8-11e8-b60b-0a7c735d220a'
    ]
}

comment = None

schema_def = em.Schema.define('common', comment=comment, acls=acls, annotations=annotations, )


def main(catalog, mode, replace=False):
    updater = CatalogUpdater(catalog)
    updater.update_catalog.update_schema(mode, schema_name, schema_def, replace=replace)


if __name__ == "__main__":
    server = 'pbcconsortium.isrd.isi.edu'
    catalog_id = 1
    mode, replace, server, catalog_id = parse_args(server, catalog_id, is_catalog=True)
    credential = get_credential(server)
    catalog = ErmrestCatalog('https', server, catalog_id, credentials=credential)
    main(catalog, mode, replace)


import argparse
from attrdict import AttrDict
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

schema_name = '_acl_admin'

table_names = ['group_lists', ]

annotations = {}

acls = {}

comment = None

schema_def = em.Schema.define('_acl_admin', comment=comment, acls=acls, annotations=annotations, )


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


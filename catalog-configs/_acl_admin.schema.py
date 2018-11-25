import argparse
from attrdict import AttrDict
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage import update_catalog

table_names = ['group_lists', ]

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

annotations = {}

acls = {}

comment = None

schema_def = em.Schema.define(
    '_acl_admin', comment=comment, acls=acls, annotations=annotations,
)


def main():
    server = pbcconsortium.isrd.isi.edu
    catalog_id = 1
    schema_name = '_acl_admin'

    mode, replace, server, catalog_id = update_catalog.parse_args(server, catalog_id)
    update_catalog.update_schema(
        mode, replace, server, catalog_id, schema_name, schema_def, annotations, acls,
        comment
    )


if __name__ == "__main__":
    main()


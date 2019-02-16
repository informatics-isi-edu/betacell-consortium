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

table_name = 'PDB_Model'

schema_name = 'Beta_Cell'

column_annotations = {
    'RCB': {
        chaise_tags.display: {
            'markdown_name': 'Creator'
        },
        chaise_tags.column_display: {
            '*': {
                'markdown_pattern': '{{{$fkeys.Beta_Cell.PDB_Model_Creator_Fkey.values._display_name}}}'
            }
        }
    },
    'Owner': {
        chaise_tags.column_display: {
            '*': {
                'markdown_pattern': '{{{$fkeys.Beta_Cell.PDB_Model_Owner_Fkey.values._display_name}}}'
            }
        }
    },
    'PDB_Id': {}
}

column_comment = {'PDB_Id': 'PDB Identifier associated with the model'}

column_acls = {}

column_acl_bindings = {}

column_defs = [
    em.Column.define('Title', em.builtin_types['text'],
                     ),
    em.Column.define('Ingredient_ID', em.builtin_types['text'],
                     ),
    em.Column.define('Match_Length', em.builtin_types['int4'],
                     ),
    em.Column.define('Match_Length/Length_Seq_Origional', em.builtin_types['float8'],
                     ),
    em.Column.define('Seq_Coverage', em.builtin_types['float8'],
                     ),
    em.Column.define('PDB_Coverage', em.builtin_types['float8'],
                     ),
    em.Column.define('Score', em.builtin_types['text'],
                     ),
    em.Column.define('Expect', em.builtin_types['float8'],
                     ),
    em.Column.define('Length', em.builtin_types['int4'],
                     ),
    em.Column.define('Identities_(Percent)', em.builtin_types['float8'],
                     ),
    em.Column.define('Identities', em.builtin_types['text'],
                     ),
    em.Column.define('Positives_(Percent)', em.builtin_types['float8'],
                     ),
    em.Column.define('Positives', em.builtin_types['text'],
                     ),
    em.Column.define('Gaps_(Percent)', em.builtin_types['float8'],
                     ),
    em.Column.define('Gaps', em.builtin_types['text'],
                     ),
    em.Column.define('Organism', em.builtin_types['text'],
                     ),
    em.Column.define('Deposited', em.builtin_types['date'],
                     ),
    em.Column.define('Pseudo_Stoichiometry', em.builtin_types['text'],
                     ),
    em.Column.define('Weight', em.builtin_types['float8'],
                     ),
    em.Column.define('Atoms', em.builtin_types['int4'],
                     ),
    em.Column.define('Residues', em.builtin_types['int4'],
                     ),
    em.Column.define('OPM', em.builtin_types['text'],
                     ),
    em.Column.define('Method', em.builtin_types['text'],
                     ),
    em.Column.define('PDB_Title', em.builtin_types['text'],
                     ),
    em.Column.define('Chains', em.builtin_types['int4'],
                     ),
    em.Column.define('Owner', em.builtin_types['text'], annotations=column_annotations['Owner'],
                     ),
    em.Column.define('PDB_Id', em.builtin_types['text'], comment=column_comment['PDB_Id'],
                     ),
]

table_annotations = {}

table_comment = None

table_acls = {}

table_acl_bindings = {
    'self_service_owner': {
        'types': ['update', 'delete'],
        'scope_acl': ['*'],
        'projection': ['Owner'],
        'projection_type': 'acl'
    },
    'self_service_creator': {
        'types': ['update', 'delete'],
        'scope_acl': ['*'],
        'projection': ['RCB'],
        'projection_type': 'acl'
    }
}

key_defs = [em.Key.define(['RID'], constraint_names=[('Beta_Cell', 'PDB_Model_RID_Key')], ), ]

fkey_defs = [
    em.ForeignKey.define(
        ['PDB_Id'],
        'Vocab',
        'PDB_Term', ['ID'],
        constraint_names=[('Beta_Cell', 'PDB_Model_PDB_Term_FKey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='RESTRICT',
    ),
    em.ForeignKey.define(
        ['Ingredient_ID'],
        'Beta_Cell',
        'Ingredient', ['RID'],
        constraint_names=[('Beta_Cell', 'Ingredient_Ingredient_ID_FKey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='RESTRICT',
    ),
    em.ForeignKey.define(
        ['Organism'],
        'Vocab',
        'Organism_Term', ['id'],
        constraint_names=[('Beta_Cell', 'PDB_Model_Organism_Term_FKey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='RESTRICT',
    ),
    em.ForeignKey.define(
        ['Owner'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[('Beta_Cell', 'PDB_Model_Owner_Fkey')],
    ),
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[('Beta_Cell', 'PDB_Model_RCB_Fkey')],
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


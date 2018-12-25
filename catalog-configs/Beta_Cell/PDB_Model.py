import argparse
from attrdict import AttrDict
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

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
    'self_service_creator': {
        'scope_acl': ['*'],
        'projection': ['RCB'],
        'types': ['update', 'delete'],
        'projection_type': 'acl'
    },
    'self_service_owner': {
        'scope_acl': ['*'],
        'projection': ['Owner'],
        'types': ['update', 'delete'],
        'projection_type': 'acl'
    }
}

key_defs = [em.Key.define(['RID'], constraint_names=[('Beta_Cell', 'PDB_Model_RID_Key')], ), ]

fkey_defs = [
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ermrest_client', ['id'],
        constraint_names=[('Beta_Cell', 'PDB_Model_RCB_Fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
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
        'ermrest_client', ['id'],
        constraint_names=[('Beta_Cell', 'PDB_Model_Owner_Fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
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


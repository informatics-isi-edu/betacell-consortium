import argparse
from attrdict import AttrDict
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

schema_name = 'Beta_Cell'

table_names = [
    'Processed_Tomography_Data', 'Protocol', 'File', 'Collection_Biosample', 'PHYRE2_Model',
    'PDB_Model', 'Dataset', 'Experiment', 'XRay_Tomography_Data', 'Biosample',
    'Protocol_Step_Additive_Term', 'Cell_Line', 'Protocol_Step', 'Mass_Spec_Data', 'Specimen',
    'Protocol_Type', 'Ingredient',
]

annotations = {chaise_tags.display: {'name_style': {'underline_space': True}}}

acls = {}

comment = None

schema_def = em.Schema.define('Beta_Cell', comment=comment, acls=acls, annotations=annotations, )


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


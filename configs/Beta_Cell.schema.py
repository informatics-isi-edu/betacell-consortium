import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
import update_catalog

table_names = [
    'Processed_Tomography_Data',
    'Protocol',
    'File',
    'Collection_Biosample',
    'Specimen',
    'Dataset',
    'Experiment',
    'XRay_Tomography_Data',
    'Biosample',
    'Protocol_Step_Additive_Term',
    'Cell_Line',
    'Protocol_Step',
    'Mass_Spec_Data',
    'Protocol_Type',
]

display = {'name_style': {'underline_space': True}}

annotations = {'tag:misd.isi.edu,2015:display': display, }

acls = {}

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
    schema_name = 'Beta_Cell'
    update_catalog.update_schema(server, catalog_id, schema_name, schema_def, annotations, acls, comment)


if __name__ == "__main__":
    main()

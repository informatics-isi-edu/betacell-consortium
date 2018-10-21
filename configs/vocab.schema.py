import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
import update_catalog

table_names = [
    'uniprot_terms',
    'anatomy_terms',
    'cellular_location_terms',
    'data_type_terms',
    'cell_line_terms',
    'experiment_type_terms',
    'file_type_terms',
    'file_format_terms',
    'specimen_type_terms',
    'species_terms',
]

display = {'name_style': {'title_case': True, 'underline_space': True}}

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
    schema_name = 'vocab'
    update_catalog.update_schema(server, catalog_id, schema_name, schema_def, annotations, acls, comment)


if __name__ == "__main__":
    main()

import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
import update_catalog

table_names = [
    'landmark',
    'model_json',
    'model',
    'model_mesh_data',
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
    schema_name = 'viz'
    update_catalog.update_schema(server, catalog_id, schema_name, schema_def, annotations, acls, comment)


if __name__ == "__main__":
    main()

import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
import update_catalog

table_names = [
    'person',
]

display = {'name_style': {'title_case': True, 'underline_space': True}}

annotations = {'tag:misd.isi.edu,2015:display': display, }

acls = {
    'delete': [
        'https://auth.globus.org/6a96ec62-7032-11e8-9132-0a043b872764',
        'https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b',
        'https://auth.globus.org/aa5a2f6e-53e8-11e8-b60b-0a7c735d220a'],
    'insert': [
        'https://auth.globus.org/6a96ec62-7032-11e8-9132-0a043b872764',
        'https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b',
        'https://auth.globus.org/aa5a2f6e-53e8-11e8-b60b-0a7c735d220a',
        'https://auth.globus.org/9d596ac6-22b9-11e6-b519-22000aef184d'],
    'update': [
        'https://auth.globus.org/6a96ec62-7032-11e8-9132-0a043b872764',
        'https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b',
        'https://auth.globus.org/aa5a2f6e-53e8-11e8-b60b-0a7c735d220a']}

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
    schema_name = 'common'
    
    mode, replace, server, catalog_id = update_catalog.parse_args(server, catalog_id)
    update_catalog.update_schema(mode, replace, server, catalog_id, schema_name, schema_def, annotations, acls, comment)


if __name__ == "__main__":
    main()

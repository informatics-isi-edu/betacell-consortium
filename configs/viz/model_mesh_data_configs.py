import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
    
annotations = \
{   'tag:isrd.isi.edu,2016:table-display': {},
    'tag:isrd.isi.edu,2016:visible-columns': {},
    'tag:isrd.isi.edu,2016:visible-foreign-keys': {}}

def main():
        parser = argparse.ArgumentParser(description='Load foreign key defs for table viz:model_mesh_data')
        parser.add_argument('--server', default='pbcconsortium.isrd.isi.edu',
                            help='Catalog server name')
        args = parser.parse_args()

        server = args.server
        schema_name = 'viz'
        table_name = 'model_mesh_data'

        credential = get_credential(server)
        catalog = ErmrestCatalog('https', server, 1, credentials=credential)
        model_root = catalog.getCatalogModel()
        schema = model_root.schemas[schema_name]
        table = schema.tables[table_name]

        if len(visible_columns) > 0:
            for k, v in visible_columns.items():
                table.visible_columns[k] = v

        if len(visible_foreign_keys) > 0:
            for k, v in visible_foreign_keys.items():
                table.visible_foreign_keys[k] = v
        table.annotations['table_display'] = table_display

        table.apply(catalog)


if __name__ == "__main__":
        main()

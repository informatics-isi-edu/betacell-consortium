import dump_table
import dump_schema
import os
from deriva.core import ErmrestCatalog, get_credential

server = 'pbcconsortium.isrd.isi.edu'


credential = get_credential(server)
catalog = ErmrestCatalog('https', server, 1, credentials=credential)
model_root = catalog.getCatalogModel()

for schema_name, schema in model_root.schemas.items():
    filename = 'configs/{}.schema.py'.format(schema_name)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as f:
        dump_schema.print_schema(server, schema_name, f)
    f.close()

    for i in schema.tables:
        print('Dumping {},{}'.format(schema_name, i))
        filename = 'configs/{}/{}.py'.format(schema_name, i)
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w') as f:
            print('dumping table ', filename)
            dump_table.print_defs(server, schema_name, i, f)
        f.close()
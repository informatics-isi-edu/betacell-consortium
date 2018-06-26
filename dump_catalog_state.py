import dump_table_def
import dump_schema
import os

server = 'pbcconsortium.isrd.isi.edu'
table_list = {
        'isa' :['biosample', 'dataset', 'experiment','protocol','protocol_treatment','replicate','specimen',
                                                        'xray_tomography_data', 'dataset_experiment_type', 'project', 'person', 'mesh_data'],
    'vocab' : [ 'treatment_terms','specimen_terms' ],
    'viz' : ['model', 'model_mesh_data'],
    'common' : []
}

for schema_name in ['vocab', 'isa', 'viz']:

    filename = 'configs/{}.schema.py'.format(schema_name)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as f:
        dump_schema.print_schema(server, schema_name, f)
    f.close()

    for i in table_list[schema_name]:
        print('Dumping {},{}'.format(schema_name, i))

        for i in table_list[schema_name]:
            filename = 'configs/{}/{}_def.py'.format(schema_name, i)
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, 'w') as f:
                dump_table_def.print_defs(server, schema_name, i,f)
            f.close()
tag_names = {
    'tag:isrd.isi.edu,2016:generated',
    'tag:isrd.isi.edu,2016:immutable',
    'tag:misd.isi.edu,2015:display',
    'tag:isrd.isi.edu,2016:visible-columns',
    'tag:isrd.isi.edu,2016:visible-foreign-keys',
    'tag:isrd.isi.edu,2016:foreign-key',
    'tag:isrd.isi.edu,2016:table-display',
    'tag:isrd.isi.edu,2016:table-alternatives',
    'tag:isrd.isi.edu,2016:column-display',
    'tag:isrd.isi.edu,2017:asset',
    'tag:isrd.isi.edu,2016:export',
}

aggregate_names = ['max', 'min', 'array', 'array_d', 'cnt', 'cnt_d']:

def validate_pseudocolumn(spec, context):
    for k, v in spec.items():
        if k is "entity" and (v is True or v is False):
            continue
        if (k == "markdown_name" or k == 'comment') and type(v) is str:
            continue
        if k == 'source' and type(v) is list:
            continue
        if k == 'aggregate' and v in aggregate_names:
            continue
        print('Invalid pseudocolumn spec {} {}:{}'.format(context, k, v))


def lint_path(fk_path, model, table, context):
    path = ''
    for fk in fk_path:
        # Get list of column names.
        cnames = [i.name for i in table.column_definitions]

        # Construct a map of constraint names to target tables.
        out_fkeys = {i.names[0][0] + ':' + i.names[0][1]:
                     model.schemas[i.referenced_columns[0]['schema_name']].tables[i.referenced_columns[0]['table_name']]
            for i in table.foreign_keys}
        in_fkeys = {i.names[0][0] + ":" + i.names[0][1]:
                        model.schemas[i.sname].tables[i.tname]
            for i in table.referenced_by}

        if type(fk) == str:
            # Column name
            path = path + '/' + fk
            if fk not in cnames:
                print('Invalid  column name {} {}'.format(context, path))
        elif type(fk) is list:
            # Old style column name [schema, fkey]
            k = '{}:{}'.format(*fk)
            path = path + '/' + k
            if not (k in out_fkeys or k in in_fkeys):
                print('Bad columm spec {} {}'.format(context, path))
        elif 'inbound' in fk:
            k = '{}:{}'.format(*fk['inbound'])
            path = path + '/' + k
            if not k in in_fkeys:
                print('Bad column spec: {} {}'.format(context, path))
                return
            else:
                table = in_fkeys[k]
        elif 'outbound' in fk:
            k = '{}:{}'.format(*fk['outbound'])
            path = path + '/' + k
            if not k in out_fkeys:
                print('Bad column spec: {} {}'.format(context, path))
                return
            else:
                table = out_fkeys[k]
        elif fk in ['choices', 'ranges', 'search', 'not_null']:
            pass
        else:
            print('{}: Bad path element {}'.format(context, path))

def lint_columns( column_list, model, table, context):
    cnames = [i.name for i in table.column_definitions]
    out_fkeys = [i.names[0] for i in table.foreign_keys]
    in_fkeys = [i.names[0] for i in table.referenced_by]
    for i in column_list:
        if type(i) == str:
            # Column name
            if i not in cnames:
                print('{}: Invalid column name {}'.format(context, i))
        elif type(i) is list:
            # Old style column name [schema, fkey]
            lint_path([i], model, table, context)
        elif type(i) is dict:
            validate_pseudocolumn(i, context)
            lint_path( i['source'], model, table, context)
        else:
            print('Unknown path {}'.format(i))


def lint_table(catalog, table):
    model_root = catalog.getCatalogModel()
    # Check to see if all the annotations are valid
    for i in table.annotations.keys():
        if i not in tag_names:
            print("Invalid tag: {}".format(i))

    for f, a in table.visible_columns.items():
        if f not in ['*', 'filter', 'compact', 'detailed', 'entry']:
            print('Invalid context: {}'.format(f))
            continue
        if f == 'filter':
            lint_columns( a['and'], model_root, table, 'visible_column[{}]'.format(f))
        else:
            lint_columns( a, model_root, table, 'visible_column[{}]'.format(f))

    for f, a in table.visible_foreign_keys.items():
        if f not in ['*', 'compact', 'detailed', 'entry']:
            print('Invalid context {}'.format(f))
            continue
        if f == 'filter':
            lint_columns( a['and'], model_root, table, 'visible_foreign_key[{}]'.format(f))
        else:
            lint_columns( a, model_root, table, 'visible_foreign_keys[{}]'.format(f))

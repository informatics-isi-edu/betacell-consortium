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

def lint_path(fk_path, model, table, context):
    for fk in fk_path:
        cnames = [i.name for i in table.column_definitions]
        out_fkeys = {i.names[0][0] + ':' + i.names[0][1]:
                     model.schemas[i.referenced_columns[0]['schema_name']].tables[i.referenced_columns[0]['table_name']]
            for i in table.foreign_keys}
        in_fkeys = {i.names[0][0] + ":" + i.names[0][1]:
                        model.schemas[i.referenced_columns[0]['schema_name']].tables[i.referenced_columns[0]['table_name']]
            for i in table.referenced_by}
        if type(fk) == str:
            # Column name
            if fk not in cnames:
                print('Invalid  column name {} {}'.format(context, fk))
        elif 'inbound' in fk:
            k = '{}:{}'.format(*fk['inbound'])
            if not k in in_fkeys:
                print('missing in path fkey {} {}'.format(context, fk))
                return
            else:
                table = in_fkeys[k]
        elif 'outbound' in fk:
            k = '{}:{}'.format(*fk['outbound'])
            if not k in out_fkeys:
                print('missing out path fkey {} {}'.format(context, fk))
                return
            else:
                table = out_fkeys[k]
        else:
            print('Bad path element {}'.format(fk))


def lint_columns( column_list, model, table, context):
    cnames = [i.name for i in table.column_definitions]
    out_fkeys = [i.names[0] for i in table.foreign_keys]
    in_fkeys = [i.names[0] for i in table.referenced_by]
    for i in column_list:
        if type(i) == str:
            # Column name
            if i not in cnames:
                print('Invalid column name {} {}'.format(context, i))
        elif type(i) is list:
            # Old style column name [schema, fkey]
            if not (tuple(i) in out_fkeys or tuple(i) in in_fkeys):
                print('missing fkey {} {}'.format(context, i))
        elif type(i) is dict:
            lint_path( i['source'], model, table, context)
        else:
            print('Unknown path {}'.format(i))


def lint_table(catalog, table):
    model_root = catalog.getCatalogModel()
    # Check to see if all the annotations are valid
    for i in table.annotations.keys():
        if i not in tag_names:
            print("Invalid tag {}".format(i))

    for f, a in table.visible_columns.items():
        if f not in ['*', 'filter', 'compact', 'detailed', 'entry']:
            print('Invalid context {}'.format(f))
            continue
        if f == 'filter':
            lint_columns( a['and'], model_root, table, 'visible_column[{}]'.format(f))
        else:
            lint_columns( a, model_root, table, 'visible_column[{}]'.format(f))

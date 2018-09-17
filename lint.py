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

aggregate_names = ['max', 'min', 'array', 'array_d', 'cnt', 'cnt_d']
constraint_names = ['choices', 'ranges', 'search', 'not_null']

def is_pure_binary(table):
    # table has only two foreign_key constraints.
    if len(table.foreign_keys) != 2:
        return (False,'more then two fkeys')

    # Each constraint is over only one column.
    if len(table.foreign_keys[0].foreign_key_columns) != 1:
        return (False,'more then one column in fkey constraint {}'.format(table.foreign_keys[0].foreign_key_columns))
    if len(table.foreign_keys[1].foreign_key_columns) != 1:
        return (False,'more then one column in fkey constraint {}'.format(table.foreign_keys[1].foreign_key_columns))

    fk0 = table.foreign_keys[0].foreign_key_columns[0]['column_name']
    fk1 = table.foreign_keys[1].foreign_key_columns[0]['column_name']
    c = False

    # There is a uniqeness constraint on the pair of fkey columns.
    for i in table.keys:
        if fk0 in i.unique_columns and fk1 in i.unique_columns:
            c = True
    if not c:
        return(False, 'no uniqueness key on fkeys')

    # Null is not allowed on the column.
    if table.column_definitions[fk0].nullok:
        return(False, 'null allowed in fkey column: {}'.format(fk0))
    if table.column_definitions[fk1].nullok:
        return(False, 'null allowed in fkey column: {}'.format(fk1))

    return (True, '')

def validate_filter_terms(spec, context):
    for k, v in spec.items():
        if (k == "entity" or k == 'open') and (v == True or v == False):
            continue
        if (k == "markdown_name" or k == 'comment') and type(v) is str:
            continue
        if k == 'source' and (type(v) is list or type(v) is str):
            continue
        if k == 'aggregate' and v in aggregate_names:
            continue
        if k in constraint_names:
            continue
        if k == 'ux_mode':
            continue
        print('Invalid filter spec {} {}:{}'.format(context, k, v))


def validate_source(source, model, table, columns, inbound_tables, outbound_tables):
    """

    :param source: A source list of either column names, fkey constraints, or inbound/outbound dicts.
    :param model: deriva_py model class
    :param table:  deriva_py table object.
    :return:
    """

    path = ''

    for fk in source:
        table_name = '{}:{}'.format(table.sname, table.name)

        # Get list of column names.
        cnames = columns.setdefault(table_name,
                                    [i.name for i in table.column_definitions] + [i.names for i in table.keys])

        # Construct a map of constraint names to target tables if we have not already done so.
        out_fkeys = outbound_tables.setdefault(table_name,
                                               {'{}:{}'.format(*i.names[0]):
                                                    model.schemas[i.referenced_columns[0]['schema_name']].tables[
                                                        i.referenced_columns[0]['table_name']]
                                                for i in table.foreign_keys})
        in_fkeys = inbound_tables.setdefault(table_name,
                                             {'{}:{}'.format(*i.names[0]):
                                                  model.schemas[i.sname].tables[i.tname]
                                              for i in table.referenced_by})
        if type(fk) == str:
            # Column name
            path += '/' + fk
            if fk not in cnames:
                return (False, 'unknown column: {}'.format(path))
        elif type(fk) is list:
            # Old style column name [schema, fkey]
            fk_name = '{}:{}'.format(*fk)
            path = path + '/' + fk_name
            if not (fk_name in out_fkeys or table_name in in_fkeys):
                return (False, 'unknown fkey constraint: {}'.format(path))
        elif 'inbound' in fk:
            fk_name = '{}:{}'.format(*fk['inbound'])
            path +=  '/' + fk_name
            if not fk_name in in_fkeys:
                return (False, 'unknown inbound fkey constraint: {}'.format(path))
            else:
                table = in_fkeys[fk_name]
        elif 'outbound' in fk:
            fk_name = '{}:{}'.format(*fk['outbound'])
            path +=  '/' + fk_name
            if not fk_name in out_fkeys:
                return (False, 'unknown outbound fkey constraint: {}'.format(path))
            else:
                table = out_fkeys[fk_name]
        else:
            return (False, 'invalid path element: {}')
    return (True,path)


def validate_columns(column_list, model, table, context):
    columns, inbound, outbound = {}, {}, {}

    for i in column_list:
        if type(i) is dict:
            validate_filter_terms(i, context)
            source = i['source']
        else:
            source = i
        # Normalize source path so that its a list.
        if type(source) == str:
            # Column name...
            source = [source]
        elif type(source) is list and len(source) == 2 and type(source[0]) == str and type(source[1]) == str:
            # Old style column name [schema, fkey]
            source = [source]
        (valid, msg) = validate_source(source, model, table, columns, inbound, outbound)
        if not valid:
            print('ERROR: {} {}'.format(context, msg ))

def lint_table(catalog, table):
    model_root = catalog.getCatalogModel()

    # Check to see if all the annotations are valid
    for i in table.annotations.keys():
        if i not in tag_names:
            print("Invalid tag: {}".format(i))

    # Check visitble_columns annotation to make sure its ok....
    for f, a in table.visible_columns.items():
        if f not in ['*', 'filter', 'compact', 'detailed', 'entry']:
            print('Invalid context: {}'.format(f))
            continue
        if f == 'filter':
            validate_columns(a['and'], model_root, table, 'visible_column[{}]'.format(f))
        else:
            validate_columns(a, model_root, table, 'visible_column[{}]'.format(f))

    for f, a in table.visible_foreign_keys.items():
        if f not in ['*', 'compact', 'detailed', 'entry']:
            print('Invalid context {}'.format(f))
            continue
        if f == 'filter':
            validate_columns(a['and'], model_root, table, 'visible_foreign_key[{}]'.format(f))
        else:
            validate_columns(a, model_root, table, 'visible_foreign_keys[{}]'.format(f))

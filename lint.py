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
    """
    Check to see if the table has the propoerties of a pure binary association.  That is it only has two foreign keys:
      1. It only has two foreign keys,
      2. There is a uniqueness constraint on the two keys.
      3. NULL values are not allowed in the foreign keys.
    :param table:
    :return:
    """
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

def validate_filter_terms(spec):
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
        return [('warning','Invalid filter spec {}:{}'.format(k, v))]
    return []


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
                                    [i.name for i in table.column_definitions] + [i.names[0][1] for i in table.keys])

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
                return [('error', 'unknown column: {}'.format(path))]
        elif type(fk) is list:
            # Old style column name [schema, fkey]
            fk_name = '{}:{}'.format(*fk)
            path = path + '/' + fk_name
            if not (fk_name in out_fkeys or fk_name in in_fkeys or fk[1] in cnames):
                return [('error', 'unknown fkey constraint: {}'.format(path))]
        elif 'inbound' in fk:
            fk_name = '{}:{}'.format(*fk['inbound'])
            path +=  '/' + fk_name
            if not fk_name in in_fkeys:
                return [('error', 'unknown inbound fkey constraint: {}'.format(path))]
            else:
                # Move on to next element in the path
                table = in_fkeys[fk_name]
        elif 'outbound' in fk:
            fk_name = '{}:{}'.format(*fk['outbound'])
            path +=  '/' + fk_name
            if not fk_name in out_fkeys:
                return [('error', 'unknown outbound fkey constraint: {}'.format(path))]
            else:
                # Move on to next element in path
                table = out_fkeys[fk_name]
        else:
            return [('error', 'invalid path element: {}')]
    return []


def validate_columns(column_list, model, table):
    columns, inbound, outbound = {}, {}, {}
    results = []

    for i in column_list:
        if type(i) is dict:
            results.extend(validate_filter_terms(i))
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
        results.extend(validate_source(source, model, table, columns, inbound, outbound))
    return results

def validate_table(catalog, table):
    model_root = catalog.getCatalogModel()

    # Check to see if all the annotations are valid
    for i in table.annotations.keys():
        if i not in tag_names:
            print("Invalid tag: {}".format(i))


    # Check visible_columns annotation to make sure its ok....
    vc_results = {}
    for f, a in table.visible_columns.items():
        if f not in ['*', 'filter', 'compact', 'detailed', 'entry']:
            vc_results.setdefault('unknown',[]).append(('warning','Invalid context: {}'.format(f)))
            continue
        if f == 'filter':
            if not 'and' in a:
                vc_results['filter'] = [('error','Invalid filter spec')]
            else:
                vc_results['filter'] = validate_columns(a['and'], model_root, table)
        else:
            vc_results[f] = validate_columns(a, model_root, table)
    fk_results = {}
    for f, a in table.visible_foreign_keys.items():
        if f not in ['*', 'compact', 'detailed', 'entry']:
            fk_results.setdefault('unknown', []).append(('warning', 'Invalid context: {}'.format(f)))
            continue
        if f == 'filter':
            fk_results['filter'] = validate_columns(a['and'], model_root, table)
        else:
            fk_results[f] = validate_columns(a, model_root, table)

    print("Table {}.visible_columns".format(table.name))
    print_validation_results(vc_results)
    print("Table {}.visible_foreign_keys".format(table.name))
    print_validation_results(fk_results)


def print_validation_results(validations):
    for k,v in validations.items():
        if len(v):
            print('    {}'.format(k))
        for i in v:
                print('        {}: {}'.format(i[0],i[1]))


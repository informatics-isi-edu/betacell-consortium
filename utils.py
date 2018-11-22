
import deriva.core.ermrest_model as em
from deriva.core import ErmrestCatalog, get_credential
from requests.exceptions import HTTPError


def setup_table(server, catalog_id, schema_name, table_name):
    credential = get_credential(server)
    catalog = ErmrestCatalog('https', server, catalog_id, credentials=credential)
    model_root = catalog.getCatalogModel()
    schema = model_root.schemas[schema_name]
    table = schema.tables[table_name]

    # Make table policy be self service, creators can update.
    self_service_policy = {
        "self_service": {
            "types": ["update", "delete"],
            "projection": ["RCB"],
            "projection_type": "acl"
        }
    }
    table.acl_bindings.update(self_service_policy)
    model_root.apply(catalog)

    # Set up foreign key to ermrest_client on RCB.
    fk_name = '{}_RCB_Fkey'.format(table_name)
    fk = em.ForeignKey.define(
        ['RCB'],
        'public',
        'ermrest_client',
        ['id'],
        constraint_names=[(schema_name, fk_name)],
    )

    try:
        # Delete old fkey if there is one laying around....
        f = table.foreign_keys[(schema_name, fk_name)]
        f.delete(catalog, table)
    except KeyError:
        pass
    table.create_fkey(catalog, fk)

    # Add a display annotation so that we use the user name on RCB
    column_annotation = {
        'tag:isrd.isi.edu,2016:column-display' :
            {'*': {'markdown_pattern': '{{{{{{$fkeys.{}.{}.values._display_name}}}}}}'.format(schema_name,fk_name)}},
        'tag:misd.isi.edu,2015:display' : {'*': {'markdown_name': 'Owner'}}
    }
    table.column_definitions['RCB'].annotations.clear()
    table.column_definitions['RCB'].annotations.update(column_annotation)
    model_root.apply(catalog)

    return

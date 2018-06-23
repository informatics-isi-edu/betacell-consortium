import argparse
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
    
visible_columns = \
{   '*': [   'name',
             'dbxref',
             'definition',
             ['vocab', 'specimen_terms_cv_fkey'],
             'is_obsolete',
             'is_relationshiptype',
             'synonyms',
             'alternate_dbxrefs'],
    'entry': [['vocab', 'specimen_terms_dbxref_fkey']],
    'filter': {   'and': [   {'source': 'name'},
                             {'source': 'dbxref'},
                             {'source': 'definition'},
                             {'source': 'cv'},
                             {'source': 'is_obsolete'},
                             {'source': 'is_relationshiptype'}]}}
visible_foreign_keys = \
{   '*': [   {   'source': [   {   'inbound': [   'isa',
                                                  'dataset_specimen_specimen_fkey']},
                               {   'outbound': [   'isa',
                                                   'dataset_specimen_dataset_id_fkey']},
                               'id']}]}
table_display = \
{   '*': {'row_order': [{'column': 'name'}]},
    'row_name': {'row_markdown_pattern': '{{name}}'}}
annotations = \
{   'tag:isrd.isi.edu,2016:table-display': {   '*': {   'row_order': [   {   'column': 'name'}]},
                                               'row_name': {   'row_markdown_pattern': '{{name}}'}},
    'tag:isrd.isi.edu,2016:visible-columns': {   '*': [   'name',
                                                          'dbxref',
                                                          'definition',
                                                          [   'vocab',
                                                              'specimen_terms_cv_fkey'],
                                                          'is_obsolete',
                                                          'is_relationshiptype',
                                                          'synonyms',
                                                          'alternate_dbxrefs'],
                                                 'entry': [   [   'vocab',
                                                                  'specimen_terms_dbxref_fkey']],
                                                 'filter': {   'and': [   {   'source': 'name'},
                                                                          {   'source': 'dbxref'},
                                                                          {   'source': 'definition'},
                                                                          {   'source': 'cv'},
                                                                          {   'source': 'is_obsolete'},
                                                                          {   'source': 'is_relationshiptype'}]}},
    'tag:isrd.isi.edu,2016:visible-foreign-keys': {   '*': [   {   'source': [   {   'inbound': [   'isa',
                                                                                                    'dataset_specimen_specimen_fkey']},
                                                                                 {   'outbound': [   'isa',
                                                                                                     'dataset_specimen_dataset_id_fkey']},
                                                                                 'id']}]}}
column_annotations = \
{   'alternate_dbxrefs': {   'tag:isrd.isi.edu,2016:generated': None,
                             'tag:misd.isi.edu,2015:display': {   'name': 'Alternate '
                                                                          'Codes'}},
    'cv': {   'tag:isrd.isi.edu,2016:generated': None,
              'tag:misd.isi.edu,2015:display': {   'name': 'Controlled '
                                                           'Vocabulary'}},
    'dbxref': {   'tag:isrd.isi.edu,2016:column-display': {   '*': {   'markdown_pattern': '[{{dbxref}}](/chaise/record/#1/data_commons:cvterm/dbxref={{#encode}}{{dbxref}}{{/encode}})'}},
                  'tag:misd.isi.edu,2015:display': {'name': 'Code'}},
    'dbxref_unversioned': {'tag:isrd.isi.edu,2016:generated': None},
    'definition': {'tag:isrd.isi.edu,2016:generated': None},
    'is_obsolete': {'tag:isrd.isi.edu,2016:generated': None},
    'is_relationshiptype': {'tag:isrd.isi.edu,2016:generated': None},
    'name': {'tag:isrd.isi.edu,2016:generated': None},
    'synonyms': {'tag:isrd.isi.edu,2016:generated': None}}

def main():
        parser = argparse.ArgumentParser(description='Load foreign key defs for table vocab:specimen_terms')
        parser.add_argument('--server', default='pbcconsortium.isrd.isi.edu',
                            help='Catalog server name')
        args = parser.parse_args()

        server = args.server
        schema_name = 'vocab'
        table_name = 'specimen_terms'

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

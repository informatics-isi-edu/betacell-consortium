from deriva.core import HatracStore, ErmrestCatalog, ErmrestSnapshot, get_credential, DerivaPathError
import deriva.core.ermrest_model as em
import csv
import re
import os
import subprocess
import shutil
import tempfile

pbcserver = 'pbcconsortium.isrd.isi.edu'
credential = get_credential(pbcserver)
catalog = ErmrestCatalog('https', pbcserver, 1, credentials=credential)


xray_tomography = 'commons:599:'
pancreas = 'UBERON:0001264:'
dataset_key ='1-882P'

for i in file_map:
    re.sub('_[0-9]?_pre_rec$','', file_map[0][3]) + '/' + file_map[0][3]


def add_file_to_replicant(dataset_rid, fmap, description = ''):
    """
    Upload a file into a data collection and add that file into the set of files associated with a cohort analysis.
    :param file: local path to the file that should be uploaded and associated with the cohort
    :param description: Text that is used to describe the file that is being uploaded
    :param cohort: RID of the analysis cohort to which the file file should be assoicated.
    :return: None.
    """
    credential = get_credential(pbcserver)
    store = HatracStore('https', pbcserver, credentials=credential)
    catalog = ErmrestCatalog('https', pbcserver, 1, credentials=credential)

    (experiment_rid, biosample_rid, replicate_rid, filename) = fmap
    dirname = re.sub('_[0-9]+_pre_rec$', '', filename)
    filename = filename + '.mrc'
    path = '{}/{}'.format(dirname,filename)
    print('Uploading ', path)
    objpath = '/hatrac/commons/data/{}/{}/{}?parents=true'.format(dataset_rid, replicate_rid, os.path.basename(filename))
    print('to ', objpath)
    loc = store.put_obj(objpath, path)
    print(loc)
    r = store.head(objpath)
    md5 = r.headers['content-md5']
    byte_count = r.headers['Content-Length']
    submit_time = r.headers['Date']

    file = {
        'dataset' : dataset_rid,
        'anatomy': pancreas,
        'device' : xray_tomography,
        'equipment_model': 'commons:600:',
        'description' :description,
        'url' : loc,
        'filename' : os.path.basename(filename),
        'file_type' : 'commons:601:',
        'byte_count': byte_count,
        'submitted_on' : submit_time,
        'md5' : md5,
        'replicate' : replicate_rid
    }
    print(file)

    pb = catalog.getPathBuilder()
    isa = pb.isa

    tomography_data = isa.tables['xray_tomography_data']
    try:
        newrid = tomography_data.insert([file])
    except:
        newrid = tomography_data.update([file])
    return

def hack_file_to_replicant(dataset_rid, fmap, description = ''):
    """
    Upload a file into a data collection and add that file into the set of files associated with a cohort analysis.
    :param file: local path to the file that should be uploaded and associated with the cohort
    :param description: Text that is used to describe the file that is being uploaded
    :param cohort: RID of the analysis cohort to which the file file should be assoicated.
    :return: None.
    """
    credential = get_credential(pbcserver)

    (experiment_rid, biosample_rid, replicate_rid, filename) = fmap
    dirname = re.sub('_[0-9]+_pre_rec$', '', filename)
    filename = filename + '.mrc'
    path = '{}/{}'.format(dirname,filename)
    print('Uploading ', path)
    objpath = '/hatrac/commons/data/{}/{}/{}?parents=true'.format(dataset_rid, replicate_rid, os.path.basename(filename))
    print('to ', objpath)
 #   loc = store.put_obj(objpath, path)
    (loc, md5, byte_count, submit_time) = filedict[filename]

    file = {
        'dataset' : dataset_rid,
        'anatomy': pancreas,
        'device' : 'commons:599:',
        'equipment_model': 'commons:600:',
        'description' :description,
        'url' : loc,
        'filename' : os.path.basename(filename),
        'file_type' : 'commons:601:',
        'byte_count': byte_count,
        'submitted_on' : submit_time,
        'md5' : md5,
        'replicate' : replicate_rid
    }

    pb = catalog.getPathBuilder()
    isa = pb.isa

    tomography_data = isa.tables['xray_tomography_data']
    try:
        newrid = tomography_data.insert([file])
    except:
        newrid = tomography_data.update([file])
    return


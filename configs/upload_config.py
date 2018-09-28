upload_spec = {
    "asset_mappings": [
        {
            "asset_type": "table",
            "default_columns": [
                "RID",
                "RCB",
                "RMB",
                "RCT",
                "RMT"
            ],
            "ext_pattern": "^.*[.](?P<file_ext>json|csv)$",
            "file_pattern": "^((?!/assets/).)*/records/(?P<schema>.+?)/(?P<table>.+?)[.]"
        },
        {
            "checksum_types": [
                "md5"
            ],
            "column_map": {
                "biosample": "{biosample_rid}",
                "byte_count": "{file_size}",
                "dataset": "{dataset_rid}",
                "filename": "{file_name}",
                "md5": "{md5}",
                "url": "{URI}"
            },
            "create_record_before_upload": "False",
            "dir_pattern": "^.*/DS-(?P<dataset>[0-9A-Z-]+)/EXP-(?P<experiment>[0-9A-Z-]+)",
            "ext_pattern": ".mrc$",
            "file_pattern": ".*_(?P<capillary>[0-9]+)_(?P<position>[0-9]+)_pre_rec",
            "hatrac_templates": {
                "hatrac_uri": "/hatrac/commons/data/{dataset_rid}/{biosample_rid}/{file_name}"
            },
            "metadata_query_templates": [
                "/attribute/D:=Beta_Cell:Dataset/E:=Beta_Cell:Experiment/RID={experiment}/B:=Beta_Cell:Biosample/Capillary_Number={capillary}/Sample_Position={position}/dataset_rid:=D:RID,experiment_rid:=E:RID,biosample_rid:=B:RID"
            ],
            "record_query_template": "/entity/{target_table}/Dataset={dataset_rid}/Biosample={biosample_rid}/URL={URI_urlencoded}",
            "target_table": [
                "Beta_Cell",
                "XRay_tomography_data"
            ]
        }
    ],
    "version_compatibility": [
        [
            ">=0.4.3",
            "<1.0.0"
        ]
    ],
    "version_update_url": "https://github.com/informatics-isi-edu/deriva-qt/releases"
}

# model_root.annotations['tag:isrd.isi.edu,2017:bulk-upload'] = upload_spec
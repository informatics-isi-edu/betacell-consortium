# Admins:  complete control
# Modelers: Can update catalog schema
# Curator: read and write any data
# Writer: Read and write data created by user
# Reader: Can read any data.

groups = {
    "admins": "https://auth.globus.org/80df6c56-a0e8-11e8-b9dc-0ada61684422",
    "modelers": "https://auth.globus.org/a45e5ba2-709f-11e8-a40d-0e847f194132",
    "curators": "https://auth.globus.org/da80b96c-edab-11e8-80e2-0a7c1eab007a",
    "writers": "https://auth.globus.org/6a96ec62-7032-11e8-9132-0a043b872764",
    "readers": "https://auth.globus.org/aa5a2f6e-53e8-11e8-b60b-0a7c735d220a",
    "isrd": 'https://auth.globus.org/3938e0d0-ed35-11e5-8641-22000ab4b42b'
}

self_service_policy = {
    "self_service_creator": {
        "types": ["update", "delete"],
        "projection": ["RCB"],
        "projection_type": "acl"
    },
    "self_service_owner": {
        "types": ["update", "delete"],
        "projection": ["Owner"],
        "projection_type": "acl"
    }
}

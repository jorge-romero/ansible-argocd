#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


import requests

from ansible.module_utils.basic import AnsibleModule

# Correct the import statement
try:
    from ansible_collections.bitertech.argocd.plugins.module_utils.argocd_api import ArgoCDClient
except ImportError as imp_exc:
    ANOTHER_LIBRARY_IMPORT_ERROR = imp_exc
else:
    ANOTHER_LIBRARY_IMPORT_ERROR = None


def main():

    fields = {
        "api_url": {"required": True, "type": 'str'},
        "token": {"required": True, "type": 'str'},
        "name": {"required": True, "type": 'str'},
        "repository_url": {"required": True, "type": 'str'},
        "path": {"required": True, "type": 'str'},
        "target_revision": {"required": True, "type": 'str'},
        "namespace": {"required": True, "type": 'str'},
        "values_files": {"required": False, "type": 'str'},
        "destination_server": {"required": False, "type": 'str'},
        "project": {"required": False, "type": "str"},
        "status": {"type": "str", "choices": ["present", "absent"], "default": "present"}
    }

    module = AnsibleModule(
        argument_spec=fields
    )

    api_url = module.params["api_url"]
    token = module.params["token"]
    name = module.params["name"]
    repository_url = module.params["repository_url"]
    path = module.params["path"]
    target_revision = module.params["target_revision"]
    namespace = module.params["namespace"]
    values_files = module.params["values_files"]
    destination_server = module.params["destination_server"]
    project = module.params["project"]
    status = module.params["status"]

    try:
        client = ArgoCDClient(api_url, token)
        if status == "present":
            result = client.create_application(name,
                                               repository_url,
                                               path,
                                               target_revision,
                                               values_files=values_files,
                                               destination_server=destination_server,
                                               namespace=namespace,
                                               project=project)
        module.exit_json(changed=True, result=result)
    except requests.exceptions.HTTPError as errh:
        module.fail_json(msg=str(errh.response.json()))
    except requests.exceptions.ReadTimeout as errrt:
        module.fail_json(msg=str(errrt))
    except requests.exceptions.ConnectionError as conerr:
        module.fail_json(msg=str(conerr))
    except requests.exceptions.RequestException as errex:
        module.fail_json(msg=str(errex))


if __name__ == "__main__":
    main()

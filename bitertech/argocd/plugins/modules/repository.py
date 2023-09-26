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
        "type": {"required": True, "type": 'str'},
        "repository_url": {"required": True, "type": 'str'},
        "username": {"required": True, "type": 'str'},
        "password": {"required": True, "type": 'str'},
        "project": {"required": False, "type": "str"},
        "name": {"required": False, "type": "str"},
        "status": {"type": "str", "choices": ["present", "absent"], "default": "present"}
    }

    module = AnsibleModule(
        argument_spec=fields
    )

    api_url = module.params["api_url"]
    token = module.params["token"]
    type = module.params["type"]
    repository_url = module.params["repository_url"]
    username = module.params["username"]
    password = module.params["password"]
    project = module.params["project"]
    name = module.params["name"]
    status = module.params["status"]

    try:
        client = ArgoCDClient(api_url, token)
        if status == "present":
            result = client.create_repository(
                type,
                repository_url,
                username,
                password,
                project,
                name
            )

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

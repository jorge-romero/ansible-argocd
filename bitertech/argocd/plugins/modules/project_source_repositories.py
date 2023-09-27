#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


import requests

from ansible.module_utils.basic import AnsibleModule

# Correct the import statement
from ansible_collections.bitertech.argocd.plugins.module_utils.argocd_api import ArgoCDClient


def main():

    fields = {
        "api_url": {"required": True, "type": 'str'},
        "token": {"required": True, "type": 'str'},
        "project_name": {"required": True, "type": 'str'},
        "repositories": {"required": True, "type": 'list'},
        "status": {"type": "str", "choices": ["present", "absent"], "default": "present"},

    }

    module = AnsibleModule(
        argument_spec=fields
    )

    api_url = module.params["api_url"]
    token = module.params["token"]
    project_name = module.params["project_name"]
    repositories = module.params["repositories"]
    status = module.params["status"]

    try:
        client = ArgoCDClient(api_url, token)

        result = client.add_remove_repositories_from_project(
            project_name, repositories, status)

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

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
        "server": {"required": True, "type": 'str'},
        "name": {"required": True, "type": 'str'},
        "namespace": {"required": True, "type": 'str'},
        "status": {"type": "str", "choices": ["present", "absent"], "default": "present"},

    }

    module = AnsibleModule(
        argument_spec=fields
    )

    api_url = module.params["api_url"]
    token = module.params["token"]
    project_name = module.params["project_name"]
    server = module.params["server"]
    name = module.params["name"]
    namespace = module.params["namespace"]
    status = module.params["status"]

    try:
        client = ArgoCDClient(api_url, token)

        if status == "present":
            result = client.add_destination_to_project(
                project_name, server, name, namespace)
        if status == "absent":
            result = client.remove_destination_from_project(
                project_name, server, name, namespace)
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

#!/usr/bin/python
# -*- coding: utf-8 -*-
import json

import requests


class ArgoCDClient:

    def __init__(self, argo_api_url, api_token):
        self.argo_api_url = argo_api_url
        # Headers for the API request
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json",
        }

    def create_application(self,
                           name,
                           repository_url,
                           path,
                           target_revision,
                           values_files=None,
                           destination_server="https://kubernetes.default.svc",
                           namespace="default",
                           project="default"):
        # Define the application spec
        application_spec = {
            "metadata": {
                "name": name,
            },
            "spec": {
                "project": project,
                "source": {
                    "repoURL": repository_url,
                    "path": path,
                    "targetRevision": target_revision,
                    "helm": {
                        "valueFiles": [values_files]
                    }
                },
                "destination": {
                    "server": destination_server,
                    "namespace": namespace,
                },
                "syncPolicy": {
                    "automated": {
                        "selfHeal": True,
                        "prune": True
                    }
                },
            },
        }

        # Create the application
        response = requests.post(f"{self.argo_api_url}/applications",
                                 headers=self.headers,
                                 data=json.dumps(application_spec),
                                 timeout=10000)

        response.raise_for_status()
        return response.json()

    def create_project(self, name, description):
        # Define the project spec
        project_spec = {
            "project": {
                "metadata": {
                    "name": name,
                    "description": description
                }
            }
        }

        # Create the project
        response = requests.post(f"{self.argo_api_url}/projects",
                                 headers=self.headers,
                                 data=json.dumps(project_spec),
                                 timeout=10000)

        response.raise_for_status()
        return response.json()

    def get_project(self, name):
        response = requests.get(f"{self.argo_api_url}/projects/{name}",
                                headers=self.headers,
                                timeout=10000)

        response.raise_for_status()
        return response.json()

    def add_role_to_project(self, project_name, role_name, role_description):
        # Step 1: Get the project data
        project_data = requests.get(f"{self.argo_api_url}/projects/{project_name}",
                                    headers=self.headers,
                                    timeout=10000)

        project_data.raise_for_status()

        # Step 2: Parse the JSON response
        project_json = project_data.json()

        # Step 3: Add the new role data to the "roles" section
        new_role = {
            "name": role_name,
            "description": role_description,
        }
        if "spec" not in project_json:
            project_json["spec"] = {}
        if "roles" not in project_json["spec"]:
            project_json["spec"]["roles"] = []

        for role in project_json["spec"]["roles"]:
            if role.get("name") == role_name:
                return project_data.json()

        project_json["spec"]["roles"].append(new_role)

        # Step 4: Update the project with the modified data
        updated_project_data = requests.put(
            f"{self.argo_api_url}/projects/{project_name}",
            headers=self.headers,
            data=json.dumps({"project": project_json}),
            timeout=10000
        )

        updated_project_data.raise_for_status()
        return updated_project_data.json(), None

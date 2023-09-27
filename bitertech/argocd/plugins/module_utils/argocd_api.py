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
                                 timeout=30)

        response.raise_for_status()
        return response.json()

    def create_project(self, project_name, description):
        # Step 1: Get the project data
        project_data = requests.get(f"{self.argo_api_url}/projects/{project_name}",
                                    headers=self.headers,
                                    timeout=30)

        if project_data.status_code == 200:
            return project_data.json(), None

        # Define the project spec
        project_spec = {
            "project": {
                "metadata": {
                    "name": project_name,
                    "description": description
                }
            }
        }

        # Create the project
        response = requests.post(f"{self.argo_api_url}/projects",
                                 headers=self.headers,
                                 data=json.dumps(project_spec),
                                 timeout=30)

        response.raise_for_status()

        return response.json(), None

    def update_project(self, project_name, description):
        # Step 1: Get the project data
        project_data = requests.get(f"{self.argo_api_url}/projects/{project_name}",
                                    headers=self.headers,
                                    timeout=30)

        project_data.raise_for_status()

        # Step 2: Parse the JSON response
        project_json = project_data.json()

        project_json["metadata"]["name"] = project_name
        project_json["metadata"]["description"] = description

        # Create the project
        response = requests.put(f"{self.argo_api_url}/projects/{project_name}",
                                headers=self.headers,
                                data=json.dumps({"project": project_json}),
                                timeout=30)

        response.raise_for_status()
        return response.json()

    # To be implemented
    def delete_project(self, name):
        return {}, None

    def get_project(self, name):
        response = requests.get(f"{self.argo_api_url}/projects/{name}",
                                headers=self.headers,
                                timeout=30)

        response.raise_for_status()
        return response.json()

    def add_role_to_project(self, project_name, role_name, role_description):
        # Step 1: Get the project data
        project_data = requests.get(f"{self.argo_api_url}/projects/{project_name}",
                                    headers=self.headers,
                                    timeout=30)

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
            timeout=30
        )

        updated_project_data.raise_for_status()
        return updated_project_data.json(), None

    def remove_role_from_project(self, project_name, role_name):
        # To be implemented
        return {}, None

    def add_remove_policies_to_role(self, project_name, role_name, policies, status):
        # Step 1: Get the project data
        project_data = requests.get(f"{self.argo_api_url}/projects/{project_name}",
                                    headers=self.headers,
                                    timeout=30)

        project_data.raise_for_status()

        # Step 2: Parse the JSON response
        project_json = project_data.json()

        # Step 3: Add the new role data to the "roles" section
        roles = project_json.get("spec", {}).get("roles", [])

        target_role = None
        for role in roles:
            if role["name"] == role_name:
                target_role = role
                break

        if target_role is None:
            return {"error": "Role '{role_name}' not found in project"}, None

        if "policies" not in target_role:
            target_role["policies"] = []

        if status == "present":
            for policy in policies:
                if policy not in target_role["policies"]:
                    target_role["policies"].append(policy)

        if status == "absent":
            for policy in policies:
                if policy in target_role["policies"]:
                    target_role["policies"].remove(policy)

        # Step 4: Update the project with the modified data
        updated_project_data = requests.put(
            f"{self.argo_api_url}/projects/{project_name}",
            headers=self.headers,
            data=json.dumps({"project": project_json}),
            timeout=30
        )

        updated_project_data.raise_for_status()
        return updated_project_data.json(), None

    def add_remove_groups_to_role(self, project_name, role_name, groups, status):
        # Step 1: Get the project data
        project_data = requests.get(f"{self.argo_api_url}/projects/{project_name}",
                                    headers=self.headers,
                                    timeout=30)

        project_data.raise_for_status()

        # Step 2: Parse the JSON response
        project_json = project_data.json()

        # Step 3: Add the new role data to the "roles" section
        roles = project_json.get("spec", {}).get("roles", [])

        target_role = None
        for role in roles:
            if role["name"] == role_name:
                target_role = role
                break

        if target_role is None:
            return {"error": "Role '{role_name}' not found in project"}, None

        if "groups" not in target_role:
            target_role["groups"] = []

        if status == "present":
            for group in groups:
                if group not in target_role["groups"]:
                    target_role["groups"].append(group)

        if status == "absent":
            for group in groups:
                if group in target_role["groups"]:
                    target_role["groups"].remove(group)

        # Step 4: Update the project with the modified data
        updated_project_data = requests.put(
            f"{self.argo_api_url}/projects/{project_name}",
            headers=self.headers,
            data=json.dumps({"project": project_json}),
            timeout=30
        )

        updated_project_data.raise_for_status()
        return updated_project_data.json(), None

    def create_repository(self,
                          type,
                          repository_url,
                          username,
                          password,
                          project,
                          name):

        repositories = requests.get(f"{self.argo_api_url}/repositories",
                                    headers=self.headers,
                                    timeout=30)

        repositories.raise_for_status()

        repositories_json = repositories.json()

        if repositories_json["items"] is not None:
            for repository in repositories_json["items"]:
                if repository["repo"] == repository_url:
                    return {"error": f"Repository {repository_url} already exists."}, None

        # Define the repository spec
        repository_spec = {
            "type": type,
            "repo": repository_url,
            "username": username,
            "password": password
        }
        if project is not None:
            repository_spec["project"] = project
        if type == "helm":
            repository_spec["name"] = name

        response = requests.post(f"{self.argo_api_url}/repositories",
                                 headers=self.headers,
                                 data=json.dumps(repository_spec),
                                 timeout=30)

        response.raise_for_status()

        return response.json(), None

    def add_destination_to_project(self, project_name, server, name, namespace):
        # Step 1: Get the project data
        project_data = requests.get(f"{self.argo_api_url}/projects/{project_name}",
                                    headers=self.headers,
                                    timeout=30)

        project_data.raise_for_status()

        # Step 2: Parse the JSON response
        project_json = project_data.json()

        # Step 3: Add the new role data to the "roles" section
        new_destination = {
            "server": server,
            "name": name,
            "namespace": namespace,
        }
        if "spec" not in project_json:
            project_json["spec"] = {}
        if "destinations" not in project_json["spec"]:
            project_json["spec"]["destinations"] = []

        for destination in project_json["spec"]["destinations"]:
            if destination.get("server") == server and destination.get("name") == name and destination.get("namespace") == namespace:
                return project_data.json()

        project_json["spec"]["destinations"].append(new_destination)

        # Step 4: Update the project with the modified data
        updated_project_data = requests.put(
            f"{self.argo_api_url}/projects/{project_name}",
            headers=self.headers,
            data=json.dumps({"project": project_json}),
            timeout=30
        )

        updated_project_data.raise_for_status()
        return updated_project_data.json(), None

    def remove_destination_from_project(self, project_name, server, name, namespace):
        # Step 1: Get the project data
        project_data = requests.get(f"{self.argo_api_url}/projects/{project_name}",
                                    headers=self.headers,
                                    timeout=30)

        project_data.raise_for_status()

        # Step 2: Parse the JSON response
        project_json = project_data.json()

        if "spec" not in project_json:
            return project_data.json(), None

        if "destinations" not in project_json["spec"]:
            return project_data.json(), None

        # Step 3: Remove the destination
        new_destination = {
            "server": server,
            "name": name,
            "namespace": namespace,
        }

        project_json["spec"]["destinations"].remove(new_destination)

        # Step 4: Update the project with the modified data
        updated_project_data = requests.put(
            f"{self.argo_api_url}/projects/{project_name}",
            headers=self.headers,
            data=json.dumps({"project": project_json}),
            timeout=30
        )

        updated_project_data.raise_for_status()
        return updated_project_data.json(), None

    def add_remove_repositories_from_project(self, project_name, repositories, status):
        # Step 1: Get the project data
        project_data = requests.get(f"{self.argo_api_url}/projects/{project_name}",
                                    headers=self.headers,
                                    timeout=30)

        project_data.raise_for_status()

        # Step 2: Parse the JSON response
        project_json = project_data.json()

        # Step 3: Add/Remove the new repositories data to the "repositories" section
        project_repositories = project_json.get(
            "spec", {}).get("sourceRepos", [])

        if status == "present":
            for repository in repositories:
                if repository not in project_repositories:
                    project_repositories.append(repository)

        if status == "absent":
            for repository in repositories:
                if repository in project_repositories:
                    project_repositories.remove(repository)

        # Step 4: Update the project with the modified data
        updated_project_data = requests.put(
            f"{self.argo_api_url}/projects/{project_name}",
            headers=self.headers,
            data=json.dumps({"project": project_json}),
            timeout=30
        )

        updated_project_data.raise_for_status()
        return updated_project_data.json(), None

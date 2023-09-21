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

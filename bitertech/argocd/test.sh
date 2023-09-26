#!/bin/sh
ansible-galaxy collection build --force
ansible-galaxy collection install bitertech-argocd-0.0.1.tar.gz -p /workspaces/test/playbook/collections --force

cp samples/* /workspaces/test/playbook/
#!/usr/bin/python3

#script copied from Stefan
import requests
import json
import sys
import argparse
import os

PROJECTS_URL='http://gns3.hepiapp.ch/v2/projects'
config_path = os.path.expanduser('~/.ssh/config.d/')
os.makedirs(os.path.dirname(config_path), exist_ok=True)


def usage():
    print(f"{sys.argv[0]} PROJECT_NAME")

def get_project_uuid(project_name):
    r = requests.get(PROJECTS_URL)
    projects = r.json()
    for project in projects:
        if project['name'] == project_name:
            return project['project_id']
    return None

def get_project_nodes(project_uuid):
    """
    Get the nodes for a project. Return a array of nodes with their host ip and port.
    """
    r = requests.get(PROJECTS_URL+'/'+project_uuid+'/nodes')
    nodes = r.json()
    nodes_info = []
    for node in nodes:
        nodes_info.append({
            'name': node['name'],
            'host': node['console_host'],
            'port': node['console'] + 1
        })
    return nodes_info


def create_ssh_config_file(nodes):
    output = ""
    for node in nodes:
        output += f"Host {node['name']}\n"
        output += f"  HostName {node['host']}\n"
        output += f"  Port {node['port']}\n"
        output += f"  User root\n"
        output += f"  StrictHostKeyChecking no\n"
        output += f"  UserKnownHostsFile /dev/null\n"
        output += f"  IdentityFile ~/.ssh/gns3.rsa\n"
        output += "\n"
    return output
       

def main():
    parser = argparse.ArgumentParser(description='Connect to GNS3 nodes')
    parser.add_argument('project_name', help='The name of the GNS3 project')
    args = parser.parse_args()
    project_name = args.project_name
    project_uuid = get_project_uuid(project_name)
    print(project_uuid)
    if project_uuid is None:
        print(f"Project {project_name} not found")
        usage()
        sys.exit(1)
    nodes = get_project_nodes(project_uuid)
    print(nodes)
    ssh_config = create_ssh_config_file(nodes)
    print(ssh_config)
    # ask to continue, if yes write to ~/.ssh/config.d/{project_name}
    if input("Do you want to continue? (y/n): ") != 'y':
        sys.exit(0)
    with open(config_path + project_name, 'w') as f:
        f.write(ssh_config)

if __name__ == '__main__':
    main()

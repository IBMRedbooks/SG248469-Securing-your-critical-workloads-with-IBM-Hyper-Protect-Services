from dbaasapi import *
from variables import *

# DBaaSManager object containing wrapped api endpoints
dbaas_manager = DBaaSManager(
    dbaas_manager_ip=dbaas_manager_ip,
    port=port,
    api_key=api_key,
    accept_license=True,
    ssl_verify=path_to_cert
)

# Initializing a GET request on the /clusters/{cluster_id} API endpoint
response = dbaas_manager.cluster_show(cluster_id=cluster_guid)
print(response.json())

# List all users on a cluster
response = dbaas_manager.user_list(cluster_id=cluster_guid)
print(response.json())

# List all information about a specific user
response = dbaas_manager.user_show(cluster_id=cluster_guid, user_id="admin.admin")
print(response.json())

# List out all users with their full details
cluster_users = dbaas_manager.user_list(cluster_id=cluster_guid).json()['users']
all_users_with_details = []
for user in cluster_users:
    response = dbaas_manager.user_show(
        cluster_id=cluster_guid,
        user_id=f"{user['auth_db']}.{user['name']}"
    )
    all_users_with_details.append(response.json())
print(all_users_with_details)

# List out all clusters and their IDs for an account
response = dbaas_manager.service_list()
all_services = dbaas_manager.service_list().json()['services']
for service in all_services:
    print(f"{service['service']['name']}: {service['cluster_id']}")

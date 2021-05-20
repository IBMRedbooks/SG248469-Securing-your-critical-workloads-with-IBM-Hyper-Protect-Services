"""
This class manages supported DBaaS REST API calls.
"""
from dbaasapi.session import Session


class DBaaSManager(Session):
    """
    CLUSTER
    """
    def cluster_show(self, cluster_id):
        """ GET /clusters/{cluster_id}
        Function to get the info on a single cluster.
        :param cluster_id: The ID of a cluster to get info on
        :return: requests.Response
        """
        url = "{}/clusters/{}".format(self.dbaas_api_endpoint, cluster_id)
        return self._get(url)

    """
    CLUSTER: USERS
    """
    def user_list(self, cluster_id):
        """ GET /clusters/{cluster_id}/users
        List all the users in the specified database cluster.
        :param cluster_id: The ID of a cluster
        :return: requests.Response
        """
        url = "{}/clusters/{}/users".format(self.dbaas_api_endpoint, cluster_id)
        return self._get(url)

    def user_show(self, cluster_id, user_id):
        """ GET /clusters/{cluster_id}/users/{db_user_id}
        Get a user's information from a database cluster.
        :param cluster_id: The ID of the cluster with the user
        :param user_id: The ID of the db user in the format: auth_db.name i.e. admin.admin
        :return: requests.Response
        """
        url = "{}/clusters/{}/users/{}".format(self.dbaas_api_endpoint, cluster_id, user_id)
        return self._get(url)

    """
    SERVICES
    """
    def service_list(self):
        """ GET /services
        Query one or more IBM Cloud service instance of Hyperprotect DBaaS on the server indicated by the URL.
        :return: requests.Response
        """
        url = "{}/services".format(self.dbaas_api_endpoint)
        return self._get(url)

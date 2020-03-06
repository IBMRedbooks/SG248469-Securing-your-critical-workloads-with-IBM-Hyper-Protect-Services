"""
This class manages HTTP sessions to DBaaS REST API service.
"""
import requests
import logging


class Session:
    def __init__(self, dbaas_manager_ip, port, api_key, accept_license=True, ssl_verify=False):
        """ Init the Session Class with connection to a DBaaS DBaaSManager

        :param dbaas_manager_ip: The IP of the DBaaS Manager
        :param port: The port that the DBaaS DBaaS Manager listens on
        :param api_key: IBM Cloud account API key
        :param accept_license: Boolean True or False for accepting the IBM Cloud license agreement
        :param ssl_verify: Path to CA cert file to use SSL
        """
        # set logging
        self._log = logging.getLogger(__name__)

        if api_key is None:
            raise Exception("Need an API key for authentication.")

        self.session = requests.Session()
        self._ssl_verify = ssl_verify
        self.session.verify = self._ssl_verify
        self.ip = dbaas_manager_ip
        self.port = port
        self.accept_license = accept_license
        self.api_key = api_key
        self.token = None
        self.user_id = None
        self.dbaas_api_endpoint = None

        self._set_token()
        self._set_user_id()
        self._set_headers()
        self._set_api_endpoint()

    def _set_token(self):
        """ Method that initializes the class token variable """
        token_response = self._get_token()
        self.token = token_response.json()

    def _get_token(self):
        """ GET /auth/token

        :return: requests.Response object
        """
        headers = {
            'accept': 'application/json',
            'api_key': self.api_key
        }
        url = "https://{}:{}/api/v1/auth/token".format(self.ip, self.port)
        self._log.debug("GET /auth/token url: {}".format(url))
        token_response = requests.get(url, headers=headers, verify=self._ssl_verify)

        if token_response.status_code != 200:
            self._log.error("Token request failed: {}  {}".format(token_response.status_code, token_response.json()))
            raise Exception("Token request failed", token_response.status_code, token_response.json())
        return token_response

    def _set_user_id(self):
        """ Initialize the class user_id by pulling the corresponding user_id from self.token """
        self.user_id = self.token['user_id']  # pull corresponding user_id from token response

    def _set_api_endpoint(self):
        """ Set DBaaS API endpoint """
        self.dbaas_api_endpoint = "https://{}:{}/api/v1/{}".format(self.ip, self.port, self.user_id)
        self._log.debug("DBaaS API endpoint updated: {}".format(self.dbaas_api_endpoint))

    def _set_headers(self):
        """ Set https session headers """
        accept_license = 'yes' if self.accept_license else 'no'
        self.session.headers = {
            'accept': 'application/json',
            'content-type': 'application/json',
            'x-auth-token': self.token['access_token'],
            'accept-license-agreement': accept_license
        }
        self._log.debug("Session headers updated: {}".format(self.session.headers))

    def _get(self, url):
        """ Method for submitting a http get request

        :param url: Endpoint url for the request
        :return: requests.Response object
        """
        try:
            response = self.session.get(url)
            return response
        except requests.exceptions.RequestException as e:
            self._log.debug("Unknown exception:\n{}".format(e))
            raise e
        finally:
            self._log.debug("_get() - completed")

    def _post(self, url, body):
        """ Method for submitting a http post request

        :param url: Endpoint url for the request
        :param body:
        :return: requests.Response object
        """
        try:
            response = self.session.post(url, json=body)
            return response
        except requests.exceptions.RequestException as e:
            self._log.debug("Unknown exception:\n{}".format(e))
            raise e
        finally:
            self._log.debug("_post() - completed")

    def _delete(self, url):
        """ Method for submitting a http delete request

        :param url: Endpoint url for the request
        :return: requests.Response object
        """
        try:
            response = self.session.delete(url)
            return response
        except requests.exceptions.RequestException as e:
            self._log.debug("Unknown exception:\n{}".format(e))
            raise e
        finally:
            self._log.debug("_delete() - completed")

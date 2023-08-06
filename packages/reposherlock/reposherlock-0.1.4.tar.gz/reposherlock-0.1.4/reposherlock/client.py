import json
import requests
import time

from bs4 import BeautifulSoup
# Because python versions are apparently a nightmare.
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode


class APIClient:
    """ This class provides a generic endpoint client to be used for REST API queries.
    """

    def __init__(self, credentials, header_auth=False, headers=None):
        """Constructor method

        :param credentials: A python dict containing a username and token
        :type credentials: dict
        :param header_auth: A flag that indicates whether authentication is included in the header or not, defaults to False
        :type header_auth: bool, optional
        :param headers: A python dict containing necessary headers for the requests
        :type headers: dict, optional
        """

        # Get and check credentials
        self.credentials = credentials
        if not isinstance(self.credentials, dict):
            raise TypeError("Expected JSON map, got something different!")
        if 'user' not in self.credentials.keys():
            raise ValueError('"user" entry not found in authentication file!')
        if 'token' not in self.credentials.keys():
            raise ValueError('"token" entry not found in authentication file!')

        # This flags whether authentication info is transmitted in the header or body
        self.header_auth = header_auth

        # Because this is a generic client, we have to trust the user.
        self.headers = headers

    def query_endpoint(self, endpoint, method='GET', parameters=None):
        """Returns the query sent to a specific endpoint using the specified parameters.

        :param endpoint: The fully qualified URI of the endpoint without parameters
        :type endpoint: str
        :param method: The method via which the request is sent, defaults to "GET"
        :type method: str
        :param parameters: A python dict containing the endpoint's parameters
        :type parameters: dict
        :return: A python dict containing the endpoint's response to the provided query
        :rtype: dict
        """
        full_uri = "%s?%s" % (endpoint, urlencode(parameters))
        if self.header_auth:
            raw_result = requests.request(
                method, full_uri,
                headers=self.headers)
        else:
            raw_result = requests.request(
                method, full_uri,
                auth=(self.credentials['user'], self.credentials['token']),
                headers=self.headers)
        result_content = raw_result.content.decode('utf-8')
        if result_content is not None and not result_content == '':
            result = json.loads(result_content)
        else:
            result = json.loads('{"message": "No result returned"}')
        time.sleep(1)
        return result


class WEBClient:
    """ This class provides a generic endpoint client to be used for HTML
    webpage retrieval.
    """

    def __init__(self):
        pass

    @staticmethod
    def retrieve_page(endpoint):
        """Retrieves the endpoint.

        Keyword arguments:
        endpoint -- The fully qualified URI of the endpoint, no parameters.
        """
        with requests.request('GET', url=endpoint) as result_raw:
            soup = BeautifulSoup(result_raw.text.encode("utf8"), 'html.parser')
        time.sleep(2)
        return soup

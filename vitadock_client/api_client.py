import json

from oauthlib.oauth1.rfc5849 import SIGNATURE_HMAC_SHA256
import requests
from requests_oauthlib.oauth1_auth import OAuth1
from vitadock_client import measurements

__author__ = 'Michal'

API_ENDPOINT = "https://cloud.vitadock.com"
API_ENDPOINT_TEST = "https://test-cloud.vitadock.com"

MODULE_CARDIODOCKS = "cardiodocks"

MODULE_CLASSES = {
    MODULE_CARDIODOCKS: measurements.CardiodocksMeasurement,
}


class VitadockError(Exception):
    def __init__(self, response):
        super(VitadockError, self).__init__(str(response.status_code))
        self.status_code = response.status_code
        self.response = response


class VitadockClient:
    headers = {
        'Accept': 'application/json',
    }

    def __init__(self, app_key, app_secret, access_token, access_secret, test=False):
        self.endpoint = API_ENDPOINT_TEST if test else API_ENDPOINT

        self.client = requests.Session()
        self.client.auth = OAuth1(
            app_key,
            app_secret,
            access_token,
            access_secret,
            signature_method=SIGNATURE_HMAC_SHA256
        )

    def get(self, module_name, **get_params):
        """
        Make a GET request to a module in Vitadock
        :param module_name: the module name as per documentation
        :param get_params: GET parameters to be appended to the requested url
        :return: Response object representing the response from server
        """
        url = "{}/data/{}".format(self.endpoint, module_name)
        return self.client.get(url, params=get_params, headers=self.headers)

    def get_json(self, module_name, **get_params):
        get = dict(start=0, max=100, date_since=0)
        get.update(get_params)
        response = self.get(module_name, **get)
        if not response.ok:
            raise VitadockError(response)
        return json.loads(response.content)

    def get_measurements(self, module, **get_params):
        """
        Fetches measurements from the selected module in Vitadock and returns them in a list of measurement objects
        :param module: the module name
        :param get_params: GET parameters for the request
        :return: list
        """
        if module not in MODULE_CLASSES:
            raise KeyError(u'Unknown Vitadock module: {}. Supported modules: {}'.format(module, ', '.join(MODULE_CLASSES.keys())))
        cls = MODULE_CLASSES[module]
        data = self.get_json(module, **get_params)
        return [cls(**values) for values in data]

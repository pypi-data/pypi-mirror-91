import os
import sys

import requests
import string

from geodesic.oauth import AuthManager

HOST = 'https://geodesic.seerai.space/'
API_VERSION = 1

client = None

def get_client():
    global client
    if client is not None:
        return client
    
    client = Client()
    return client


class Client:
    def __init__(self):
        self._auth = AuthManager()
        self._session = None
        self._host = HOST
        self._api_version = API_VERSION

    def request(self, uri, method='GET', **params):
        url = HOST
        if url.endswith("/"):
            url = url[:-1] + uri
        if uri.startswith("http"):
            url = uri

        if method == 'GET':
            req = requests.Request("GET", url, params=params)
        elif method == 'POST':
            req = requests.Request("POST", url, json=params)
        req.headers['Authorization'] = "Bearer {0}".format(self._auth.id_token)

        if self._session is None:
            self._session = requests.Session()

        prepped = req.prepare()
        res = self._session.send(prepped)

        try:
            res = res.json()
            if 'error' in res:
                raise Exception("an error occurred: {0}".format(res['error']))
            return res
        except Exception as e:
            if not isinstance(res, dict):
                print("response: {0}".format(res.text))
            raise Exception("an error occured: {0}".format(e))

    def get(self, uri, **query):
        return self.request(uri, method="GET", **query)

    def post(self, uri, **body):
        return self.request(uri, method="POST", **body)




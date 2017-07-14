import json
import urllib.request
import urllib.parse
import urllib.error

# private query nonce
import time

# private query signing
import hashlib
import hmac
import base64

from . import connection


class API(object):
    def __init__(self, key='', secret='', conn=None):
        self.key = key
        self.secret = secret
        self.uri = 'https://api.kraken.com'
        self.apiversion = '0'
        self.conn = conn
        return

    def load_key(self, path):
        with open(path, 'r') as f:
            self.key = f.readline().strip()
            self.secret = f.readline().strip()
        return

    def _query(self, urlpath, req, conn=None, headers=None):
        url = self.uri + urlpath

        if conn is None:
            if self.conn is None:
                self.conn = connection.Connection()
            conn = self.conn

        if headers is None:
            headers = {}

        ret = conn._request(url, req, headers)
        return json.loads(ret)

    def query_public(self, method, req=None, conn=None):
        urlpath = '/' + self.apiversion + '/public/' + method

        if req is None:
            req = {}

        return self._query(urlpath, req, conn)

    def query_private(self, method, req=None, conn=None):
        if req is None:
            req = {}

        urlpath = '/' + self.apiversion + '/private/' + method

        req['nonce'] = int(1000*time.time())
        postdata = urllib.parse.urlencode(req)

        # Encoded before hashing
        encoded = (str(req['nonce']) + postdata).encode()
        message = urlpath.encode() + hashlib.sha256(encoded).digest()

        signature = hmac.new(base64.b64decode(self.secret),
                             message, hashlib.sha512)
        sigdigest = base64.b64encode(signature.digest())

        headers = {
            'API-Key': self.key,
            'API-Sign': sigdigest.decode()
        }

        return self._query(urlpath, req, conn, headers)

#!/usr/bin/env python3

import json

from http.client import HTTPSConnection
from base64 import b64encode


class ApiConnector:
    def __init__(self, protocol, host_url, username=None, password=None, headers=None):
        self.protocol = protocol
        self.host_url = host_url

        self.common_headers = {**headers} if headers != None else {}

        if username != None and password != None:
            credentials = "%s:%s" % (username, password)
            basic_auth_token = b64encode(
                credentials.encode("ascii")).decode("ascii")
            self.common_headers["Authorization"]: "Basic %s" % basic_auth_token

    def open_connection(self):
        self.connection = HTTPSConnection(self.host_url)
        return self

    def merge_headers(self, extra):
        return {**self.common_headers, **extra}

    def request(self, method, path=None, params={}):
        # self.open_connection()
        request_url = "%s://%s" % (self.protocol, self.host_url)

        if path != None:
            request_url += "/%s" % path

        headers = self.merge_headers(
            params["headers"]) if "headers" in params else self.common_headers
        body = json.dumps(params["body"]) if "body" in params else None

        self.connection.request(method, request_url, headers=headers, body=body)
        response = self.connection.getresponse()
        # self.close_connection()
        return self.handle_response(response.status, response.read())

    def handle_response(self, status, body):
        if status in [200, 204]:
            try:
                parsed = json.loads(body)
            except ValueError:
                parsed = body.decode("utf-8")
        else:
            try:
                parsed = json.loads(body)

                if "errorCode" in parsed:
                    parsed = "%d %s" % (
                        parsed["errorCode"], parsed["errorMessage"])
            except ValueError:
                parsed = body.decode("utf-8")

        return {
            "status": status,
            "body": parsed
        }

    def __str__(self):
        return "*ApiConnector*\nhost URL: %s\ncommon headers: %s" % (self.host_url, str(self.common_headers))

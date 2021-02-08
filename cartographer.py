#!/usr/bin/env python3

import json

import requests


class Cartographer:
    HTTP_OPTIONS = "OPTIONS"
    HTTP_HEAD = "HEAD"
    HTTP_GET = "GET"
    HTTP_POST = "POST"
    HTTP_PUT = "PUT"
    HTTP_PATCH = "PATCH"
    HTTP_DELETE = "DELETE"

    def __init__(self, config):
        (host_url, nodes, auth, headers) = self._parse_configs(config)

        self.host_url = host_url
        self.nodes = nodes

        self.auth = None
        if auth:
            self.set_authentication(**auth)

        self.common_headers = {}
        if headers:
            self.add_common_headers(headers)

    def _parse_configs(self, raw_config):
        config = json.loads(raw_config)

        connection = config.get("connection", None)
        nodes = config.get("nodes", None)

        if not connection or not nodes:
            raise ConfigError(
                "Config file is missing connection and node data")

        if not "hostUrl" in connection:
            raise ConfigError("Config file is missing host URL")

        host_url = "{0}://{1}".format(connection.get("protocol",
                                                     "https"), connection.get("hostUrl", ""))

        auth = None
        if "auth" in connection:
            auth = connection["auth"]
        # shortcut for v0.1 -> v0.2 backcompatibility
        elif "username" in connection and "password" in connection:
            auth = {
                "type": "basic",
                "username": connection["username"],
                "password": connection["password"]
            }

        node_list = {name: ApiNode(name, entry)
                     for name, entry in nodes.items()}

        headers = connection.get("headers", None)
        return (host_url, node_list, auth, headers)

    def set_authentication(self, **kwargs):
        # since basic auth is ubiquitous, if the type is missing just assume it by default 
        auth_type = kwargs.get("type", "basic").lower()

        if auth_type == "basic":
            self.auth = (kwargs.get("username", ""),
                         kwargs.get("password", ""))
        # TODO: add other types later
    
    def add_common_headers(self, headers):
        self.common_headers = {**self.common_headers, **headers}

    def has_node(self, node_name):
        return node_name in self.nodes

    def call(self, method, node_name, *args, **kwargs):
        if self.nodes == None:
            raise UndefinedNodeMapError("Nodemap has not been set")
        elif not self.has_node(node_name):
            raise NodeNotFoundError(
                "Node: '{0}' not found".format(node_name))

        node = self.nodes[node_name]

        path_url = node.resolve_url(*args)

        request_url = self.host_url

        if path_url and path_url != "":
            request_url += "/{0}".format(path_url)

        headers = None
        if "headers" in kwargs:
            headers = {**self.common_headers, **kwargs["headers"]}
        else:
            headers = self.common_headers

        body = json.dumps(kwargs["body"]) if "body" in kwargs else None

        query_params = kwargs["query"] if "query" in kwargs else None

        actions = {
            Cartographer.HTTP_OPTIONS: requests.options,
            Cartographer.HTTP_HEAD: requests.head,
            Cartographer.HTTP_GET: requests.get,
            Cartographer.HTTP_POST: requests.post,
            Cartographer.HTTP_PUT: requests.put,
            Cartographer.HTTP_PATCH: requests.patch,
            Cartographer.HTTP_DELETE: requests.delete
        }
        action = actions[method]

        if "debug_mode" in kwargs and (kwargs.get("debug_mode", False) == True):
            message = "About to send {0} request to {1}".format(
                method, request_url)
            if headers:
                message += "\n--- with headers: {0}".format(headers)
            if body:
                message += "\n--- with body: {0}".format(body)
            print(message)

        response = action(
            request_url, auth=self.auth, headers=headers, params=query_params, json=body)

        return response

    def options(self, node_name, *args, **kwargs):
        return self.call(Cartographer.HTTP_OPTIONS, node_name, *args, **kwargs)

    def head(self, node_name, *args, **kwargs):
        return self.call(Cartographer.HTTP_HEAD, node_name, *args, **kwargs)

    def get(self, node_name, *args, **kwargs):
        return self.call(Cartographer.HTTP_GET, node_name, *args, **kwargs)

    def post(self, node_name, *args, **kwargs):
        return self.call(Cartographer.HTTP_POST, node_name, *args, **kwargs)

    def put(self, node_name, *args, **kwargs):
        return self.call(Cartographer.HTTP_PUT, node_name, *args, **kwargs)

    def patch(self, node_name, *args, **kwargs):
        return self.call(Cartographer.HTTP_PATCH, node_name, *args, **kwargs)

    def delete(self, node_name, *args, **kwargs):
        return self.call(Cartographer.HTTP_DELETE, node_name, *args, **kwargs)

    def __str__(self):
        return "Cartographer instance details:\n" + str(self.connector) + "\nNodes: " + str([str(node) for node in self.nodes])


class ApiNode:
    def __init__(self, name, node_config):
        self.name = name

        # v0.1 -> v0.2 backcompatibility: clean this up after deprecation
        self.root_url = node_config.get(
            "root_url", None) if "root_url" in node_config else node_config.get("queryUrl", None)
        self.variable_url = node_config.get(
            "variable_url", None) if "variable_url" in node_config else node_config.get("nodeUrl", None)

    def query(self):
        return self.query_url

    # v0.1 method shortcut for :id variables. Deprecate?
    def by_id(self, id):
        return self.variable_url.replace(":id", id)

    # The end user is responsible for handling the variable substitutions correctly!
    def resolve_url(self, *args):
        resolved_url = None

        if len(args) == 0:
            resolved_url = self.root_url
        # v0.1 method shortcut for :id variables. Deprecate?
        elif len(args) == 1 and ":id" in self.variable_url:
            resolved_url = self.by_id(args[0])
        else:
            for i, entry in enumerate(args):
                resolved_url = resolved_url.replace("{{0}}".format(i), entry)

        return resolved_url

    def __str__(self):
        return "*ApiNode*:\nqueryUrl: %s\nnodeUrl: %s" % (self.root_url, self.node_url)


class ConfigError(Exception):
    pass


class UndefinedNodeMapError(Exception):
    pass


class NodeNotFoundError(Exception):
    pass

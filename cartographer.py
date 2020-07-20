#!/usr/bin/env python3

from urllib.parse import quote

from .submodules.api_connector import ApiConnector
from .submodules.api_node import ApiNode


def add_query_params(base, params):
    key_value_pairs = ["{0}={1}".format(key, quote(value))
                       for key, value in params.items()]
    query_string = "&".join(key_value_pairs)
    return "{0}?{1}".format(base, query_string)


class Cartographer:
    def __init__(self, config):
        (connector, nodes) = self.parse_configs(config)
        self.connector = connector
        self.nodes = nodes

        self.node_names = [self.nodes.keys()]

    def parse_configs(self, raw_config):
        import json

        config = json.loads(raw_config)

        if not "connection" in config or not "nodes" in config:
            raise Exception("Config file is missing connection and node data")

        connection = config["connection"]
        if not "hostUrl" in connection:
            raise Exception("Connection details has no hostUrl attribute")
        connector = ApiConnector(connection["protocol"], connection["hostUrl"], connection["username"] if "username" in connection else None,
                                 connection["password"] if "password" in connection else None, connection["headers"] if "headers" in connection else None)

        nodes = {name: ApiNode(name, entry)
                 for name, entry in config["nodes"].items()}

        # TODO: parse the rest of the stuff in the config

        return (connector, nodes)

    def set_authentication(self, type, settings={}):
        if type == "basic":
            self.connector.set_basic_authentication(settings.get("username"), settings.get("password"))
        else:
            raise Exception("Unsupported auth type argument in set_authentication '{0}'".format(type))


    def call(self, method, node_name, node_id=None, params={}, debug=False):
        if self.connector == None:
            raise UndefinedConnectorContextError("Connector has not been set")
        elif self.nodes == None:
            raise UndefinedNodeMapError("Nodemap has not been set")
        else:
            if not node_name in self.nodes:
                raise InvalidNodeError(
                    "Invalid node: '{0}' not found".format(node_name))

            node = self.nodes[node_name]
            path_url = node.query() if node_id == None else node.by_id(node_id)

            if not path_url:
                raise UndefinedPathError(
                    "Failed to get a valid path for node '{0}' (check if the %s was configured correctly).\n List of configured nodes: {1}".format(node_name, "nodeUrl" if node_id == None else "queryUrl", str(self.node_names)))

            if "query" in params:
                path_url = add_query_params(path_url, params["query"])
            return self.connector.request(method, path_url, params, debug)

    def options(self, node_name, node_id=None, params={}, debug=False):
        return self.call("OPTIONS", node_name, node_id, params, debug)

    def head(self, node_name, node_id=None, params={}, debug=False):
        return self.call("HEAD", node_name, node_id, params, debug)

    def get(self, node_name, node_id=None, params={}, debug=False):
        return self.call("GET", node_name, node_id, params, debug)

    def post(self, node_name, node_id=None, params={}, debug=False):
        return self.call("POST", node_name, node_id, params, debug)

    def put(self, node_name, node_id=None, params={}, debug=False):
        return self.call("PUT", node_name, node_id, params, debug)

    def patch(self, node_name, node_id=None, params={}, debug=False):
        return self.call("PATCH", node_name, node_id, params, debug)

    def delete(self, node_name, node_id=None, params={}, debug=False):
        return self.call("DELETE", node_name, node_id, params, debug)

    def __str__(self):
        return "Cartographer instance details:\n" + str(self.connector) + "\nNodes: " + str([str(node) for node in self.nodes])


class UndefinedConnectorContextError(Exception):
    pass


class UndefinedNodeMapError(Exception):
    pass


class InvalidNodeError(Exception):
    pass


class UndefinedPathError(Exception):
    pass

#!/usr/bin/env python3

from submodules.api_connector import ApiConnector
from submodules.api_node import ApiNode


def add_query_params(base, params):
    key_value_pairs = ["%s=%s" % (key, value) for key, value in params.items()]
    query_string = "&".join(key_value_pairs)
    return "%s?%s" % (base, query_string)


class Cartographer:
    def __init__(self, config):
        (connector, nodes) = self.parse_configs(config)
        self.connector = connector
        self.nodes = nodes

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

    def call(self, method, node_name, node_id=None, params={}):
        if self.connector == None:
            raise UndefinedConnectorContextError("Connector has not been set")
        elif self.nodes == None:
            raise UndefinedNodeMapError("Nodemap has not been set")
        else:
            if not node_name in self.nodes:
                raise InvalidNodeError(
                    "Invalid node: '%s' not found" % node_name)

            node = self.nodes[node_name]
            path_url = node.query() if node_id == None else node.by_id(node_id)

            if not path_url:
                raise UndefinedPathError(
                    "Failed to get a valid path for node '%s' (check if the %s was configured correctly)" % (node_name, "nodeUrl" if node_id == None else "queryUrl"))

            if "query" in params:
                path_url = add_query_params(path_url, params["query"])
            return self.connector.request(method, path_url, params)

    def options(self, node_name, node_id=None, params={}):
        return self.call("OPTIONS", node_name, node_id, params)

    def head(self, node_name, node_id=None, params={}):
        return self.call("HEAD", node_name, node_id, params)

    def get(self, node_name, node_id=None, params={}):
        return self.call("GET", node_name, node_id, params)

    def post(self, node_name, node_id=None, params={}):
        return self.call("POST", node_name, node_id, params)

    def put(self, node_name, node_id=None, params={}):
        return self.call("PUT", node_name, node_id, params)

    def patch(self, node_name, node_id=None, params={}):
        return self.call("PATCH", node_name, node_id, params)

    def delete(self, node_name, node_id=None, params={}):
        return self.call("DELETE", node_name, node_id, params)

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

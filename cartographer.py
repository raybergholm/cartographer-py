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

        nodes = [ApiNode(name, entry)
                 for name, entry in config["nodes"].items()]

        # TODO: parse the rest of the stuff in the config

        return (connector, nodes)

    def options(self, node_name, node_id=None, params={}):
        if self.connector == None:
            raise UndefinedConnectorContextError("Connector has not been set")
        elif self.nodes == None:
            raise UndefinedNodeMapError("Nodemap has not been set")
        else:
            path_url = self.nodes.query(
                node_name) if node_id == None else self.nodes.by_id(node_name, node_id)
            if "query" in params:
                path_url = add_query_params(path_url, params["query"])
            return self.connector.request("OPTIONS", path_url, params)

    def head(self, node_name, node_id=None, params={}):
        if self.connector == None:
            raise UndefinedConnectorContextError("Connector has not been set")
        elif self.nodes == None:
            raise UndefinedNodeMapError("Nodemap has not been set")
        else:
            path_url = self.nodes.query(
                node_name) if node_id == None else self.nodes.by_id(node_name, node_id)
            if "query" in params:
                path_url = add_query_params(path_url, params["query"])
            return self.connector.request("HEAD", path_url, params)

    def get(self, node_name, node_id=None, params={}):
        if self.connector == None:
            raise UndefinedConnectorContextError("Connector has not been set")
        elif self.nodes == None:
            raise UndefinedNodeMapError("Nodemap has not been set")
        else:
            path_url = self.nodes.query(
                node_name) if node_id == None else self.nodes.by_id(node_name, node_id)
            if "query" in params:
                path_url = add_query_params(path_url, params["query"])
            return self.connector.request("GET", path_url, params)

    def post(self, node_name, node_id=None, params={}):
        if self.connector == None:
            raise UndefinedConnectorContextError("Connector has not been set")
        elif self.nodes == None:
            raise UndefinedNodeMapError("Nodemap has not been set")
        else:
            path_url = self.nodes.query(
                node_name) if node_id == None else self.nodes.by_id(node_name, node_id)
            if "query" in params:
                path_url = add_query_params(path_url, params["query"])
            return self.connector.request("POST", path_url, params)

    def put(self, node_name, node_id=None, params={}):
        if self.connector == None:
            raise UndefinedConnectorContextError("Connector has not been set")
        elif self.nodes == None:
            raise UndefinedNodeMapError("Nodemap has not been set")
        else:
            path_url = self.nodes.query(
                node_name) if node_id == None else self.nodes.by_id(node_name, node_id)
            if "query" in params:
                path_url = add_query_params(path_url, params["query"])
            return self.connector.request("PUT", path_url, params)

    def patch(self, node_name, node_id=None, params={}):
        if self.connector == None:
            raise UndefinedConnectorContextError("Connector has not been set")
        elif self.nodes == None:
            raise UndefinedNodeMapError("Nodemap has not been set")
        else:
            path_url = self.nodes.query(
                node_name) if node_id == None else self.nodes.by_id(node_name, node_id)
            if "query" in params:
                path_url = add_query_params(path_url, params["query"])
            return self.connector.request("PATCH", path_url, params)

    def delete(self, node_name, node_id=None, params={}):
        if self.connector == None:
            raise UndefinedConnectorContextError("Connector has not been set")
        elif self.nodes == None:
            raise UndefinedNodeMapError("Nodemap has not been set")
        else:
            path_url = self.nodes.query(
                node_name) if node_id == None else self.nodes.by_id(node_name, node_id)
            if "query" in params:
                path_url = add_query_params(path_url, params["query"])
            return self.connector.request("DELETE", path_url, params)

    def __str__(self):
        return "Cartographer instance details:\n" + str(self.connector) + "\nNodes: " + str([str(node) for node in self.nodes])


class UndefinedConnectorContextError(Exception):
    pass


class UndefinedNodeMapError(Exception):
    pass
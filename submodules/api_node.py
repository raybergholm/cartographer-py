#!/usr/bin/env python3

class ApiNode:
    def __init__(self, name, config):
        self.name = name
        self.prefix = config["prefix"] if "prefix" in config else "/"
        self.query_url = config["queryUrl"] if "queryUrl" in config else ""
        self.node_url = config["nodeUrl"] if "nodeUrl" in config else ""

    def query(self):
        return "%s%s" % (self.prefix, self.query_url)

    def by_id(self, id):
        parameterized_path = self.node_url.replace(":id", id)
        return "%s%s" % (self.prefix, parameterized_path)

    def __str__(self):
        return "*ApiNode*:\nqueryUrl: %s\nnodeUrl: %s" % (self.query_url, self.node_url)
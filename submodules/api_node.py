#!/usr/bin/env python3

class ApiNode:
    def __init__(self, node_name, config):
        if not "queryUrl" in config or not "nodeUrl" in config:
            raise Exception("Failed to instantiate %s, missing queryUrl or nodeUrl" % node_name)

        self.prefix = config["prefix"] if "prefix" in config else "/"
        self.query_url = config["queryUrl"]
        self.node_url = config["nodeUrl"]

    def query(self):
        return "%s%s" % (self.prefix, self.query_url)

    def by_id(self, id):
        return "%s%s" % (self.prefix, self.query_url)

    def __str__(self):
        return "*ApiNode*:\nqueryUrl: %s\nnodeUrl: %s" % (self.query_url, self.node_url)
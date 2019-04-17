#!/usr/bin/env python3


def flatten_query_params(params):
    key_value_pairs = ["%s=%s" % (key, value) for key, value in params.items()]
    return "&".join(key_value_pairs)

class ApiNode:
    def __init__(self, node_name, config):
        if not "queryUrl" in config or not "nodeUrl" in config:
            raise Exception("Failed to instantiate %s, missing queryUrl or nodeUrl" % node_name)

        self.prefix = config["prefix"] if "prefix" in config else "/"
        self.query_url = config["queryUrl"]
        self.node_url = config["nodeUrl"]
    
    def flatten_query_params(self, params):
        key_value_pairs = ["%s=%s" % (key, value) for key, value in params.items()]
        return "&".join(key_value_pairs)

    def query(self, query_params=""):
        url = "%s%s" % (self.prefix, self.query_url)
        if query_params != "":
            query_string = flatten_query_params(query_params) 
            url = "%s?%s" % (url, query_string)
        
        return url

    def by_id(self, id, query_params):
        url = "%s%s" % (self.prefix, self.query_url)
        url = url.replace(":id", id)
        if query_params != "":
            query_string = flatten_query_params(query_params) 
            url = "%s?%s" % (url, query_string)
        
        return url

    def __str__(self):
        return "*ApiNode*:\nqueryUrl: %s\nnodeUrl: %s" % (self.query_url, self.node_url)
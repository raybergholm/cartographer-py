# Cartographer for Python

Cartographer is a library for streamlining the connection and calling of an API.

Given a config file containing the connection details of the API and the list of nodes and their details, this library builds a map of the API which is used to construct API calls as required. Rather having to manually make calls like `HTTPSConnection(host_url).request("GET", "/why/did/i/create/such/a/long/chain/to/cake-selection")` calls, just use Cartographer to shorten it to `cartographer.get("cake-selection")` and have Cartographer handle the middle layers for you.

## Changelog

[Click here](./CHANGELOG.md)

## Dependencies

* requests

Make sure you have pip then run `pip install requests`

## How to instantiate

Supply the config file contents in the constructor. This should be read from the file stream but does not need to be converted to JSON, it will be parsed automatically during instantiation.

```python
    def instantiate_cartographer(filepath):
        import cartographer
        with open(filepath, "r") as file_stream:
            config_settings = file_stream.read()
            return cartographer.Cartographer(config_settings)
```

## How to make a request

The cartographer instance has defined methods `get`, `post`, `head`, `post`, `put`, `patch`, `delete` (i.e. the same as HTTP method names) which can be used to make requests. These methods are syntactic sugar that route to the `call` method.

Examples:

```python
    # get /foo
    instance.get("foo")

    # get foo endpoint with id (e.g. /foo/bar)
    instance.get("foo", "bar")

    # get foo endpoint with an additional header
    instance.get("foo", headers={
        "extraheader": "bar"
    })

    # get foo with query params
    instance.get("foo", query={
        "page": 0,
        "limit": 100
    })

    # post to foo with body
    instance.post("foo", body={
        "bar": "baz"
    })
```

The following optional parameters are supported:

* headers - additional headers. This will be merged with common headers defined in the config file (additional headers take priority if the keys clash)
* body - body payload
* query - query parameters

## Config file setup

The config file has at least two base elements.

### Connection

The connection attribute defines the common parts which will be used for all calls done with the instance. The full example structure:

```json
"connection": {
    "protocol": "https",
    "hostUrl": "www.example-api-hosturl.com",
    "auth": {
        "type": "basic",
        "username": "YOUR_USERNAME_HERE",
        "password": "YOUR_PASSWORD_HERE"
    },
    "headers": {
        "x-api-key": "SOME_AWS_API_KEY",
        "somecommonheader": "THIS_WILL_BE_ADDED_TO_ALL_CALLS",
        "authentication": "YOU_CAN_ALSO_INCLUDE_THE_AUTH_HEADER_DIRECTLY_INSTEAD_OF_SUPPLYING_A_USERNAME_AND_PASSWORD"
    }
}
```

In the super minimal case, only the hostUrl is actually mandatory, if no security headers or auth tokens are required then it's fine to specify only the hostUrl.

Note that v0.1 used to directly read `connection.username` and `connection.password`, this is still supported for backcompatibility.

### Nodes

The other main item in the config file is a list of nodes. An example:

```json
"nodes": {
    "users": {
        "rootUrl": "users",
        "variable_url": "users/{0}",
    },
    "userItems": {
        "rootUrl": "users/{0}/items",
        "variable_url": "users/{0}/items/{1}",
    }
}
```

In the above example, `cartographer.get("users")` is equivalent to calling /users while `cartographer.get("users", "1234")` is equivalent to calling hostUrl/users/1234. Multiple substitutions are also supported, so `cartographer.get("usersItems", "1234", "abcd")` -> hostUrl/users/1234/items/abcd

## Troubleshooting

Each call supports verbose debug info, just pass `debug_mode=True` to have request and response details echoed to output.

## TODO: Features on the backlog

* Auto-detect input config settings: auto-detect if the input is already JSON, otherwise try to parse as JSON
* Field lists: automatically filter payloads to only use these fields
* Allowed methods: limit which HTTP methods are allowed per node: trying to make an invalid call throws an error. This can be used to set client-side restrictions if some nodes do not support certain methods.

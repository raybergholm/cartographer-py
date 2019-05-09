# Cartographer for Python

Cartographer is a library for streamlining the connection and calling of an API.

Given a config file containing the connection details of the API and the list of nodes and their details, this library builds a map of the API which is used to construct API calls as required. Rather having to manually make `HTTPSConnection(host_url).request("GET", "/why/did/i/create/such/a/long/chain/to/cake-selection")` calls, just use Cartographer to shorten it to `cartographer.get("cake-selection")` and have Cartographer handle the boring the middle layers.

## How to instantiate
Supply the config file contents in the constructor. This should be read from the file stream but does not need to be converted to JSON, it will be parsed automatically during instantiation.


```python
    def instantiate_cartographer(filepath):
        import cartographer
        with open(filepath, "r") as file_stream:
            config_settings = file_stream.read()
        
        return cartographer.Cartographer(config_settings)
```

## TODO: Features on the backlog

- Auto-detect input config settings: auto-detect if the input is already JSON, otherwise try to parse as JSON
- Field lists: automatically filter payloads to only use these fields
- Allowed methods: limit which HTTP methods are allowed per node: trying to make an invalid call throws an error. This can be used to set client-side restrictions if some nodes do not support certain methods.
# Changelog

## v0.2.0

First major rewrite. The old v0.1 used the standard urllib but upkeep is easier using Requests.

* Now requires the [Requests library](https://requests.readthedocs.io/en/master/)
* If auth is specified but not the type, the default assumption is basic auth
* Added option to set common headers after initial instantiation (adding headers to individual requests remain unchanged)
* Verbose debug mode in individual calls is now triggered by `debug_mode=True`

### Breaking changes v0.1 -> v0.2

The response object returned from a request is now from the Requests library. This means that scripts expecting v0.1 type responses may break, since it's no longer a dictionary-type response. The following table shows some examples:

| old | new |
| --- | --- |
| `response["status"]` | `response.status_code` |
| `response["body"]` | `response.text` |
| `json.loads(response["body"])` | `response.json()` |

Additionally, the `call()` in v0.1 expected additional parameters as a dictionary in `params`, now they have been split to their own keyword arguments. Examples are as follows:

| old | new |
| --- | --- |
| `params.query` | `query` |
| `params.headers` | `headers` |
| `params.body` | `body` |

The following features are supported for backcompatibility with v0.1:

* Basic auth can also be specified in the config by adding `connection.username` and `connection.password`
* `node.rootUrl` can also be declared as `queryUrl`
* `node.variableUrl` can also be declared as `nodeUrl`
* A node's variableUrl with a single substitution can also be declared in the format `path/:id`.

## v0.1.5

* Cleaned up config file parsing, small bug fixes

## v0.1.4

* Added option to set the authentication header later initial instantiation
* Small refactoring to prefer string.format over the old `"%s %s" % ("one", "two")` style
* Fixed insufficient url encoding of query parameters

## v0.1.3

* Added verbose debug mode argument to calls. Pass debug=True as an argument to enable this.
* Fixed detection of HTTP or HTTPS

## v0.1.2

* Fixed handling of null hostUrl in the config file: this now throws an exception

## v0.1.1

* Fixed the handling of opening & closing connections so that there's no unexpected behaviour when chaining calls in sequence

## v0.1.0

* Initial release

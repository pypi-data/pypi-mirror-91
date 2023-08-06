# Configly Python Library
> The Python library for [Configly](https://www.config.ly): the modern config/static data key/value store.

![GitHub](https://img.shields.io/github/license/configly/python)

Table of Contents
=================

* [Configly Python Library](#configly-python-library)
* [Table of Contents](#table-of-contents)
   * [What is Configly?](#what-is-configly)
      * [Core Features](#core-features)
      * [Concepts/ Data Model](#concepts-data-model)
         * [Types](#types)
   * [Getting Started](#getting-started)
      * [1. Get your API Key](#1-get-your-api-key)
      * [2. Create your first Config](#2-create-your-first-config)
      * [3. Install the client library](#3-install-the-client-library)
      * [4. Fetch the Config](#4-fetch-the-config)
   * [Usage](#usage)
   * [API Reference](#api-reference)
      * [Initialization](#initialization)
      * [get(key, options?)](#getkey-options)
         * [Unknown keys](#unknown-keys)
         * [Options](#options)
         * [Errors](#errors)
            * [Example Error Handling](#example-error-handling)
   * [License](#license)


## What is Configly?

[Configly](https://www.config.ly) is the place software developers put their static / config data&mdash;like
 copy, styling, and minor configuration values.
They can then update that data directly from [https://www.config.ly](https://www.config.ly/)
without having to wait for a deploy process / app store review. Their app or webapp receives the data near instantly.
Non-technical folks themselves can publish changes freeing developers to focus on hard software problems and not copy tweaks.

On the backend, [Configly](https://www.config.ly) provides a read-optimized static-data key/value store built
with the aim of being low-latency, and high-availability. The client libraries are made to be dead-simple, lean, and efficient
(via enhancements like caching). There is a fancy [web UI called the Configulator](https://config.ly/config)
for setting and updating the configs as well as seeing things like change history. Configly is built for modern software development.

There are a host of other benefits to using Configly (
such as ensuring you do not have [data duplicated across clients](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself), reducing load on your primary DB, and better tolerance for traffic spikes),
read more about the benefits at [Configly](config.ly).

### Core Features

- API to fetch Strings, JSON Blobs (arrays and objects), Booleans, and Numbers from the Configly backend
- [Web interface](https://www.config.ly/config) for modifying these values without having to deploy code (we call our beloved web interface _the Configulator_).
- High availability, high-throughput, low-latency backend.
- Smart caching on the client libraries to minimize server requests.
- Client libraries available in an expanding amount of languages.

### Concepts/ Data Model
- A Configly account contains a set of Configs.
- A Config is a key-value pair along with associated metadata (like TTL).
- The keys are strings.
- The values are one of the following types:

#### Types

| Type    |  notes   | Example(s)|
|---------|----------|----------|
| string  |          | "I <3 Configly!" |
| number  | Can be integers or decimal; _be aware some clients require you to specify which when fetching_  | 31337, 1.618 |
| boolean | only true or false | true, false |
| jsonBlob | A [JSON5](https://json5.org/) (more relaxed JSON) array or object. | ``` ["one", 5, true]```, ```{"text": "Buy now!", color: "#0F0"}``` |

##### More `jsonBlob` examples
You can make arbitrarily complex JSON structures -- _as long_ as the top level is
an object or array. This is incredibly powerful as you can send a host of data
with a single _config_:


A more complex array for a store inventory. Note that because we're using JSON5, quotes
are optional for single words.
```js
[
  "Simple T-shirt",
  "Basic hoodie",
  {
    item: "Complex T-shirt",
    sizes: ['S', 'M', 'L'],
    price_us_cents: [1099, 1499, 1599],
  }
]
```

And a more complex object showing how you can internationalize and set style:
```js
{
  "welcome_message": {
    copy: {
      'en': 'Welcome!',
      'es': "¡Bienvenidos!",
    }, style: {
      color: '#0F0',
      fontWeight: '700',
    }
  },
  "buy_button" : {
    copy: {
      'en': 'Buy',
      'es': "Comprar",
    }, style: {
      backgroundColor: "#F00",
      border: "border-radius 10px",
    }
  }
}
```

## Getting Started

In four easy steps!

### 1. Get your API Key

You'll need a [Configly](https://www.config.ly) account. Registration is lightning quick&mdash;you can register via
visiting [https://www.config.ly/signup](https://www.config.ly/signup).

After signing up, you can grab your API Key from [https://www.config.ly/config](https://www.config.ly/config).
You'll need your API Key to setup the API below.

### 2. Create your first Config
From [https://www.config.ly/config](https://www.config.ly/config), create a new Config via the "Add" button:
![image](https://user-images.githubusercontent.com/184923/98487495-3b42ca80-21f1-11eb-9bfc-bfd429733362.png)

Consider creating a simple `JSON Object or Array` Config called `greetings` and give it the value of:
`['hello', 'hola', '你好', 'नमस्ते']`:

[https://www.config.ly/config](https://www.config.ly/config) should look like this:

![image](https://user-images.githubusercontent.com/184923/98494454-09d6f880-220b-11eb-9ef7-36709ddc129f.png)

Be sure to save via clicking 'Send to Clients'. Now, we'll write client code to fetch this key.

### 3. Install the client library

```sh
pip install configly-python
```

### 4. Fetch the Config

Add the following code in the execution path of a Python application. It could be a Django or Flask
app or a script.

```python
import configly
from configly import errors

configly.api_key = 'YOUR_API_KEY'

try:
    greetings_list = configly.get('greetings')
    if greetings_list is None:
        print('Can't find key')
    else:
        print('Greetings!\n')
        for saying in greetings_list:
            print(f'A greeting: {saying}')
except errors.InvalidApiKeyError as error:
    print(f'Invalid API Key: {error.message}')
except errors.ConfiglyRequestError as error:
    print(f'Generic error: {error.message}')
except errors.ConfiglyConnectionError as error:
    print(f'Connection error: {error.message}')
    # print(error.original_error)
```

Try changing some values on [https://www.config.ly/config](https://www.config.ly/config) to confirm that
the client is getting the updates.

Congratulations you have Configly working end-to-end! Now, feel free to use Configly with all your projects!

## Usage
> The golden rule of Configly library use is: **do NOT** assign the result of a `get()`
to a long-lived variable; in order to check for new values from the server, you must call `get()`.

The package needs to be configured with your account's API key, which is available in the
[Configly Configulator](https://config.ly/config)

```
// This value is stored on the Config.ly servers.
store_catalog:
{
   has_sale: true,
   discount: 0.8,
   items: ['T Shirt', 'Hoodie', 'Ferrari'],
   price: [100, 250,  200000],
}
```

On the Python client:

```python
# You can try this example out by setting the `CONFIGLY_API_KEY` environmental variable to our demo account: 'Dem0apiKEY'
try:
    catalog = configly.get('store_catalog')

    # `get` returns None if the key is not found.
    if catalog is None:
        print('The key was not found')
    else:
        items = catalog['items']
        prices = catalog['prices']

        for index in range(0, len(items)):
            item = items[index]
            price = prices[index]
            if catalog['has_sale']:
                price = catalog['discount']*price
            print(f'{item}: {price:.2f} USD')
except Exception as error:
    print(error)
    # configly.errors.InvalidApiKeyError is thrown when there's an unknown API Key
    # configly.errors.ConfiglyRequestError is thrown on a timeout or failure to connection to the server
    # configly.errors.ConfiglyrequestError is thrown when the server responds with an error
```
## API Reference
### Initialization
The module must be imported and configured prior to any call to `get`.

You can set global options directly on the module. API Key is a required value
and the rest are optional.


```python
import configly

configly.api_key = 'YOUR_API_KEY' # Required

# Global Defaults - these are optional and can be overriden per-request.

# Seconds to timeout on requests to the servers
configly.timeout = 3

# Disabling caching will cause the client to ignore server-set TTLs and make a
# a request to Configly's servers on every call to `get` - use this only if
# it is essential that your data is always fresh and you are not worried about
# latency/bandwidth usage.
configly.enable_cache = True
```

### `get(key, options?)`
`get()` exposes the core function of the library; is to request values stored in Configly.

`get()` accepts a string as its first argument&dash;a key. Configly will fetch the corresponding
value from the Configly servers (or look it up in the local library cache).

```python
hero = configly.get('the_best_superhero')
print(hero)
```
#### Unknown keys
`get` returns `None` if the key is not recognized

```python
hero = configly.get('the_best_superhero')
if hero is None:
  print('There is no best superhero!')
else:
  print(hero)
```
#### Options
You can pass per-request values for `timeout` and `enable_cache` that will
override any global settings set on module first load.

```python
# In this example, it's crucial we have up-to-date data and we're willing wait
# for it (in the case that something goes wrong). Note these overrides are for
# _only_ this call to get()
options = { "timeout": 5, "enable_cache": False }
feature_flag = configly.get("feature1_enabled", options)

if feature_flag:
    print("Feature is enabled")
else:
    print("Feature is disabled!")
```
Both options are optional.

#### Errors
`get` can throw any of several errors. The errors are in the `configly.errors` namespace:

| Key   | Explanation  |
| ----- | -------- |
| `InvalidApiKeyError` | Configly's server returned a 401. This likely means the `API Key` supplied in `init()` is incorrect. You can see your API Key in the [https://config.ly/config](Configluator). |
| `ConfiglyConnectionError` | There was a problem communicating with the Config.ly backend. This could be due to a network fault, bad internet connection, or timeout. You can see the original error in the `original_error` member. Try again later. If the problem persists [let us know](mailto:configlyco@gmail.com)! |
| `ConfiglyRequestError` | A miscellaneous error. Take a look at the `request` value inside the returned object to see the response from Configly's servers. This could indicate a problem with the library; if so, you can create a [Github issue](https://github.com/configly/js/issues) and we'll look into it. |

Each error has a `message` variable with further details.

##### Example Error Handling
```python
try:
    copy = configly.get('en_copy')
    if copy is None:
        print("No copy was found")
    else:
      print(copy)
except errors.InvalidApiKeyError as error:
    print(f"Invalid API Key: {error.message}")
except errors.ConfiglyRequestError as error:
    print(f"Generic error: {error.message}")
    # You can access the response via error.response
except errors.ConfiglyConnectionError as error:
    print(f"Connection error: {error.message}")
    # You can access the internal error via original_error
```

## License

This repository is published under the [MIT](LICENSE.md) license.

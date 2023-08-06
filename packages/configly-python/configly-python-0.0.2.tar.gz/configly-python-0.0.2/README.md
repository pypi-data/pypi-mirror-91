# Configly Python Library
> The Python library for [Configly](https://www.config.ly): the modern config/static data key/value store.

![npm](https://img.shields.io/gem/v/configly-ruby)
![GitHub](https://img.shields.io/github/license/configly/ruby)

Table of Contents
=================

  * [What is Configly?](#what-is-configly)
     * [Core Features](#core-features)
     * [Concepts/ Data Model](#concepts--data-model)
  * [Getting Started](#getting-started)
    + [1. Get your API Key](#1-get-your-api-key)
    + [2. Create your first Config](#2-create-your-first-config)
    + [3. Install the client library](#3-install-the-client-library)
    + [4. Fetch the Config](#4-fetch-the-config)
  * [Usage](#usage)
    * [Feature Flags](#feature-flags)
  * [Configuring this library to use websockets](#configuring-this-library-to-use-websockets)
  * [License](#license)
- [Configly Python Library](#configly-ruby-library)


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

After signing up, you can grab your API Key from [https://www.config.ly/register](https://www.config.ly/register).
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

If you're using [Bundler](https://bundler.io/) (as is often the case with Rails), add the following line to your project's `Gemfile`:
```sh
gem 'configly-ruby', '~> 1.0.0'
```

Or, if you're using the Gem directly from your application, you can run:
```sh
gem install configly-ruby
```

You will need to set the `CONFIGLY_API_KEY` [environment variable](https://www.rubyguides.com/2019/01/ruby-environment-variables/).

### 4. Fetch the Config
In a Rails controller, add the following code
```ruby
def get
   begin
      key = Configly::Client.get(params[:key])
      render plain: key
   rescue Configly::KeyError
      render :status => 404
   end
end
```

Map the route, and then request it in your browser with the `key` params (e.g. `http://localhost:3000/configly?key=test1234`). 

Try changing some values on [https://www.config.ly/config](https://www.config.ly/config) to confirm that
the client is getting the updates.

Congratulations you have Configly working end-to-end! Now, feel free to use Configly with all your projects!

## Configuring this library to use websockets
Coming soon...

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
   price: [ 100, 250,  200000],
}
```

On the Python client:

```ruby
# You can try this example out by setting the `CONFIGLY_API_KEY` environmental variable to our demo account: 'Dem0apiKEY' 
begin
   catalog = Configly::Client.get("store_catalog")
   items = catalog['items']
   prices = catalog['prices']

   items.each_with_index do |item, index|
      Rails.logger.debug("#{item}: #{prices[index]} USD")
   end
rescue Configly::KeyError
   Rails.logger.error("Something went wrong")
end
```

Note: If the key doesn't exist, this will raise a `Configly::KeyError`

### Feature Flags
Here is an example with feature flags. 

```
// These values are stored on the Config.ly server

feature1_enabled: true
feature2_enabled: false
```

On the ruby client:

```ruby
# Remember, you need to set the `CONFIGLY_API_KEY` environment variable. 
# You can find your API Key on https://www.config.ly/config.

begin
  if Configly::Client.get('feature1_enabled')
    # Logic for feature 1
  end

  if Configly::Client.get('feature2_enabled')
    # Logic for feature 2
  end
rescue Configly::KeyError
   Rails.logger.error("Something went wrong")
end
```

## License

This repository is published under the [MIT](LICENSE.md) license.

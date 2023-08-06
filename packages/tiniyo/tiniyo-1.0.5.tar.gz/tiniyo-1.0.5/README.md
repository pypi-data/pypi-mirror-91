# tiniyo-python


### Supported Python Versions

This library supports the following Python implementations:

* Python 2.7
* Python 3.4
* Python 3.5
* Python 3.6
* Python 3.7
* Python 3.8

## Installation

Install from PyPi using [pip](https://pip.pypa.io/en/latest/), a
package manager for Python.

    pip install tiniyo

If pip install fails on Windows, check the path length of the directory. If it is greater 260 characters then enable [Long Paths](https://docs.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation) or choose other shorter location.

Don't have pip installed? Try installing it, by running this from the command
line:

    $ curl https://bootstrap.pypa.io/get-pip.py | python

## Getting Started

Getting started with the Tiniyo API couldn't be easier. Create a
`Client` and you're ready to go.

### API Credentials

The `Tiniyo` needs your Tiniyo credentials. You can either pass these
directly to the constructor.

```python
from tiniyo.rest import Client

account = "AAAAAAAAAAAA"
token = "BBBBBBBBBBBBBBBBBBBBBBB"
client = Client(account, token)
```

### Make a Call

```python
from tiniyo.rest import Client

account = "AAAAAAAAAAAA"
token = "BBBBBBBBBBBBBBBBBBBBBBB"
client = Client(account, token)

call = client.calls.create(to="122122313",
                           from="12112121",
                           url="https://raw.githubusercontent.com/tiniyo/public/master/answer_speak.xml")
print(call.sid)
```

### Send an SMS

```python
from tiniyo.rest import Client

account = "AAAAAAAAAAAA"
token = "BBBBBBBBBBBBBBBBBBBBBBB"
client = Client(account, token)

message = client.messages.create(to="122122313", from="12112121",
                                 body="Hello there!")
```

### Enable Debug Logging

Log the API request and response data to the console:

```python
import logging

client = Client(account, token)
logging.basicConfig()
client.http_client.logger.setLevel(logging.INFO)
```

Log the API request and response data to a file:

```python
import logging

client = Client(account, token)
logging.basicConfig(filename='./log.txt')
client.http_client.logger.setLevel(logging.INFO)
```

### Generating TinyXML

To control phone calls, your application needs to output [TinyXML][TinyXML].

Use `tiniyo.voice_response` or `tiniyo.messaging_response` to easily create such responses.

```python
from tiniyo.voice_response import VoiceResponse

r = VoiceResponse()
r.say("Welcome to TinyXML!")
print(str(r))
```

```xml
<?xml version="1.0" encoding="utf-8"?>
<Response><Say>Welcome to TinyXML!</Say></Response>
```

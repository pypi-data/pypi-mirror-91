# spotify-client
Client for interacting with the Spotify API

Full documentation for the library is available on [Read the Docs](https://spotify-client.readthedocs.io)

## Usage

First install the package with pip:

`pip install spotify-client`

Then import the client for usage in your application:

```python
from spotify_client import SpotifyClient

SPOTIFY_CLIENT_ID = 'client_id_from_spotify'
SPOTIFY_SECRET_KEY = 'secret_key_from_spotify'

client = SpotifyClient(SPOTIFY_CLIENT_ID, SPOTIFY_SECRET_KEY, identifier='test-spotify-client')
```

You'll need to generate your client ID and secret keys for authenticating with Spotify from their API console. You can
find the steps for doing that in the [Spotify documentation](https://developer.spotify.com/documentation/general/guides/app-settings/).

Optionally, you can also configure the client authentication configuration one time in a setup script by using the
`Config` class:

```python
from spotify_client import SpotifyClient
from spotify_client.config import Config

SPOTIFY_CLIENT_ID = 'client_id_from_spotify'
SPOTIFY_SECRET_KEY = 'secret_key_from_spotify'

Config.configure(SPOTIFY_CLIENT_ID, SPOTIFY_SECRET_KEY)

client = SpotifyClient()
```

The client will make a request to generate the access_token the first time it makes a call to the API. It will then
cache the access token as an instance variable, to use in future requests by that client instance. This avoids the
overhead of having to make a request for the access token on each request to the API.

You can optionally pass an identifier to the constructor. This will be used in logging messages by the client to
uniquely identify logs for the client instance.


## Developing

To work on this library, you'll first need to clone the repository:

`git clone git@github.com:Moody-Tunes/spotify-client.git`

Next, create a virtual environment and install the dependencies for development:

```shell script
virtualenv -p $(which python3) venv
source venv/bin/activate
(venv) pip install -r dev.txt
```

### pre-commit

We use [pre-commit](https://pre-commit.com/) for running hooks during git commits. This will help immensely with
developer workflow by running linters, checkers, and other tools when you make commits. To install pre-commit, create a
virtual environment and install pre-commit:

```shell script
(venv) pip install pre-commit
```

Next, install the pre-commit packages we use in our project:

```shell script
(venv) pre-commit install
```

This should run the pre-commit hooks when you make a commit to the spotify-client repository.

### Running Tests

We use [pytest](https://docs.pytest.org/en/stable/) for running tests. You can run the spotify-client test suite by
invoking pytest in the virtual environment:

`(venv) pytest`

We also use [pytest-cov](https://pypi.org/project/pytest-cov/) for reporting test coverage of the library. This will
be displayed after the tests have finished running and report lines in the code that have test coverage.

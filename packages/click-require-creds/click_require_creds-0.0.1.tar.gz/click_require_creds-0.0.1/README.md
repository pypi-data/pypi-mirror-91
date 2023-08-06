# Click decorator to handle creentials

This package provides a simple way to handle interactive provided credentials in Click applications.

Additionally, credentials are cached based on a key (usually a username)  

## Install


```
pip install click-require-creds
```

## Usage

Minimal example, by default asks for _username_ and _password_ and pass them to the decorated function as parameters. Once the input is cached, it won't ask for credentials until TTL expires.

```
import click
from click_require_creds import setup, require_creds 

setup('my-click-app', default_ttl=800)

@click.command()
@require_creds()
def cli(username, password):
    click.echo(f"User {username} password is {password}")
```

But you can use custom parameters:

```
import click
from click_require_creds import setup, require_creds 

setup('my-click-app', default_ttl=800)

@click.command()
@require_creds('tokenid', 'secret')
def cli(tokenid, secret):
    click.echo(f"Tokenid {tokenid} secret is {secret}")
```

You can also set individual TTL cache per command:

```
import click
from click_require_creds import setup, require_creds 

setup('my-click-app', default_ttl=800)

@click.command()
@require_creds('tokenid', 'secret' ttl=60*60*24)
def cli(tokenid, secret):
    click.echo(f"Tokenid {tokenid} secret is {secret}")
``` 

It also possible to pass values as options (e.g. set user as $USER by default, it won't ask for user)

```
import click
from click_require_creds import setup, require_creds 

setup('my-click-app', default_ttl=800)

@click.command()
@click.option("--user", "-u", prompt=True, envvar="USER", help="Username")
@require_creds()
def cli(username, password):
    click.echo(f"User {username} password is {password}")
``` 


## Considerations

- Cache can store any object that can be `pickled`
- It's not thread-safe
- It does not encrypt credentials on disk
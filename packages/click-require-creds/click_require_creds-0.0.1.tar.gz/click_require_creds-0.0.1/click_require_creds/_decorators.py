import click

from ._helpers import login


def require_creds(key="username", value="password", ttl=None):
    """
    Click decorator to ask for username/password (or generally key/value) for a given command.
    It will cache key/value locally for a given TTL.
    This decorator will do the following:
    - Check that "key" and "value" are parameters of the command
    - If "key" is not provided, ask for it.
    - Check if credentials are cached for the given key
    - If not cached, ask for credentials "value" and then save it.
    - Return credentials as parameter "value"

    By default, assumes that "key" is "username" and "value" is "password".
    Args:
        key (str): short and/or long decls ex: ("-p", "--password")
        value (None, str): Identifies the click option name that holds the username.
         If not provided, defaults to "username"
        ttl (dict): Addition keyword arguments to pass to click option
    """
    from ._core import credentials_cache

    def decorator(func):
        def wrapper_func(*args, **kwargs):
            # Check params of func
            for parameter in [key, value]:
                if parameter not in func.__code__.co_varnames:
                    raise click.ClickException(
                        f"Function/command '{func.__name__}' requires '{parameter}' parameter"
                    )

            # Do login if needed
            user = login(key, value, ttl=ttl, **kwargs)

            creds = credentials_cache.get(user)
            kwargs[value] = creds
            kwargs[key] = user
            return func(*args, **kwargs)

        wrapper_func.__name__ = func.__name__
        return wrapper_func

    return decorator

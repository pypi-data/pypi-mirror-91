"""
Click helpers
"""
import click


def login(key, value, ttl=None, **kwargs):
    from ._core import credentials_cache

    user = kwargs.get(key, None)
    while not user:
        user = click.prompt(f"{key.capitalize()}", err=True)

    creds = kwargs.get(value, None)
    while not (creds or credentials_cache.authenticated(user)):
        creds = click.prompt(
            f"{value.capitalize()} for {user}", hide_input=True, err=True
        )
        credentials_cache.save(user, creds, ttl=ttl)

    return user


def logout(user):
    from ._core import credentials_cache

    if credentials_cache.logged_in(user):
        credentials_cache.remove(user)
        return True
    return False


def clear_cache():
    from ._core import credentials_cache

    return credentials_cache.clear()

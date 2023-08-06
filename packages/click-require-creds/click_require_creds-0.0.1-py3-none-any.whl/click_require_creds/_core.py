import os

import click
import nttldict

credentials_cache = None


def setup(app_name, dbname="click-require-creds.db", default_ttl=300):
    global credentials_cache
    local_dir = click.get_app_dir(app_name)
    os.makedirs(local_dir, exist_ok=True)
    creds_backend = os.path.join(local_dir, dbname)
    credentials_cache = CredentialsCache(
        creds_backend=creds_backend, default_ttl=default_ttl
    )


class CredentialsCache:
    def __init__(
        self,
        creds_backend=None,
        default_ttl=None,
    ):
        self.creds_store = nttldict.NaiveTTLDictDisk(creds_backend, default_ttl)

    def logged_in(self, key):
        return key in self.creds_store.keys()

    def authenticated(self, key):
        return self.logged_in and bool(self.creds_store.get(key, None))

    def get(self, key):
        """Get a credential saved previously for the provided key."""
        if self.authenticated(key):
            return self.creds_store.get(key)
        return None

    def save(self, key, creds, ttl=None):
        self.creds_store.set(key, creds, ttl=ttl)

    def remove(self, key):
        del self.creds_store[key]

    def clear(self):
        self.creds_store.clear()

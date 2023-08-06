"""Contains functions that convert a parameter into something else."""
import hashlib
import json
from urllib.parse import quote


def password_to_hash(password: str):
    """Generate a sha1 password from string."""
    if password is None:
        return None
    pw_hash = hashlib.sha1(password.encode('utf-8'))
    return pw_hash.hexdigest()


def quote_json(_json: dict) -> str:
    """Convert JSON to HTML quote."""
    stringified = json.dumps(_json)
    return quote(stringified)

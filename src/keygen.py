import secrets
import string

from sqlalchemy.orm import Session

from . import crud


def create_random_key(length: int = 5) -> str:
    chars = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(chars) for _ in range(length))


def create_unique_random_key(db: Session) -> str:
    key = create_random_key()
    while crud.get_link_by_short_code(db, key):
        key = create_random_key()
    return key

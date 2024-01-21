import secrets
import string

from sqlalchemy.orm import Session

from src import crud, config


def create_random_key(length: int = 5) -> str:
    chars = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(chars) for _ in range(length))


def create_unique_random_key(db: Session) -> str:
    key = create_random_key(config.get_settings().short_code_len)
    while crud.short_code_exists(db, key):
        key = create_random_key(config.get_settings().short_code_len)
    return key

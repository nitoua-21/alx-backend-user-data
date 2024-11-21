#!/usr/bin/env python3
"""
Module auth
"""
import bcrypt
import uuid
from sqlalchemy.orm.exc import NoResultFound
from db import DB, User


def _hash_password(password: str) -> bytes:
    """Returns a salted hash of the input password
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generate a UUID"""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Auth Initializer
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user to the database"""
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        raise ValueError("User {} already exists".format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """Check email and password combinaison
        """
        try:
            user = self._db.find_user_by(email=email)
            if user is not None:
                return bcrypt.checkpw(
                    password.encode('utf-8'),
                    user.hashed_password
                )
        except NoResultFound:
            return False
        return False

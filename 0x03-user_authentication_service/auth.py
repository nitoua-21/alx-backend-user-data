#!/usr/bin/env python3
"""
Module auth
"""
import bcrypt


def _hash_password(password: str) -> str:
    """Returns a salted hash of the input password
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

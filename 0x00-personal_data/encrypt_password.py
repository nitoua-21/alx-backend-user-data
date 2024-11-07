#!/usr/bin/env python3
"""
Module for encrypting passwords
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hash a password using bcrypt

    Args:
        password: String password to hash

    Returns:
        bytes: Salted and hashed password
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validate that the provided password matches the hashed password

    Args:
        hashed_password: Bytes of the hashed password
        password: String of the password to check

    Returns:
        bool: True if password matches, False otherwise
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

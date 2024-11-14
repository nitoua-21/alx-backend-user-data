#!/usr/bin/env python3
"""
Authentication module for the API
"""
from flask import request
from typing import List, TypeVar
import re


class Auth:
    """
    Authentication class
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines whether a path requires authentication
        """
        if path is None or excluded_paths is None or not excluded_paths:
            return True

        # Make sure path ends with /
        if not path.endswith('/'):
            path += '/'

        # Check if path matches any excluded path pattern (with * support)
        for excluded_path in excluded_paths:
            # Convert * to regex pattern
            pattern = excluded_path.replace('*', '.*')
            if re.match(f"^{pattern}$", path):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Returns the authorization header from a request
        """
        if request is None:
            return None

        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns the current user from the request
        """
        return None

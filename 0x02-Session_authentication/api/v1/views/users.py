#!/usr/bin/env python3
""" Module of Users views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def view_all_users() -> str:
    """ GET /api/v1/users
    Return:
      - list of all User objects JSON represented
    """
    all_users = [user.to_json() for user in User.all()]
    return jsonify(all_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def view_one_user(user_id: str = None) -> str:
    """ GET /api/v1/users/:id
    Path parameter:
      - User ID or 'me' to retrieve the authenticated user
    Return:
      - User object JSON represented
      - 404 if the User ID doesn't exist
    """
    if user_id == "me" and request.current_user is None:
        abort(404)
    
    if user_id == "me" and request.current_user is not None:
        return jsonify(request.current_user.to_json())

    if user_id is None:
        abort(404)
    
    user = User.get(user_id)
    if user is None:
        abort(404)
    
    return jsonify(user.to_json())

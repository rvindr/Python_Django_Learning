from rest_framework.permissions import BasePermission
from account.mongo_client import roles_collection
import logging


class IsAdminPermission(BasePermission):
    def has_permission(self, request, view):
        # Ensure the user is authenticated and is an admin
        user = request.user
        return user.is_authenticated and user.is_admin


class HasPermission(BasePermission):
    def __init__(self, required_permission=None):
        self.required_permission = required_permission

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False

        role_id = user.role_id
        if not role_id:
            return False

        try:
            role = roles_collection.find_one({"_id": role_id})
        except Exception as e:

            return False

        if not role:
            return False

        if self.required_permission in role.get("permissions", []):
            return True

        return False

    @classmethod
    def require(cls, permission):
        return lambda: cls(permission)

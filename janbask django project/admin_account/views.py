from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from user_management.mongo_client import users_collection, logs_collection
from account.serializers import RegistrationSerializer
from admin_account.serializers import (
    RoleSerializer,
    PermissionSerializer,
    UserRoleAssignmentSerializer,
    AdminLoginSerializer,
)
from rest_framework.permissions import IsAuthenticated
from user_management.customJWTAuthentication import CustomJWTAuthentication
from user_management.permission import IsAdminPermission, check_permission
from user_management.mongo_client import roles_collection, permissions_collection
from account.serializers import UserSerializer
from account.models import UserModel
from account.utils import Util
from bson import json_util

class AdminLoginView(APIView):

    def post(self, request):
        serializer = AdminLoginSerializer(data=request.data)

        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)

        return Response(
            {"error": serializer.errors}, status=status.HTTP_401_UNAUTHORIZED
        )


class AdminOnlyView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminPermission]

    def get(self, request):
        return Response({"message": "Admin access granted"})


class AdminUserManagementView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminPermission]

    def get(self, request, user_id=None):
        if user_id:
            # Retrieve a specific user by ID
            user = users_collection.find_one({"_id": user_id})
            if user:
                user_data = UserSerializer(user).data

                # Retrieve role name
                role_id = user.get('role_id')
                if role_id:
                    role = roles_collection.find_one({"_id": role_id})
                    if role:
                        user_data['role_name'] = role.get('name')
                    else:
                        user_data['role_name'] = 'Unknown Role'
                else:
                    user_data['role_name'] = 'No Role Assigned'

                return Response({"user": user_data})
            else:
                return Response(
                    {"error": "User not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            # Retrieve all users
            users = users_collection.find()
            user_list = []
            for user in users:
                user_data = UserSerializer(user).data
                # Retrieve role name
                role_id = user.get('role_id')
                if role_id:
                    role = roles_collection.find_one({"_id": role_id})
                    if role:
                        user_data['role_name'] = role.get('name')
                    else:
                        user_data['role_name'] = 'Unknown Role'
                else:
                    user_data['role_name'] = 'No Role Assigned'
                
                user_list.append(user_data)

            return Response({"users": user_list})
    def post(self, request):
        # Create a new user
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.save()

            # Send email
            # Send email
            email_data = {
                "subject": "Your account was registered successfully!",
                "body": f"""Dear {data["first_name"]} {data["last_name"]},
                
                Your account has been created successfully. Your registered email is {data["email"]}.
                
                Note: Please use the 'Forgot Password' link on the login page to reset your password.""",
                "to_email": data["email"],
            }
            Util.send_email(email_data)
            return Response(
                {"detail": "User registered successfully!", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )

    def put(self, request, user_id):
        # Update user data
        user_data = request.data
        user = users_collection.find_one({"_id": user_id})
        if not user:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = UserSerializer(data=user_data, partial=True)
        if serializer.is_valid():
            updated_data = serializer.validated_data
            # Update the user in MongoDB
            updated_user = users_collection.find_one_and_update(
                {"_id": user_id}, {"$set": user_data}, return_document=True
            )

            if not updated_user:
                return Response(
                    {"error": "Failed to update user"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # Log the user update
            user_model = UserModel(**updated_user)
            user_model.log_activity(
                action="User Updated", details={"updated_fields": user_data}
            )

            return Response({"message": "User updated successfully"})
        return Response(
            {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )

    def patch(self, request, user_id):
        # active a user
        user = users_collection.find_one({"_id": user_id})
        if not user:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        users_collection.update_one({"_id": user_id}, {"$set": {"is_active": True}})
        return Response({"message": "User activated successfully"},status=status.HTTP_200_OK)

    def delete(self, request, user_id):
        # Inactivate (delete) a user
        user = users_collection.find_one({"_id": user_id})
        if not user:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # instead of deleting, you might want to update a field to mark the user as inactive
        users_collection.update_one({"_id": user_id}, {"$set": {"is_active": False}})
        return Response({"message": "User deactivated successfully"},status=status.HTTP_200_OK)

class AdminUserLogView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminPermission]

    def get(self, request, user_id):
        user_logs = list(logs_collection.find({"user_id": user_id}))
        if not user_logs:
            return Response(
                {"error": "No logs found for this user"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        # Serialize the logs to JSON format
        logs_json = json_util.dumps(user_logs)

        return Response({"user_logs": logs_json},status=status.HTTP_200_OK)


class RoleManagementView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminPermission]

    def get(self, request):
        # Retrieve all roles
        roles = roles_collection.find()
        role_list = [RoleSerializer(role).data for role in roles]
        return Response({"roles": role_list}, status=status.HTTP_200_OK)

    def post(self, request):
        # Create a new role
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "Role created successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, role_id):
        # Delete a role
        role = roles_collection.find_one({"_id": role_id})
        if not role:
            return Response(
                {"error": "Role not found"}, status=status.HTTP_404_NOT_FOUND
            )

        roles_collection.delete_one({"_id": role_id})
        return Response({"message": "Role deleted successfully"})


class PermissionManagementView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminPermission]

    def get(self, request):
        # Retrieve all permissions
        permissions = permissions_collection.find()
        permission_list = [
            PermissionSerializer(permission).data for permission in permissions
        ]
        return Response({"permissions": permission_list}, status=status.HTTP_200_OK)

    def post(self, request):
        # Create a new permission
        serializer = PermissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "Permission created successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, permission_id):
        # Delete a permission
        permission = permissions_collection.find_one({"_id": permission_id})
        if not permission:
            return Response(
                {"error": "Permission not found"}, status=status.HTTP_404_NOT_FOUND
            )
        
        # Remove the permission from roles
        roles_collection.update_many(
            {"permissions": permission_id},
            {"$pull": {"permissions": permission_id}}
        )

        permissions_collection.delete_one({"_id": permission_id})
        return Response({"detail": "Permission deleted successfully"},status=status.HTTP_200_OK)


class UserRoleAssignmentView(APIView):
    def put(self, request, user_id):
        user = users_collection.find_one({"_id": user_id})
        if not user:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = UserRoleAssignmentSerializer(data=request.data)
        if serializer.is_valid():
            role_id = serializer.validated_data["role_id"]
            users_collection.update_one(
                {"_id": user_id}, {"$set": {"role_id": role_id}}
            )
            return Response({"message": "Role assigned to user successfully"})
        return Response(
            {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


class SomeView(APIView):
    permission_classes = [IsAuthenticated]

    @check_permission("read")
    def get(self, request):
        return Response({"message": "GET access granted"})

    @check_permission("write")
    def post(self, request):
        return Response({"message": "POST access granted"})

    @check_permission("update")
    def put(self, request):
        return Response({"message": "PUT access granted"})

    @check_permission("update")
    def patch(self, request):
        return Response({"message": "PATCH access granted"})

    @check_permission("delete")
    def delete(self, request):
        return Response({"message": "DELETE access granted"})

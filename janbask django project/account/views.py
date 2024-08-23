from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from account.mongo_client import users_collection, logs_collection
from account.serializers import (
    RegistrationSerializer,
    LoginSerializer,
    ChangePasswordSerializer,
    PasswordResetEmailSerializer,
    PasswordResetSerializer,
    RoleSerializer,
    PermissionSerializer,
    UserRoleAssignmentSerializer,
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from account.customJWTAuthentication import CustomJWTAuthentication
from account.permission import IsAdminPermission, HasPermission
from account.mongo_client import roles_collection, permissions_collection
from account.serializers import UserSerializer  # UserCreateSerializer
from django.contrib.auth.hashers import make_password, check_password
from account.models import UserModel


class RegistrationView(APIView):

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "user registered successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


class LoginView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)

        return Response(
            {"error": serializer.errors}, status=status.HTTP_401_UNAUTHORIZED
        )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout_class = CustomJWTAuthentication()
        logout_res = logout_class.logout(request)

        return Response(logout_res, status=status.HTTP_200_OK)


class Testing(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"msg": "working"})


class UserChangePassword(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data, context={"user": user})

        if serializer.is_valid():
            # Save the new password
            serializer.save()

            # Log the activity
            user.log_activity(
                action="Password Changed",
                details={"reason": "User changed their password."},
            )

            return Response(
                {"detail": "Password changed successfully"}, status=status.HTTP_200_OK
            )

        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


class SendPasswordResetEmailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetEmailSerializer(data=request.data)

        if serializer.is_valid():
            return Response(
                {"detail": "Password reset link send. Please check your email"},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


class PasswordResetView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, uid, token):
        serializer = PasswordResetSerializer(
            data=request.data, context={"uid": uid, "token": token}
        )

        if serializer.is_valid():
            response_data = serializer.save()
            return Response(response_data, status=status.HTTP_200_OK)

        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
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
            # Scenario 4: Retrieve and return user activity logs for a specific user
            user_logs = list(logs_collection.find({"user_id": user_id}))
            if not user_logs:
                return Response(
                    {"error": "No logs found for this user"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            return Response({"user_logs": str(user_logs)})
        else:
            # Retrieve all users
            users = users_collection.find()
            user_list = [UserSerializer(user).data for user in users]
            return Response({"users": user_list})

    def post(self, request):
        # Create a new user
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "user registered successfully", "data": serializer.data},
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

    def delete(self, request, user_id):
        # Inactivate (delete) a user
        user = users_collection.find_one({"_id": user_id})
        if not user:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # instead of deleting, you might want to update a field to mark the user as inactive
        users_collection.update_one({"_id": user_id}, {"$set": {"is_active": False}})
        return Response({"message": "User deactivated successfully"})


# ---------------------Role and permission-------


class RoleManagementView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminPermission]

    def get(self, request):
        # Retrieve all roles
        roles = roles_collection.find()
        role_list = [RoleSerializer(role).data for role in roles]
        return Response({"roles": role_list})

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

    # def put(self, request, role_id):
    #     # Update role permissions
    #     role = roles_collection.find_one({"_id": role_id})
    #     if not role:
    #         return Response(
    #             {"error": "Role not found"}, status=status.HTTP_404_NOT_FOUND
    #         )

    #     serializer = RoleSerializer(data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.update(role, serializer.validated_data)
    #         return Response({"message": "Role updated successfully"})
    #     return Response(
    #         {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
    #     )

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
        return Response({"permissions": permission_list})

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

        permissions_collection.delete_one({"_id": permission_id})
        return Response({"message": "Permission deleted successfully"})


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
    permission_classes = [IsAuthenticated, HasPermission.require("manage roles")]

    def get(self, request):
        return Response({"message": "GET access granted"})

    def put(self, request):
        return Response({"message": "PUT access granted"})

    def delete(self, request):
        return Response({"message": "DELETE access granted"})


class UserInfoView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get the authenticated user's ID from the request
        user_id = request.user.id

        # Fetch the user information from MongoDB
        user = users_collection.find_one({"_id": user_id})
        if not user:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # Serialize the user data
        serializer = UserSerializer(user)
        return Response({"user_info": serializer.data}, status=status.HTTP_200_OK)

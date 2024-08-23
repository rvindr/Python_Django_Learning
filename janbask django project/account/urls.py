from django.urls import path
from account.views import (
    RoleManagementView,
    PermissionManagementView,
    RegistrationView,
    LoginView,
    LogoutView,
    Testing,
    UserChangePassword,
    SendPasswordResetEmailView,
    PasswordResetView,
    AdminOnlyView,
    AdminUserManagementView,
    UserRoleAssignmentView,
    SomeView,
    UserInfoView,
)

urlpatterns = [
    path("register/", RegistrationView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("change-password/", UserChangePassword.as_view(), name="change-password"),
    path(
        "send-reset-password/",
        SendPasswordResetEmailView.as_view(),
        name="send-reset-password",
    ),
    path(
        "reset-password/<uid>/<token>/",
        PasswordResetView.as_view(),
        name="reset-password",
    ),
    path("admin/", AdminOnlyView.as_view(), name="admin"),
    path(
        "admin/users/", AdminUserManagementView.as_view(), name="admin-user-management"
    ),
    path(
        "admin/users/<str:user_id>/",
        AdminUserManagementView.as_view(),
        name="admin-user-detail",
    ),
    path(
        "admin/users/<str:user_id>/logs/",
        AdminUserManagementView.as_view(),
        name="user-activity-logs",
    ),
    path("user-info/", UserInfoView.as_view(), name="user-info"),
    # ---------------------Role and permission-------
    path("admin/roles/", RoleManagementView.as_view(), name="role-management"),
    path(
        "admin/roles/<str:role_id>/", RoleManagementView.as_view(), name="role-detail"
    ),
    path(
        "admin/permissions/",
        PermissionManagementView.as_view(),
        name="permission-management",
    ),
    path(
        "admin/permissions/<str:permission_id>/",
        PermissionManagementView.as_view(),
        name="permission-detail",
    ),
    path(
        "admin/users/<str:user_id>/role/",
        UserRoleAssignmentView.as_view(),
        name="assign-role",
    ),
    # ---------------------temp-------
    path("test/", Testing.as_view(), name="testing"),
    path("protected/", SomeView.as_view(), name="protected"),
]

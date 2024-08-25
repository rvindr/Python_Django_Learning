from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from bson import ObjectId
from datetime import datetime, timedelta
from user_management.mongo_client import logs_collection, users_collection


class UserModel(BaseModel):
    """
    A Pydantic User model representing a user with attributes for account management
    and role-based access control.
    """

    id: Optional[str] = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    email: str
    first_name: str
    last_name: str
    password: str
    is_active: bool = True  # Indicates if the user's account is active
    is_admin: bool = False  # Indicates if the user has admin privileges
    role_id: Optional[str] = None  # Optional field to store the user's role ID

    @property
    def is_authenticated(self):
        """
        Always return True as this method is used to indicate that the user is authenticated.
        """
        return True

    def log_activity(self, action: str, details: Optional[dict] = None):
        log_entry = {
            "user_id": self.id,
            "action": action,
            "timestamp": datetime.utcnow(),
            "details": details or {},
        }
        logs_collection.insert_one(log_entry)

    # New fields for login attempts and lockout
    failed_login_attempts: int = 0
    lockout_until: Optional[datetime] = None

    def is_locked_out(self) -> bool:
        """Check if the account is locked."""
        if self.lockout_until and datetime.utcnow() < self.lockout_until:
            return True
        return False

    def increment_failed_attempts(self):
        """Increment failed login attempts and lock the account if necessary."""
        self.failed_login_attempts += 1
        if self.failed_login_attempts >= 3:  # Lock after 3 failed attempts
            self.lockout_until = datetime.utcnow() + timedelta(
                minutes=1
            )  # Lock for 1 minutes
        users_collection.update_one(
            {"_id": self.id},
            {
                "$set": {
                    "failed_login_attempts": self.failed_login_attempts,
                    "lockout_until": self.lockout_until,
                }
            },
        )

    def reset_failed_attempts(self):
        """Reset failed login attempts and unlock the account."""
        self.failed_login_attempts = 0
        self.lockout_until = None
        users_collection.update_one(
            {"_id": self.id},
            {
                "$set": {
                    "failed_login_attempts": self.failed_login_attempts,
                    "lockout_until": self.lockout_until,
                }
            },
        )

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True

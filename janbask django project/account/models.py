from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from bson import ObjectId
from datetime import datetime, timedelta
from account.mongo_client import logs_collection, users_collection

from datetime import datetime, timedelta
from pydantic import BaseModel, Field
from bson import ObjectId


class UserModel(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    email: str
    first_name: str
    last_name: str
    password: str
    is_active: bool = True
    is_admin: bool = False
    role_id: Optional[str] = None


    @property
    def is_authenticated(self):
        return True
    
    def log_activity(self, action: str, details: Optional[dict] = None):
        log_entry = {
            "user_id": self.id,
            "action": action,
            "timestamp": datetime.utcnow(),
            "details": details or {}
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


# ---------------------Role and permission-------
class PermissionModel(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    name: str
    description: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True


class RoleModel(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    name: str
    permissions: List[str]  # List of permission IDs

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True

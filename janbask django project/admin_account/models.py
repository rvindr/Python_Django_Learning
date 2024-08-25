from pydantic import BaseModel, Field
from typing import Optional, List
from bson import ObjectId


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

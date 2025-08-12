from pydantic import BaseModel, EmailStr
from typing import List, Optional

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class ResourceAssign(BaseModel):
    user_id: int
    resource_name: str
    permissions: str 

class ResourcePermission(BaseModel):
    resource_name: str
    permissions: str 

class ApproveUserRequest(BaseModel):
    user_id: int
    role: str
    resources: List[ResourcePermission]
    approval_token: str 



class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(BaseModel):
    title: str
    content: str

class PostUpdate(BaseModel):
    title: str
    content: str

class PostResponse(PostCreate):
    id: int
    owner_id: int
    class Config:
        from_attributes = True


class CommentPostRequest(BaseModel):
    post_id: int
    content: str

class ManagePostRequest(BaseModel):
    post_id: int
    action: str

class EventCreate(BaseModel):
    title: str
    description: str

class PollCreate(BaseModel):
    question: str
    options: str

class ReactionPostRequest(BaseModel):
    post_id: int
    reaction_type: str

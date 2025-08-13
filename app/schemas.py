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


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class PostResponse(PostBase):
    id: int
    owner_id: int
    class Config:
        from_attributes = True



class CommentPostRequest(BaseModel):
    post_id: int
    content: str


class CommentUpdateRequest(BaseModel):
    content: str


class CommentResponse(BaseModel):
    id: int
    post_id: int
    user_id: int
    content: str
    class Config:
        from_attributes = True



class CommentCreate(CommentPostRequest):
    pass



class ManagePostRequest(BaseModel):
    post_id: int
    action: str


class ManagePostUpdate(BaseModel):
    action: str


class ManagePostResponse(BaseModel):
    id: int
    post_id: int
    user_id: int
    action: str
    class Config:
        from_attributes = True


class ManagePostCreate(ManagePostRequest):
    pass



class EventCreate(BaseModel):
    title: str
    description: Optional[str] = None


class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class EventResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    owner_id: int
    class Config:
        from_attributes = True



class PollCreate(BaseModel):
    question: str
    options: str


class PollUpdate(BaseModel):
    question: Optional[str] = None
    options: Optional[str] = None


class PollResponse(BaseModel):
    id: int
    question: str
    options: str
    owner_id: int
    class Config:
        from_attributes = True



class ReactionPostRequest(BaseModel):
    post_id: int
    reaction_type: str


class ReactionUpdateRequest(BaseModel):
    reaction_type: str


class ReactionResponse(BaseModel):
    id: int
    post_id: int
    user_id: int
    reaction_type: str
    class Config:
        from_attributes = True


class ReactionCreate(ReactionPostRequest):
    pass

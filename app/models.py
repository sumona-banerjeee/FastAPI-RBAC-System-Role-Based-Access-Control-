from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from .database import Base


class UserResource(Base):
    __tablename__ = "user_resources"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    resource_id = Column(Integer, ForeignKey("resources.id"))
    permissions = Column(String)  # e.g. CRUD, R, CU

    user = relationship("User", back_populates="user_resources")
    resource = relationship("Resource", back_populates="resource_users")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    is_active = Column(Boolean, default=False)  # Boolean instead of Integer

    user_resources = relationship("UserResource", back_populates="user")
    posts = relationship("Post", back_populates="owner")
    comments = relationship("Comment", back_populates="user")
    events = relationship("Event", back_populates="owner")
    polls = relationship("Poll", back_populates="owner")
    reactions = relationship("Reaction", back_populates="user")


class Resource(Base):
    __tablename__ = "resources"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    resource_users = relationship("UserResource", back_populates="resource")


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")
    reactions = relationship("Reaction", back_populates="post")


class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    content = Column(Text, nullable=False)

    post = relationship("Post", back_populates="comments")
    user = relationship("User", back_populates="comments")


class ManagePost(Base):
    __tablename__ = "manage_posts"
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    action = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))


class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="events")


class Poll(Base):
    __tablename__ = "polls"
    id = Column(Integer, primary_key=True)
    question = Column(String, nullable=False)
    options = Column(Text, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="polls")


class Reaction(Base):
    __tablename__ = "reactions"
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    reaction_type = Column(String, nullable=False)

    post = relationship("Post", back_populates="reactions")
    user = relationship("User", back_populates="reactions")

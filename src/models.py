from flask_sqlalchemy import SQLAlchemy
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Table, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

# Tabla de asociación para las etiquetas en las publicaciones
post_tags = Table('post_tags', Base.metadata,
    Column('post_id', Integer, ForeignKey('post.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tag.id'), primary_key=True)
)

# Clase Usuario
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(250), nullable=False)
    first_name = Column(String(80), nullable=True)
    last_name = Column(String(80), nullable=True)
    bio = Column(Text, nullable=True)
    profile_image_url = Column(String(250), nullable=True)
    created_at = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)
    
    # Relaciones
    posts = relationship("Post", back_populates="user")
    comments = relationship("Comment", back_populates="user")
    likes = relationship("Like", back_populates="user")
    followers = relationship("Follower", foreign_keys="Follower.followed_id", back_populates="followed")
    following = relationship("Follower", foreign_keys="Follower.follower_id", back_populates="follower")
    sent_messages = relationship("DirectMessage", foreign_keys="DirectMessage.sender_id", back_populates="sender")
    received_messages = relationship("DirectMessage", foreign_keys="DirectMessage.receiver_id", back_populates="receiver")

    def __repr__(self):
        return f'<User {self.username}>'

# Clase Publicación
class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    image_url = Column(String(250), nullable=False)
    caption = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False)
    location = Column(String(100), nullable=True)
    
    # Relaciones
    user = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")
    likes = relationship("Like", back_populates="post")
    tags = relationship("Tag", secondary=post_tags, back_populates="posts")
    
    def __repr__(self):
        return f'<Post {self.id}>'

# Clase Comentario
class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False)
    
    # Relaciones
    user = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")
    
    def __repr__(self):
        return f'<Comment {self.id}>'

# Clase Me gusta
class Like(Base):
    __tablename__ = 'like'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    created_at = Column(DateTime, nullable=False)
    
    # Relaciones
    user = relationship("User", back_populates="likes")
    post = relationship("Post", back_populates="likes")
    
    def __repr__(self):
        return f'<Like {self.id}>'

# Clase Seguidor
class Follower(Base):
    __tablename__ = 'follower'
    id = Column(Integer, primary_key=True)
    follower_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    followed_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    created_at = Column(DateTime, nullable=False)
    
    # Relaciones
    follower = relationship("User", foreign_keys=[follower_id], back_populates="following")
    followed = relationship("User", foreign_keys=[followed_id], back_populates="followers")
    
    def __repr__(self):
        return f'<Follower {self.id}>'

# Clase Etiqueta
class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    
    # Relaciones
    posts = relationship("Post", secondary=post_tags, back_populates="tags")
    
    def __repr__(self):
        return f'<Tag {self.name}>'

# Clase Mensaje Directo
class DirectMessage(Base):
    __tablename__ = 'direct_message'
    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    receiver_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False)
    is_read = Column(Boolean, default=False)
    
    # Relaciones
    sender = relationship("User", foreign_keys=[sender_id], back_populates="sent_messages")
    receiver = relationship("User", foreign_keys=[receiver_id], back_populates="received_messages")
    
    def __repr__(self):
        return f'<DirectMessage {self.id}>'

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem generating the diagram")
    print(e)
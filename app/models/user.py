from .db import db, environment, SCHEMA, add_prefix_for_prod
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.orm import reletionship
import datetime


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    hashed_password = db.Column(db.String(255), nullable=False)
    profile_pic = db.Column(db.String(255))
    created_at = db.Column(db.Date, default = datetime.datetime.now())
    updated_at = db.Column(db.Date, default = datetime.datetime.now())

    user_servers = db.relationship('Server', backref='owner',cascade="all, delete")

    server_members = db.relationship('ServerMember', backref='member')

    channel_members = db.relationship('ChannelMember', backref='member')

    channel_messages = db.relationship('ChannelMessage', backref='sender',cascade="all, delete")

    user_channels = db.relationship('Channel', backref='owner', cascade='all, delete')

    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):
        return {
        'id': self.id,
        'username': self.username,
        'email':self.email,
        'profilePic': self.profile_pic,
        'userServers': {server.id: server.to_alt_dict() for server in self.user_servers},
        'serverMembers': {member.id: member.to_dict() for member in self.server_members},
        'channelMembers': {room.id: room.channel.to_dict() for room in self.channel_members},
    }

    def to_resource_dict(self):
        return {
        'id': self.id,
        'username': self.username,
        'email':self.email,
        'profilePic': self.profile_pic,
    }

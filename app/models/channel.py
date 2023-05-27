from sqlalchemy.sql import func, expression
from sqlalchemy.orm import relationship

from sqlalchemy.orm import Session
from .db import db, environment, SCHEMA, add_prefix_for_prod

import datetime

class Channel(db.Model):
    '''
    RELETIONSHIPS:
    member from User Model
    server from Server Model
    '''
    __tablename__ = 'channels'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    server_id = db.Column(db.Integer, db.ForeignKey('servers.id'))
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    dm_channel = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.Date, default = datetime.datetime.now())
    updated_at = db.Column(db.Date, default = datetime.datetime.now())

    members = db.relationship('ChannelMember', backref='channel', cascade='all, delete-orphan')
    messages = db.relationship('ChannelMessage', backref='channel',cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'serverId': self.server_id,
            'members': {member.user_id: member.to_dict() for member in self.members},
            'messages': {message.id:message.to_dict() for message in self.messages},
            'dmChannel': self.dm_channel,
            'numOfMembers': len(self.members)
        }
    def to_socket_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'serverId': self.server_id,
            'dmChannel': self.dm_channel,
            'numOfMembers': len(self.members)
        }

class ChannelMember(db.Model):
    '''
    RELETIONSHIPS:
    member from User Model

    '''
    __tablename__ = 'channelMembers'

    id = db.Column(db.Integer, primary_key=True)
    channel_id = db.Column(db.Integer, db.ForeignKey('channels.id', passive_deletes=True), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.Date, default = datetime.datetime.now())
    updated_at = db.Column(db.Date, default = datetime.datetime.now())

    def to_dict(self):
        return {
            'id': self.id,
            'userId': self.user_id,
            'username':self.member.username,
            'channelId': self.channel_id,
            'profilePic': self.member.profile_pic,
        }


class ChannelMessage(db.Model):
    '''
    RELETIONSHIPS:
    sender from User Model

    '''
    __tablename__ = 'channelMessages'

    id = db.Column(db.Integer, primary_key=True)
    channel_id = db.Column(db.Integer, db.ForeignKey('channels.id'))
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.String(1500), nullable=False)
    picture = db.Column(db.String(2500))
    created_at = db.Column(db.Date, default = datetime.datetime.now())
    updated_at = db.Column(db.Date, default = datetime.datetime.now())

    def to_dict(self):
        return {
            'id': self.id,
            'serverId': self.channel.server_id,
            'senderId': self.sender_id,
            'senderUsername':self.sender.username,
            'senderProfilePic':self.sender.profile_pic,
            'channelId': self.channel_id,
            'content': self.content,
            'createdAt': self.created_at,
            'updatedAt': self.updated_at
        }
    def to_socket_dict(self):
        return {
            'id': self.id,
            'serverId': self.channel.server_id,
            'senderId': self.sender_id,
            'senderUsername':self.sender.username,
            'senderProfilePic':self.sender.profile_pic,
            'channelId': self.channel_id,
            'content': self.content,
        }

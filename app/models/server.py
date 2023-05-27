from .db import db, environment, SCHEMA, add_prefix_for_prod
from sqlalchemy.sql import func
import datetime

def find_general_chat_id (channels):
    for channel in channels:
        if channel.name == 'General Chat':
           return channel.id

class Server(db.Model):
    '''
    RELETIONSHIPS:
    owner from User Model
    '''
    __tablename__ = 'servers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), nullable=False)
    server_icon = db.Column(db.String(255))
    description = db.Column(db.String(255))
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.Date, default = datetime.datetime.now())
    updated_at = db.Column(db.Date, default = datetime.datetime.now())

    members = db.relationship('ServerMember', cascade='all, delete-orphan', backref='server')
    channels = db.relationship('Channel', backref='server', cascade="all,delete-orphan")


    def to_dict(self):
        return{
            'id': self.id,
            'name': self.name,
            'serverIcon': self.server_icon,
            'description': self.description,
            'ownerId': {'id':self.owner.id, 'username': self.owner.username},
            'channels': {channel.id: channel.to_dict() for channel in self.channels},
            'generalChatId': find_general_chat_id(self.channels),
            'members': {member.id: member.to_dict() for member in self.members},
            'numOfMembers': len(self.members),
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


    def to_socket_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'serverIcon': self.server_icon,
            'owner': {'id':self.owner.id, 'username': self.owner.username},
            'description': self.description,
            'membersLength': len(self.members),
        }

class ServerMember(db.Model):
    '''
    RELETIONSHIPS:
    member from User Model

    '''

    __tablename__ = 'serverMembers'

    id = db.Column(db.Integer, primary_key=True)
    server_id = db.Column(db.Integer, db.ForeignKey('servers.id', passive_deletes=True), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.Date, default = datetime.datetime.now())
    updated_at = db.Column(db.Date, default = datetime.datetime.now())

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.member.username,
            'memberId': self.member.id,
            'profilePic': self.member.profile_pic,
            'email': self.member.email,
            'serverId': self.server_id,
        }

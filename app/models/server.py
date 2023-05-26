from .db import db, environment, SCHEMA, add_prefix_for_prod
from sqlalchemy.sql import func
import datetime

def find_general_channel_id (channels):
    for channel in channels:
        if channel.name == 'Test':
           return channel.id

class Server(db.Model):
    __tablename__ = 'servers'

    id = db.Column(db.Integer, primary_key=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    icon = db.Column(db.String(255))
    name = db.Column(db.String(70), nullable=False)
    description = db.Column(db.String(255))
    created_at = db.Column(db.Date, default = datetime.datetime.now())
    updated_at = db.Column(db.Date, default = datetime.datetime.now())

    channels = db.relationship('Channel', backref='server', cascade="all,delete-orphan")

    members = db.relationship('ServerMember', cascade='all, delete-orphan', backref='server')

    def to_dict(self):
        return{
            'id': self.id,
            'serverOwner': {'id':self.owner.id, 'username': self.owner.username},
            'icon': self.icon,
            'name': self.name,
            'description': self.description,
            'channels': {channel.id: channel.to_dict() for channel in self.channels},
            'membership': {member.id: member.to_dict() for member in self.members},
            'generalChannelId': find_general_channel_id(self.channels),
            'numOfMembers': len(self.members),
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


    def to_alt_dict(self):
        return {
            'id': self.id,
            'owner': {'id':self.owner.id, 'username': self.owner.username},
            'icon': self.icon,
            'name': self.name,
            'description': self.description,
            'membersLength': len(self.members),
        }

class ServerMember(db.Model):
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
            'userId': self.member.id,
            'profilePic': self.member.profile_pic,
            'email': self.member.email,
            'serverId': self.server_id,
        }

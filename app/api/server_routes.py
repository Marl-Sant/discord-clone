# - need changes
from flask import Blueprint, jsonify, session, request
from flask_login import current_user, login_required
from app.models import User, Server, ServerMember, Channel, ChannelMessage, db
from .auth_routes import validation_errors_to_error_messages

servers_routes = Blueprint('servers', __name__)


# - all get routes for server
@servers_routes.route('')
@login_required
def get_all_servers():
    servers= db.session.query(Server).all()

    return {'servers':{server.id: server.to_dict() for server in servers}}

@servers_routes.route('/<int:id>')
@login_required
def get_a_server(id):
    server = Server.query.get(id)

    return server.to_dict()

# - creating a new server
@servers_routes.route('', methods=['POST'])
@login_required
def create_a_server():
    ## - 1 -creating the server with the data from the request form and 
    ## - using the currently logged in user
    ## - 2 -adding the currently logged in user as the first member 
    ## - of the created server
    ## - 3 -creating the first channel with the defaulted 
    ##- name of General Chat
    ## - 4 - creating the welcome message that is displayed on the General Chat
    ## - 5 -creating the welcome message that is displayed on the General Chat
    server = Server(owner_id=current_user.id, name=request.form['name'])
    db.session.add(server)
    db.session.commit()
    owner = ServerMember(server_id=server.id, user_id=server.owner_id)
    db.session.add(owner)
    db.session.commit()
    generalChat = Channel(name="General Chat", server_id=server.id)
    db.session.add(generalChat)
    db.session.commit()
    welcome_message = ChannelMessage(channel_id=generalChat.id, sender_id=current_user.id, content=f'Hey! Welcome to the {server.name} server')
    db.session.add(welcome_message)
    db.session.commit()

    return server.to_dict()

# - update a server
@servers_routes.route('/<int:id>', methods=['PUT'])
@login_required
def update_a_server(id):

    # - 1 - finding the server by the id we would like to update using the 
    # - integer in the url 
    # - 2 - grabbing the general chat associated with the found server and all 
    # - existing information for the record
    # - 3 - grabbing the welcome message on the General Chat of the server
    # - grabbing the name from the update form that we will be 
    #- 4 - takeing information from. this form will be prepopulated with the 
    # - current name of the server
    # - 5 -using the name from the form to provide the new welcome message
    # - 6 -renaming the server
    # - 7 -saving the new updated server
    server = Server.query.get(id)

    general_chat = Channel.query.get(server.channels[0].id)

    welcome_message = ChannelMessage.query.filter_by(channel_id=general_chat.id).filter_by(sender_id=current_user.id).first()

    name = request.form['name']

    welcome_message.content = f'Welcome to {name}\'s Server'

    server.name = request.form['name']

    db.session.commit()

    return server.to_dict()

# - delete a server
@servers_routes.route('/<int:id>', methods=['DELETE'])
@login_required
def delete_a_server(id):
    
    # - finding the server by the id we would like to delete using 
    # - the integer in the url then deleteing the selected server
    server = Server.query.get(id)

    db.session.delete(server)

    db.session.commit()
    return {'serverId': server.id}

## routes that deal with the server members

# - get server members
@servers_routes.route('/<int:id>/members')
@login_required
def get_server_members(id):

    server = Server.query.get(id)

    return {"serverMembers": {member.id: member.to_dict() for member in server.members}}

# - get a server member
@servers_routes.route('/members/<int:id>')
@login_required
def get_a_server_member(id):

    server_member = ServerMember.query.get(id)
    
    return {'serverMember': server_member.to_dict()}

# - add a new server member
@servers_routes.route('/<int:id>/members', methods=['POST'])
@login_required
def create_new_server_member(id):
    # - 1 - using the information in the request, we will be creating the 
    # - new member
    # - 2 - grabbing information about the user that will join the server
    # - adding that user to the server
    # - 3 - sending message on General Chat welcoming the new member
    server = Server.query.get(id)
    data = request.json

    

    new_member= User.query.get(data['userId'])

    added_member = ServerMember(server_id=id, user_id=data['userId'])

    db.session.add(added_member)

    general_chat = Channel.query.filter_by(server_id=data['serverId']).first()
    welcome_message = ChannelMessage(channel_id=general_chat.id,sender_id=server.owner_id,content=f'Everyone welcome {new_member.username} to the server!')
    db.session.add(welcome_message)
    db.session.commit()

    return {'member':added_member.to_dict(), 'server':server.to_dict()}

# - delete a servermember
@servers_routes.route('/<int:server_id>/members/<int:member_id>', methods=['DELETE'])
@login_required
def delete_a_server_member(server_id, member_id):

    # - find the server member that wants to leave and say goodbye
    server_member = ServerMember.query.get(member_id)
    db.session.delete(server_member)

    general_chat = Channel.query.filter_by(server_id=server_id).first()
    goodbye_message = ChannelMessage(channel_id=general_chat.id,sender_id=general_chat.server.owner_id,content=f'Everyone say goodbye to {server_member.member.username}!')
    db.session.add(goodbye_message)
    db.session.commit()
    
    return {'serverMemberId': server_member.id, 'serverId': general_chat.server.id}

# - get all server channels
@servers_routes.route('/<int:id>/channels')
def get_all_channels(id):

    # find all the channels associated with the server id passed in
    server_channels = Channel.query.filter_by(server_id = id).all()

    return {'channels': {channel.id: channel.to_socket_dict() for channel in server_channels}}

# - get a server channel
@servers_routes.route('/<int:server_id>/channels/<int:channel_id>')
def get_a_channel(server_id, channel_id):
    channel = Channel.query.get(channel_id)

    return channel.to_dict()

# -  create a server channel
@servers_routes.route('/<int:id>/channels', methods=["POST"])
def create_new_channel(id):
    # - 1 -grab the information from the request with new server info
    # - 2 -make a new channel with the information provided
    # - 3 -create a welcome message to the new channel
    data = request.json
    channel = Channel(name=data['name'], server_id=data['serverId'])
    db.session.add(channel)
    db.session.commit()

    welcome_message = ChannelMessage(channel_id=channel.id,sender_id=channel.server.owner_id,content=f'Welcome to {channel.server.name}\'s channel {channel.name}')
    db.session.add(welcome_message)
    db.session.commit()

    return channel.to_dict()

# - update a channel
@servers_routes.route('/<int:server_id>/channels/<int:channel_id>', methods=['PUT'])
def edit_a_channel(server_id, channel_id):
    # - 1 - grab the channel you would like to edit
    # - 2 - grab the information from the request with new server info
    channel = Channel.query.get(channel_id)

    data = request.json
    name = data['name']

    channel.name = name
    db.session.commit()
    return channel.to_dict()

@servers_routes.route('/<int:server_id>/channels/<int:channel_id>', methods=['DELETE'])
def delete_a_channel(server_id, channel_id):
    # grab the channel you would like to delete
    channel = Channel.query.get(channel_id)

    db.session.delete(channel)
    db.session.commit()
    return{'channelId': channel.id}

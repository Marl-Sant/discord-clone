from flask import Blueprint, jsonify, session, request
from flask_login import current_user, login_required
from app.models import User, Server, ServerMember, Channel, ChannelMessage, db
from .auth_routes import validation_errors_to_error_messages

servers_routes = Blueprint('servers', __name__)


# - getting all servers
@servers_routes.route('')
@login_required
def get_all_servers():
    servers= db.session.query(Server).all()

    return {'servers':{server.id: server.to_socket_dict() for server in servers}}

# - getting a server
@servers_routes.route('/<int:id>')
@login_required
def get_a_server(id):
    server = db.session.query(Server).get(id)

    return {"server": {server.id: server.to_dict()}}

# - creating a new server
@servers_routes.route('', methods=['POST'])
@login_required
def create_a_server():
    ## - creating the server with the data from the request form and using the currently logged in user
    server = Server(owner_id=current_user.id, name=request.form['name'])
    db.session.add(server)
    db.session.commit()

    ## - adding the currently logged in user as the first member of the created server
    owner = ServerMember(server_id=server.id, user_id=server.owner_id)
    db.session.add(owner)
    db.session.commit()

    ## - creating the first channel with the defaulted name of General Chat
    generalChat = Channel(name="General Chat", server_id=server.id)
    db.session.add(generalChat)
    db.session.commit()

    ## - creating the welcome message that is displayed on the General Chat
    welcome_message = ChannelMessage(channel_id=generalChat.id, sender_id=current_user.id, content=f'Hey! Welcome to the {server.name} server')
    db.session.add(welcome_message)
    db.session.commit()

    return server.to_dict()

# - update a server
@servers_routes.route('/<int:id>', methods=['PUT'])
@login_required
def update_a_server(id):

    # - finding the server by the id we would like to update using the integer in the url 
    server = Server.query.get(id)

    # - grabbing the general chat associated with the found server and all existing information for the record
    general_chat = Channel.query.get(server.channels[0].id)

    # - grabbing the welcome message on the General Chat of the server
    welcome_message = ChannelMessage.query.filter_by(channel_id=general_chat.id).filter_by(sender_id=current_user.id).first()

    # - grabbing the name from the update form that we will be takeing information from. this form will be prepopulated with the current name of the server
    name = request.form['name']

    # - using the name from the form to provide the new welcome message
    welcome_message.content = f'Welcome to {name}\'s Server'

    # - renaming the server
    server.name = request.form['name']

    # - saving the new updated server
    db.session.commit()

    return server.to_dict()

# - delete a server
@servers_routes.route('/<int:id>', methods=['DELETE'])
@login_required
def delete_a_server(id):
    
    # - finding the server by the id we would like to delete using the integer in the url 
    server = Server.query.get(id)

    # - deleteing the selected server
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

    server = Server.query.get(id)
    
    # - using the information in the request, we will be creating the new member
    data = request.json

    # - grabbing information about the user that will join the server
    new_member= User.query.get(data['userId'])

    # - adding that user to the server
    added_member = ServerMember(server_id=id, user_id=data['userId'])

    db.session.add(added_member)

    # - sending message on General Chat welcoming the new member
    general_chat = Channel.query.filter_by(server_id=id).first()
    welcome_message = ChannelMessage(channel_id=general_chat.id,sender_id=server.owner_id,content=f'Everyone welcome {new_member.username} to the server!')
    db.session.add(welcome_message)
    db.session.commit()

    return {'member':added_member.to_dict(), 'server':server.to_dict()}

# - delete a servermember
@servers_routes.route('/<int:server_id>/members/<int:member_id>', methods=['DELETE'])
@login_required
def delete_a_server_member(server_id, member_id):

    # - find the server member that wants to leave
    server_member = ServerMember.query.get(member_id)
    db.session.delete(server_member)

    # - bid the user adieu with a nice message
    general_chat = Channel.query.filter_by(server_id=server_id).first()
    goodbye_message = ChannelMessage(channel_id=general_chat.id,sender_id=general_chat.server.owner_id,content=f'Everyone say goodbye to {server_member.member.username}!')
    db.session.add(goodbye_message)
    db.session.commit()
    
    return {'serverMemberId': server_member.id, 'serverId': general_chat.server.id}

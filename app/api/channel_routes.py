from flask import Blueprint, jsonify, session, request
from flask_login import current_user, login_required
from app.models import User, Channel, ChannelMessage, ChannelMember, db
from .auth_routes import validation_errors_to_error_messages

channel_routes = Blueprint('channels', __name__, url_prefix='channels')

## THESE MAY NOT BE NECESSARY
# get one channel
@channel_routes.route('/<int:id>')
def get_a_channel(id):
    channel = Channel.query.get(id)
    return channel.to_dict()

#update a channel
@channel_routes.route('/<int:id>', methods=["PUT"])
def edit_a_channel(id):
    channel = Channel.query.get(id)

    # - grabbing the name from the update form that we will be takeing information from. this form will be prepopulated with the current name of the channel
    name = request.form['name']
    channel.name = name
    db.session.commit()

    return channel.to_dict()

# delete a channel
@channel_routes.route('/<int:id>', methods=["DELETE"])
def delete_a_channel(id):

    # - finding the server by the id we would like to delete using the integer in the url 
    channel = Channel.query.get(id)

    db.session.delete(channel)
    db.session.commit()

    return {'channelId': channel.id}

#the routes below is necessary

#posting a new message to a channel
@channel_routes.route('/<int:id>/messages', methods=['POST'])
def post_channel_message(id):
    #create a new message
    new_message = ChannelMessage(
        channel_id=id,
        sender_id=current_user.id,
        content=request.form['content']
    )
    db.session.add(new_message)
    db.session.commit()
    return new_message.to_dict()

#get all members on a channel
@channel_routes.route('/<int:id>/members')
def get_all_channel_members(id):
    #find the channel you would like to see the members of
    channel_members = ChannelMember.query.filter_by(channel_id=id).all()
    return {'channelMembers': {member.id:member.to_dict() for member in channel_members}}

#add a member to the channel
@channel_routes.route('/<int:id>/members', methods=['POST'])
def add_member_to_channel(id):

    channel = Channel.query.get(id)
    # - using the information in the request, we will be creating the new member
    data = request.json
    new_member = User.query.get(data['userId'])
    member = ChannelMember(channel_id=id, user_id=data['userId'])
    db.session.add(member)
    # - welcome the new member with a message
    welcome_message = ChannelMessage(channel_id=id, sender_id=channel.server.owner_id, content=f"Welcome {new_member.username} to the channel")
    db.session.add(welcome_message)
    db.session.commit()

    return {'member': member.to_dict(), 'channel': channel.to_dict()}

#delete a member from the channel
@channel_routes.route('/<int:channel_id>/members/<int:member_id>', methods=['DELETE'])
def delete_channel_member(channel_id, member_id):
    # find the channel the member belongs to
    channel = Channel.query.get(channel_id)
    # find the member that would like to leave
    channel_member = ChannelMember.query.get(member_id)
    db.session.delete(member)
    goodbye_message = ChannelMessage(channel_id=channel_id, sender_id=channel.server.owner_id, content=f"Goodbye {channel_member.member.username}!")
    db.session.add(goodbye_message)
    db.session.commit()
    return {'member': member.id, 'channelId': channel.id} 

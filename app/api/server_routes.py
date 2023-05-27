from flask import Blueprint, jsonify, session, request
from flask_login import current_user, login_required
from app.models import User, Server, ServerMember, Channel, ChannelMessage, db
from .auth_routes import validation_errors_to_error_messages

servers_routes = Blueprint('servers', __name__)


# ---- getting all servers
@servers_routes.route('/')
def get_all_servers():
    servers= db.session.query(Server).all()

    return {'servers':{server.id: server.to_socket_dict() for server in servers}}

# ---- creating a new server
@servers_routes.route('/', methods=['POST'])
def create_a_server():
    server = Server(owner_id=current_user.id, name=request.form['name'])
    db.session.add(server)
    db.session.commit()

    owner = ServerMember(server_id=server.id, user_id=server.owner_id)
    db.session.add(owner)

    generalChat = Channel(name="General Chat", server_id=server.id)
    db.session.add(channel)
    db.session.commit()

    welcome_message = ChannelMessage(channel_id=generalChat.id, sender_id=current_user.id, content=f'Hey! Welcome to the {server.name} server')
    db.session.add(welcome_message)
    db.session.commit()

    return server.to_dict()

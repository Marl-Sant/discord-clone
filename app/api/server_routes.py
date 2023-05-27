from flask import Blueprint, jsonify, session, request
from flask_login import current_user, login_required
from app.models import User, Server, ServerMember, Channel, ChannelMessage, db
from .auth_routes import validation_errors_to_error_messages

servers_routes = Blueprint('servers', __name__)


# ---- getting all servers
@servers_routes.route('/')
def get_all_servers():
    if request.method == 'GET':
        servers= db.session.query(Server).all()

        return {'servers':{server.id: server.to_resource_dict() for server in servers}}

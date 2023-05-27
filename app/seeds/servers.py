from app.models import db, Server, User, ServerMember, SCHEMA, environment
from sqlalchemy.sql import func, text
from sqlalchemy.sql.expression import func


def seed_servers():
    server1 = Server(
        name = 'Video Games',
        server_icon = 'TEST.jpg',
        description = 'Server about Video Games',
        owner_id = 1
    )
    server2 = Server(
        name = 'Movies',
        server_icon = 'TEST.jpg',
        description = 'Server about Movies',
        owner_id = 2
    )
    server3 = Server(
        name = 'General Server',
        server_icon = 'TEST.jpg',
        description = 'Server about Generals',
        owner_id = 3
    )

    db.session.add(server1)
    db.session.add(server2)
    db.session.add(server3)
    db.session.commit()

def seed_server_members():
    for i in range(1 ,3):
        for j in range(1, 6):
            members = ServerMember(
                user_id = j,
                server_id = i
            )
            db.session.add(members)
            db.session.commit()

    # for k in range(1, 5):
    #     random_user_id = db.session.query(User.id).order_by(func.random()).first()[0]
    #     seed_server = Server(
    #         name=f'Server {k}',
    #         created_by = random_user_id
    #     )
    #     db.session.add(seed_server)
    #     db.session.commit()

    #     member1 = ServerMember(
    #         user_id = 1,
    #         server_id = k
    #     )
    #     member2 = ServerMember(
    #         user_id = 2,
    #         server_id = k
    #     )
    #     member3 = ServerMember(
    #         user_id = 3,
    #         server_id = k
    #     )
    #     member4 = ServerMember(
    #         user_id = 4,
    #         server_id = k
    #     )
    #     member5 = ServerMember(
    #         user_id = 5,
    #         server_id = j
    #     )
    #     db.session.add(member1)
    #     db.session.add(member2)
    #     db.session.add(member3)
    #     db.session.add(member4)
    #     db.session.add(member5)
    #     db.session.commit()


def undo_servers():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.servers RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM servers"))

    db.session.commit()


def undo_server_members():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.serverMembers RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM serverMembers"))

    db.session.commit()

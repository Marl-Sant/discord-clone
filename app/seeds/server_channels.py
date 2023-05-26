import random
from app.models import db, Server, Channel, ChannelMessage, SCHEMA, environment
from sqlalchemy.sql import text, func

def seed_channels():
    channels = [
    {
        'name': 'Test',
        'server_id': 1
    },
    {
        'name': 'AppAcademy',
        'server_id': 1
    },
    {
        'name': 'projects',
        'server_id': 1
    },
    {
        'name': "General",
        'server_id': 2
    },
    {
        'name': 'The boys',
        'server_id': 2
    }
    ]
    for channel in channels:
        new_channel = Channel(name=channel['name'], server_id=channel['server_id'])
        db.session.add(new_channel)


def seed_dm():
    dms = [{'dm_channel':True, 'owner_id': 2}]
    for dm in dms:
        new_dm = Channel(owner_id=dm['owner_id'], dm_channel=dm['dm_channel'])
        db.session.add(new_dm)
        db.session.commit()

def seed_channel_messages():
    # i === channels
    for i in range(1, 2):
        channel = Channel.query.get(i)
        if channel.name == 'Test':
            message = ChannelMessage(channel_id=i, sender_id=1, content=f'Welcome to {channel.server.name}\'s Server')
            db.session.add(message)
        else:
            message = ChannelMessage(channel_id=i, sender_id=1, content=f'Welcome to {channel.server.name}\'s Channel {channel.name}')
            db.session.add(message)
        #  x === users
        for x in range(2, 4):
                # users 2-3 channels 1-3
            if x < 4 and i < 2:
                message = ChannelMessage(channel_id=i, sender_id=x, content='test')
                db.session.add(message)
                # users 9 - 13 channels 4-6
            # elif (x >= 9 and x < 14) and i <= 6 and i > 3:
            #     message = ChannelMessage(channel_id=i, sender_id=x, content='test')
            #     db.session.add(message)
            #     # users 13 - 18  channels 7-9
            # elif (x > 13 and x < 19) and i <= 9 and i > 6:
            #     message = ChannelMessage(channel_id=i, sender_id=x, content='test')
            #     db.session.add(message)

    db.session.add(channel)
    db.session.commit()

def undo_channels():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.channels RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM channels"))

    db.session.commit()

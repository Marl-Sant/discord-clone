import random
from app.models import db, Server, Channel, ChannelMessage, SCHEMA, environment
from sqlalchemy.sql import text, func

def seed_channels():
    # ---- creating channels for several servers ID 1 - 5
    channels = [
    {
        'name': 'General Chat',
        'server_id': 1
    },
    {
        'name': 'Video Games Channel',
        'server_id': 1
    },
    {
        'name': 'General Chat',
        'server_id': 2
    },
    {
        'name': "Comics Channel",
        'server_id': 2
    },
    {
        'name': 'General Chat',
        'server_id': 3
    }
    ]
    for channel in channels:
        new_channel = Channel(name=channel['name'], server_id=channel['server_id'])
        db.session.add(new_channel)


def seed_dm_channels():
    # --- creating dm channels IDs 6 - 8
    dms = [{'dm_channel':True, 'owner_id': 1}, {'dm_channel':True, 'owner_id': 2}, {'dm_channel':True, 'owner_id': 3}]
    for dm in dms:
        new_dm = Channel(owner_id=dm['owner_id'], dm_channel=dm['dm_channel'])
        print(new_dm, "!@#!##!##!#!#!#!@#@")
        db.session.add(new_dm)
        db.session.commit()

def seed_channel_messages():
    # i === channels
    for i in range(1, 8):
        channel = Channel.query.get(i)
        print(channel)
        if channel.name == 'General Chat':
            message = ChannelMessage(channel_id=i, sender_id=1, content=f'Welcome to {channel.server.name}\'s Server')
            db.session.add(message)
        elif channel.dm_channel == True:
            message = ChannelMessage(channel_id=i, sender_id=4, content=f'Welcome to Direct Messages Channel')
            db.session.add(message)
        else:
            message = ChannelMessage(channel_id=i, sender_id=2, content=f'Welcome to {channel.server.name}\'s Channel {channel.name}')
            db.session.add(message)

    db.session.add(channel)
    db.session.commit()

def undo_channels():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.channels RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM channels"))

    db.session.commit()

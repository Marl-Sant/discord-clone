from app.models import db, Server, ChannelMember, SCHEMA, environment
from sqlalchemy.sql import text

def seed_channel_members():
    member1 = ChannelMember(
        user_id = 1, channel_id = 1
    )
    member2 = ChannelMember(
        user_id = 2, channel_id = 1
    )
    member3 = ChannelMember(
        user_id = 1, channel_id = 2
    )
    member4 = ChannelMember(
        user_id = 2, channel_id = 1
    )
    member5 = ChannelMember(
        user_id = 1, channel_id = 2
    )

    db.session.add(member1)
    db.session.add(member2)
    db.session.add(member3)
    db.session.add(member4)
    db.session.add(member5)
    db.session.commit()

def undo_channel_members():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.channelMembers RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM channelMembers"))

    db.session.commit()

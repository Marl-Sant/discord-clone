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
        user_id = 3, channel_id = 2
    )
    member5 = ChannelMember(
        user_id = 1, channel_id = 3
    )
    member6 = ChannelMember(
        user_id = 3, channel_id = 3
    )
    member6 = ChannelMember(
        user_id = 4, channel_id = 3
    )
    member7 = ChannelMember(
        user_id = 1, channel_id = 6
    )
    member8 = ChannelMember(
        user_id = 5, channel_id = 6
    )
    member9 = ChannelMember(
        user_id = 6, channel_id = 6
    )
    member10 = ChannelMember(
        user_id = 1, channel_id = 7
    )
    member11 = ChannelMember(
        user_id = 4, channel_id = 7
    )

    db.session.add(member1)
    db.session.add(member2)
    db.session.add(member3)
    db.session.add(member4)
    db.session.add(member5)
    db.session.add(member6)
    db.session.add(member7)
    db.session.add(member8)
    db.session.add(member9)
    db.session.add(member10)
    db.session.add(member11)
    db.session.commit()

def undo_channel_members():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.channelMembers RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM channelMembers"))

    db.session.commit()

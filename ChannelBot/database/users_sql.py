import ast
from sqlalchemy import Column, BigInteger, String
from ChannelBot.database import BASE, SESSION


class Users(BASE):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}
    user_id = Column(BigInteger, primary_key=True)
    channels = Column(String, nullable=True)

    def __init__(self, user_id, channels=None):
        self.user_id = user_id
        self.channels = channels


Users.__table__.create(checkfirst=True)


async def num_users():
    try:
        return SESSION.query(Users).count()
    finally:
        SESSION.close()


async def add_channel(user_id, channel_id):
    q: Users = SESSION.query(Users).get(user_id)
    if q:
        if q.channels:
            channels = list(set(ast.literal_eval(q.channels)))
            channels.append(channel_id)
            q.channels = str(channels)
        else:
            q.channels = str([channel_id])
    else:
        SESSION.add(Users(user_id))
    SESSION.commit()


async def remove_channel(user_id, channel_id):
    q = SESSION.query(Users).get(user_id)
    if q:
        channels = list(set(ast.literal_eval(q.channels)))
        if q.channels and channel_id in channels:
            channels.remove(channel_id)
            if len(channels) == 0:
                q.channels = None
            else:
                q.channels = str(channels)
    else:
        SESSION.add(Users(user_id))
    SESSION.commit()


async def get_channels(user_id):
    q = SESSION.query(Users).get(user_id)
    if q:
        if q.channels:
            # literal_eval() makes sure that the items remain of their type (here int).
            # While list() will make items str.
            channels = ast.literal_eval(q.channels)
            SESSION.close()
            return True, channels
        else:
            return False, []
    else:
        SESSION.add(Users(user_id))
        SESSION.commit()
        return False, []

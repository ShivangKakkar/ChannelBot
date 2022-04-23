from sqlalchemy import Column, String, Boolean, BigInteger
from ChannelBot.database import BASE, SESSION


class Channel(BASE):
    __tablename__ = "channels"
    __table_args__ = {'extend_existing': True}
    channel_id = Column(BigInteger, primary_key=True)
    admin_id = Column(BigInteger)
    caption = Column(String, nullable=True)
    buttons = Column(String, nullable=True)
    position = Column(String, nullable=True)
    sticker_id = Column(String, nullable=True)
    edit_mode = Column(String, nullable=True)
    webpage_preview = Column(Boolean)

    def __init__(self, channel_id, admin_id, caption=None, buttons=None, edit_mode=None, position=None, webpage_preview=False, sticker_id=None):
        self.channel_id = channel_id
        self.admin_id = admin_id
        self.caption = caption
        self.buttons = buttons
        self.position = position
        self.webpage_preview = webpage_preview
        self.sticker_id = sticker_id
        self.edit_mode = edit_mode


Channel.__table__.create(checkfirst=True)


async def num_channels():
    try:
        return SESSION.query(Channel).count()
    finally:
        SESSION.close()


async def add_channel(channel_id, user_id):
    q = SESSION.query(Channel).get(channel_id)
    if not q:
        SESSION.add(Channel(channel_id, user_id))
        SESSION.commit()
    else:
        SESSION.close()


async def remove_channel(channel_id):
    q = SESSION.query(Channel).get(channel_id)
    if q:
        SESSION.delete(q)
        SESSION.commit()
    else:
        SESSION.close()


async def get_channel_info(channel_id):
    q = SESSION.query(Channel).get(channel_id)
    if q:
        info = {
            'admin_id': q.admin_id,
            'buttons': q.buttons,
            'caption': q.caption,
            'position': q.position,
            'sticker_id': q.sticker_id,
            'webpage_preview': q.webpage_preview,
            'edit_mode': q.edit_mode
        }
        SESSION.close()
        return True, info
    else:
        SESSION.close()
        return False, {}


async def set_caption(channel_id, caption):
    q = SESSION.query(Channel).get(channel_id)
    if q:
        q.caption = caption
        SESSION.commit()
        return True
    else:
        SESSION.close()
        return False


async def get_caption(channel_id):
    q = SESSION.query(Channel).get(channel_id)
    if q and q.caption:
        caption = q.caption
        SESSION.close()
        return caption
    else:
        SESSION.close()
        return ''


async def set_buttons(channel_id, buttons):
    q = SESSION.query(Channel).get(channel_id)
    if q:
        q.buttons = buttons
        SESSION.commit()
        return True
    else:
        SESSION.close()
        return False


async def get_buttons(channel_id):
    q = SESSION.query(Channel).get(channel_id)
    if q and q.buttons:
        buttons = q.buttons
        SESSION.close()
        return buttons
    else:
        SESSION.close()
        return None


async def set_position(channel_id, position):
    q = SESSION.query(Channel).get(channel_id)
    if q:
        q.position = position
        SESSION.commit()
        return True
    else:
        SESSION.close()
        return False


async def get_position(channel_id):
    q = SESSION.query(Channel).get(channel_id)
    if q and q.position:
        position = q.position
        SESSION.close()
        return position
    else:
        SESSION.close()
        return 'below'


async def set_sticker(channel_id, sticker):
    q = SESSION.query(Channel).get(channel_id)
    if q:
        q.sticker_id = sticker
        SESSION.commit()
        return True
    else:
        SESSION.close()
        return False


async def get_sticker(channel_id):
    q = SESSION.query(Channel).get(channel_id)
    if q and q.sticker_id:
        sticker = q.sticker_id
        SESSION.close()
        return sticker
    else:
        SESSION.close()


async def toggle_webpage_preview(channel_id, value):
    q = SESSION.query(Channel).get(channel_id)
    if q:
        # print(value)
        if value:
            q.webpage_preview = True
        else:
            q.webpage_preview = False
        # print(q.webpage_preview)
        SESSION.commit()
        return True
    else:
        SESSION.close()
        return False


async def get_webpage_preview(channel_id):
    q = SESSION.query(Channel).get(channel_id)
    if q and q.webpage_preview:
        SESSION.close()
        return True
    else:
        SESSION.close()
        return False


async def set_edit_mode(channel_id, edit_mode):
    q = SESSION.query(Channel).get(channel_id)
    if q:
        q.edit_mode = edit_mode
        SESSION.commit()
        return True
    else:
        SESSION.close()
        return False


async def get_edit_mode(channel_id):
    q = SESSION.query(Channel).get(channel_id)
    if q and q.edit_mode:
        edit_mode = q.edit_mode
        SESSION.close()
        return edit_mode
    else:
        SESSION.close()
        return 'media'

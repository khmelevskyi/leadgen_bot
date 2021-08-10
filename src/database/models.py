from sqlalchemy import Column, ForeignKey, MetaData
from sqlalchemy import BigInteger, Integer, String, Boolean, DateTime, Date
from sqlalchemy.dialects.postgresql import JSONB


from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from datetime import datetime, time, timedelta
from typing import Any
import pytz
from enum import Enum

meta = MetaData(  # automatically name constraints to simplify migrations
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)
# Any saves from mypy checks of a dynamic class
Base: Any = declarative_base(metadata=meta)


def local_time() -> datetime:
    """ time in Ukraine """
    kiev_tz = pytz.timezone("Europe/Kiev")
    current_time = datetime.now(tz=kiev_tz)
    return current_time

class User(Base):
    __tablename__ = "user"

    chat_id = Column(BigInteger, primary_key=True)
    is_banned = Column(Boolean, default=False)
    username = Column(String(35))  # Telegram allows username no longer then 32
    first_name = Column(String)  # first name is unlimited
    last_name = Column(String)
    time_registered = Column(DateTime(timezone=True), default=local_time)

    def __repr__(self):
        return "<User(chat_id='{}', username='{}', is_banned='{}', university='{}')>".format(
            self.chat_id, self.username, self.is_banned
        )


class Admin(Base):
    __tablename__ = "admin"

    chat_id = Column(BigInteger, ForeignKey("user.chat_id"), primary_key=True)

    user = relationship("User", backref="admin", foreign_keys=[chat_id])

    def __repr__(self):
        return "<Admin(chat_id='{}')>".format(
            self.chat_id
        )


class UserStat(Base):
    __tablename__ = "user_stat"

    id = Column(Integer, primary_key=True)
    leadgen_id = Column(Integer, ForeignKey("user.chat_id"))
    connects = Column(Integer)
    calls = Column(Integer)
    ban = Column(Boolean)
    work = Column(Boolean)
    added_at = Column(Date)

    leadgen = relationship("User", backref="stat_leadgen", foreign_keys=[leadgen_id])

    def __repr__(self):
        return "<UserStat(id='{}', connects='{}', calls='{}', ban='{}', work='{}', added_at='{}')>".format(
            self.id, self.connects, self.calls, self.ban, self.work, self.added_at
        )


class Calls(Base):
    __tablename__ = "calls"

    id = Column(Integer, primary_key=True)
    planned_at = Column(DateTime(timezone=True), default=local_time)
    linkedin = Column(String)
    leadgen_id = Column(Integer, ForeignKey("user.chat_id"))

    leadgen = relationship("User", backref="call_leadgen", foreign_keys=[leadgen_id])

    def __repr__(self):
        return "<Group(id='{}', planned at='{}')>".format(
            self.id, self.planned_at
        )

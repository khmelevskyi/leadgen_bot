from sqlalchemy import Column, ForeignKey, MetaData
from sqlalchemy import BigInteger, Integer, String, Boolean, DateTime, Date, Time
from sqlalchemy.dialects.postgresql import JSONB

from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

import datetime
from typing import Any
import pytz
from enum import Enum

from ..data import TIME_ZONE

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


def local_time() -> datetime.datetime:
    """ time in Ukraine """
    kiev_tz = pytz.timezone("Europe/Kiev")
    current_time = datetime.datetime.now(tz=kiev_tz)
    return current_time

class User(Base):
    __tablename__ = "user"

    chat_id = Column(BigInteger, primary_key=True)
    is_banned = Column(Boolean, default=False, nullable=False)
    username = Column(String(35))  # Telegram allows username no longer then 32
    first_name = Column(String)  # first name is unlimited
    last_name = Column(String)
    time_registered = Column(DateTime(timezone=True), default=local_time)
    is_admin = Column(Boolean, default=False, nullable=False)
    reminder_time = Column(Time, default=datetime.time(hour=21, tzinfo=TIME_ZONE))

    def __repr__(self):
        return "<User(chat_id='{}', username='{}', is_banned='{}')>".format(
            self.chat_id, self.username, self.is_banned
        )


class Admin(Base):
    __tablename__ = "admin"

    chat_id = Column(BigInteger, ForeignKey("user.chat_id"), primary_key=True)
    role = Column(String)  # superadmin, sales

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
    deals = Column(Integer)
    earned = Column(Integer)
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
        return "<Calls(id='{}', planned at='{}')>".format(
            self.id, self.planned_at
        )

class Deals(Base):
    __tablename__ = "deals"

    id = Column(Integer, primary_key=True)
    linkedin = Column(String)
    leadgen_id = Column(Integer, ForeignKey("user.chat_id"))

    leadgen = relationship("User", backref="deal_leadgen", foreign_keys=[leadgen_id])

    def __repr__(self):
        return "<Deals(id='{}', leadgen_id='{}')>".format(
            self.id, self.leadgen_id
        )

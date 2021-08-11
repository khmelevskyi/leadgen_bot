""" session genation """
import pandas as pd
from functools import wraps
from os import link

from .base import Session

""" busines logic database access """
import datetime
from typing import Dict
from typing import List
from typing import Set
from typing import Tuple

from .models import Admin, Calls, User, UserStat

from .base import pg_session


def local_session(function):
    """ build and close local session """

    @wraps(function)
    def wrapped(self, *args, **kwargs):
        session = Session()
        try:
            result = function(self, session, *args, **kwargs)
        except Exception as error:
            # in case commit wan't be rolled back next trasaction failed
            session.rollback()
            raise ValueError(error) from error  # notify developer

        session.close()
        return result

    return wrapped



class DBSession():
    """ db function with renewadle session for each func """

    def __init__(self):
        self.admins = self.get_admins()

    @local_session
    def get_admins(self, session) -> None:
        admins = session.query(Admin.chat_id).all()

        return admins
    

    @local_session
    def add_user(self, session, user_data: Dict) -> User:
        """
        Create user record if not exist, otherwise update username
        """
        chat_id = user_data["chat_id"]
        username = user_data["username"]
        first_name = user_data["first_name"]
        last_name = user_data["last_name"]
        time_registered = user_data["time_registered"]

        user = session.query(User).get(chat_id)
        if user:
            if user.username != username:
                user.username = username
                session.commit()
            if user.is_banned is True:
                user.is_banned = False
                session.commit()
            return user

        new_user = User(
            chat_id=chat_id,
            is_banned=False,
            username=username,
            first_name=first_name,
            last_name = last_name,
            time_registered = time_registered
        )
        session.add(new_user)
        session.commit()
        return new_user

    @local_session
    def add_call(self, session, call_data: Dict) -> Calls:
        """
        Create user record if not exist, otherwise update username
        """
        planned_at = call_data["new_call_datetime"]
        linkedin = call_data["new_call_link"]
        leadgen_id = call_data["chat_id"]

        new_call = Calls(
            planned_at = planned_at,
            linkedin = linkedin,
            leadgen_id = leadgen_id
        )
        session.add(new_call)
        session.commit()
        return new_call

    @local_session
    def get_calls_list(self, session, date=None) -> List:
        """ list all users in database """

        if date == None:
            calls = session.query(
                Calls.id,
                Calls.planned_at,
                Calls.linkedin,
                Calls.leadgen_id
            ).all()
        else:
            calls = session.query(
                Calls.id,
                Calls.planned_at,
                Calls.linkedin,
                Calls.leadgen_id
            ).filter(Calls.planned_at.date()==date).all()
        return calls

    @local_session
    def call_done(self, session, call):
        old_call = session.query(Calls).get(call.id)
        leadgen_stat = session.query(UserStat).filter(
            UserStat.leadgen_id==call.leadgen_id,
            UserStat.added_at==datetime.date.today()
        ).first()
        if leadgen_stat:
            leadgen_stat.calls += 1
        else:
            leadgen_stat = session.query(UserStat).filter(
                UserStat.leadgen_id==call.leadgen_id,
                UserStat.added_at==datetime.date.today() - datetime.timedelta(1)
            ).first()
            leadgen_stat.calls += 1
        session.delete(old_call)
        session.commit()

    @local_session
    def delete_call(self, session, call):
        old_call = session.query(Calls).get(call.id)
        session.delete(old_call)
        session.commit()

    @local_session
    def add_user_stat(self, session, leadgen_data):
        leadgen_id = leadgen_data["leadgen_id"]
        connects = leadgen_data["connects"]
        ban = leadgen_data["ban"]
        work = leadgen_data["work"]
        added_at = leadgen_data["added_at"]

        new_user_stat = UserStat(
            leadgen_id=leadgen_id,
            connects=connects,
            calls = 0,
            ban=ban,
            work=work,
            added_at=added_at
        )
        session.add(new_user_stat)
        session.commit()
        return new_user_stat

    @local_session
    def get_user_stat(self, session, chat_id, date):
        user_stat = session.query(
            UserStat.id,
            UserStat.leadgen_id,
            UserStat.connects,
            UserStat.calls,
            UserStat.ban,
            UserStat.work,
            UserStat.added_at,
            ).filter(
            UserStat.leadgen_id==chat_id,
            UserStat.added_at==date).all()
        return user_stat

    @local_session
    def change_user_stat_connects(self, session, chat_id, date, new_connects):
        user_stat = session.query(UserStat).filter(
            UserStat.leadgen_id==chat_id,
            UserStat.added_at==date
        ).first()
        user_stat.connects = new_connects
        session.commit()

    @local_session
    def ban_user(self, session, chat_id: int) -> None:
        """ user banned the bot """

        user = session.query(User).get(chat_id)
        if user and user.is_banned is False:
            user.is_banned = True
            session.commit()

    @local_session
    def unban_user(self, session, chat_id: int) -> None:
        """ user started conversation after ban """

        user = session.query(User).get(chat_id)
        if user.is_banned is True:
            user.is_banned = False
            session.commit()


    @local_session
    def get_user_data(self, session, chat_id: int) -> Tuple[int, dict]:
        """ return universi_id and user date for engine.API call """
        university_id, user_data = (
            session.query(User.university_id, User.user_data)
            .filter(User.chat_id == chat_id)
            .first()
        )
        return (university_id, user_data)

    @local_session
    def count_users(self, session) -> int:
        """ number of users in our db """

        users_quantity = session.query(User).count()
        return users_quantity

    @local_session
    def get_users_list(self, session):
        """ list all users in database """

        users = session.query(User.chat_id).all()
        return users

    @local_session
    def delete_from_group(self, session, chat_id: int) -> None:
        """ deleting from group table """
        group = session.query(User).get(chat_id)
        if group:
            session.delete(group)
            session.commit()


    @local_session
    def get_stats(self, session):
        df = pd.read_sql(session.query(Calls).statement, session.bind)
        print(df)


db_session: DBSession = DBSession()



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
        self.admins = self.get_admins(["superadmin", "leadgen", "sales"])

    @local_session
    def get_admins(self, session, role_list) -> None:
        admins = (
            session.query(Admin.chat_id)
            .filter(Admin.role.in_(role_list))
            .all()
        )

        return admins

#### User.is_admin defines whether to count user in general leadgen list
    @local_session
    def make_admin(self, session, chat_id, role) -> None:

        if role == "superadmin" or role == "sales":
            user = session.query(User).get(chat_id)
            user.is_admin = True  # not count as leadgen
            session.commit()
        elif role == "leadgen":
            user = session.query(User).get(chat_id)
            user.is_admin = False  # count as leadgen
            session.commit()
        
        admin = session.query(Admin).get(chat_id)

        if admin:
            admin.role = role
            session.commit()
            return admin
        
        new_admin = Admin(
            chat_id=chat_id,
            role=role
        )
        session.add(new_admin)
        session.commit()

        return new_admin    

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
        is_admin = False

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
            time_registered = time_registered,
            is_admin = is_admin
        )
        session.add(new_user)
        session.commit()
        return new_user

    @local_session
    def delete_user(self, session, chat_id):
        old_user = session.query(User).get(chat_id)

        session.query(Admin).filter(Admin.chat_id==old_user.chat_id).delete(synchronize_session=False)
        session.query(UserStat).filter(UserStat.leadgen_id==old_user.chat_id).delete(synchronize_session=False)
        session.query(Calls).filter(Calls.leadgen_id==old_user.chat_id).delete(synchronize_session=False)

        session.delete(old_user)
        session.commit()

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
            self.create_user_stat(
                call.leadgen_id,
                datetime.date.today()
            )
            return self.call_done(call)
        session.delete(old_call)
        session.commit()

    @local_session
    def delete_call(self, session, call):
        old_call = session.query(Calls).get(call.id)
        session.delete(old_call)
        session.commit()

    @local_session
    def create_user_stat(self, session, user_id, date):
        leadgen_stat = session.query(UserStat).filter(
            UserStat.leadgen_id==user_id,
            UserStat.added_at==date
        ).first()

        if leadgen_stat:
            pass
        else:
            new_stat = UserStat(
                leadgen_id = user_id,
                connects = None,
                calls = 0,
                ban = None,
                work = None,
                added_at = date
            )
            session.add(new_stat)
        session.commit()

    @local_session
    def add_user_stat(self, session, leadgen_data):
        leadgen_id = leadgen_data["leadgen_id"]
        connects = leadgen_data["connects"]
        ban = leadgen_data["ban"]
        work = leadgen_data["work"]
        added_at = leadgen_data["added_at"]

        leadgen_stat = session.query(UserStat).filter(
            UserStat.leadgen_id==leadgen_id,
            UserStat.added_at==added_at
        ).first()

        if leadgen_stat:
            leadgen_stat.connects = connects
            leadgen_stat.ban = ban
            leadgen_stat.work = work
        else:
            new_stat = UserStat(
            leadgen_id = leadgen_id,
            connects = connects,
            calls = 0,
            ban = ban,
            work = work,
            added_at = added_at
            )
            session.add(new_stat)
        session.commit()

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
    def check_who_answered(self, session, user_id, date):
        leadgen_stat = session.query(UserStat).filter(
            UserStat.leadgen_id==user_id,
            UserStat.added_at==date
        ).first()

        if leadgen_stat and leadgen_stat.connects != None:
            return True
        else:
            return False

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
    def get_users_name(self, session) -> Tuple[int, str, str]:
        """ return universi_id and user date for engine.API call """
        users = (
            session.query(User.chat_id, User.first_name, User.last_name)
            .filter(User.is_admin==False)
            .all()
        )
        return users

    @local_session
    def get_users_admins_name(self, session) -> Tuple[int, str, str]:
        """ return universi_id and user date for engine.API call """
        users = (
            session.query(User.chat_id, User.first_name, User.last_name)
            .all()
        )
        return users

    @local_session
    def count_users(self, session) -> int:
        """ number of users in our db """

        users_quantity = session.query(User).count()
        return users_quantity

    @local_session
    def get_users_list(self, session):
        """ list all users in database """

        users = session.query(User.chat_id).filter(User.is_admin==False).all()
        return users

    @local_session
    def get_users_list_full(self, session):
        """ list all users in database """

        users = session.query(
            User.chat_id,
            User.is_banned,
            User.username,
            User.first_name,
            User.last_name,
            User.time_registered
            ).filter(User.is_admin==False).all()
        return users

    @local_session
    def get_users_admins_list(self, session):
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
    def get_stats(self, session, leadgen_id=None):
        if leadgen_id == None:
            df = pd.read_sql(session.query(UserStat).statement, session.bind)
        else:
            df = pd.read_sql(session.query(UserStat).filter(UserStat.leadgen_id==leadgen_id).statement, session.bind)
        # print(df)
        df_res = {}

        # print(df_res)
        self.created_dict(df_res, "overall", df)

        today_df = df[pd.to_datetime(df['added_at'], errors = 'coerce', format = '%Y-%m-%d').dt.day == datetime.date.today().day]
        self.created_dict(df_res, "today", today_df)

        ystrdy_df = df[pd.to_datetime(df['added_at'], errors = 'coerce', format = '%Y-%m-%d').dt.day == datetime.date.today().day-1]
        self.created_dict(df_res, "ystrdy", ystrdy_df)

        this_week_df = df[pd.to_datetime(df['added_at'], errors = 'coerce', format = '%Y-%m-%d').dt.isocalendar().week == datetime.date.today().isocalendar()[1]]
        self.created_dict(df_res, "this_week", this_week_df)

        last_week_df = df[pd.to_datetime(df['added_at'], errors = 'coerce', format = '%Y-%m-%d').dt.isocalendar().week == datetime.date.today().isocalendar()[1]-1]
        self.created_dict(df_res, "last_week", last_week_df)

        this_month_df = df[pd.to_datetime(df['added_at'], errors = 'coerce', format = '%Y-%m-%d').dt.month == datetime.date.today().month]
        self.created_dict(df_res, "this_month", this_month_df)

        last_month_df = df[pd.to_datetime(df['added_at'], errors = 'coerce', format = '%Y-%m-%d').dt.month == datetime.date.today().month-1]
        self.created_dict(df_res, "last_month", last_month_df)

        year_df = df[pd.to_datetime(df['added_at'], errors = 'coerce', format = '%Y-%m-%d').dt.year == datetime.date.today().year]
        self.created_dict(df_res, "year", year_df)

        return df_res

    def created_dict(self, df_res, date, df):
        dict_date = {}
        dict_date["connects"] = df["connects"].sum()
        dict_date["calls"] = df["calls"].sum()
        if date=="today" or date=="ystrdy":
            try:
                dict_date["is_ban"] = df["ban"].values[0]
                dict_date["is_work"] = df["work"].values[0]
            except:
                dict_date["is_ban"] = None
                dict_date["is_work"] = None
        else:
            dict_date["days_ban"] = df[df["ban"] == True]["ban"].count()
            dict_date["days_not_ban"] = df[df["ban"] == False]["ban"].count()
            dict_date["days_work"] = df[df["work"] == True]["work"].count()
            dict_date["days_not_work"] = df[df["work"] == False]["work"].count()

        df_res[date] = dict_date


         



db_session: DBSession = DBSession()



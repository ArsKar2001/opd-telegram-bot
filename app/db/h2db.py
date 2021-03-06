import sqlite3
from sqlite3 import Connection

import models


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class DB:
    connect: Connection
    url: str

    def __init__(self, url):
        self.url = url
        self.connectdb(url)

    def get_faculties(self):
        result = []
        self.connectdb(self.url)
        try:
            cursor = self.connect.cursor()
            cursor.execute('SELECT * FROM faculty')
            result = cursor.fetchall()
        except sqlite3.DatabaseError as e:
            print('Error: ', e)
        finally:
            self.connect.close()

        return result

    def get_groups(self):
        result = []
        self.connectdb(self.url)

        try:
            cursor = self.connect.cursor()
            cursor.execute('SELECT * FROM "group"')
            result = cursor.fetchall()
        except sqlite3.DatabaseError as e:
            print('Error: ', e)
        finally:
            self.connect.close()
        return result

    def upset_user(self, user):
        self.connectdb(self.url)
        get_user = self.get_user(user)
        if get_user is not None:
            user = self.update_user(user)
        else:
            user = self.user_insert(user)
        self.connect.close()
        return user

    def user_insert(self, user):
        try:
            cursor = self.connect.cursor()
            cursor.execute('INSERT INTO user(chat_id) VALUES (:chat_id)', {"chat_id": user.chat_id})
            self.connect.commit()
            return self.get_user(user)
        except sqlite3.DatabaseError as e:
            print('Error: ', e)

    def find_groups_by_faculty_id(self, faculty_id):
        r = []
        try:
            self.connectdb(self.url)
            cursor = self.connect.cursor()
            cursor.execute('SELECT * FROM "group" g WHERE g.faculty_id = :faculty_id', {'faculty_id': faculty_id})
            r = cursor.fetchall()
        except sqlite3.DatabaseError as e:
            print('Error: ', e)
        finally:
            self.connect.close()
        return r

    def get_user(self, user):
        try:
            cursor = self.connect.cursor()
            cursor.execute('SELECT * FROM user u WHERE u.chat_id = :chat_id', {"chat_id": user.chat_id})
            return cursor.fetchone()
        except sqlite3.DatabaseError as e:
            print('Error: ', e)
        return None

    def connectdb(self, url):
        self.connect = sqlite3.connect(url)
        self.connect.row_factory = dict_factory

    def is_group_id(self, param):
        result = False
        try:
            self.connectdb(self.url)
            cursor = self.connect.cursor()
            cursor.execute('SELECT * FROM "group" g WHERE g.id = :id', {'id': param})
            result = cursor.fetchone() is not None
        except sqlite3.DatabaseError as e:
            print('Error: ', e)
        finally:
            self.connect.close()
        return result

    def is_faculty_id(self, param):
        result = False
        try:
            self.connectdb(self.url)
            cursor = self.connect.cursor()
            cursor.execute('SELECT * FROM faculty g WHERE g.id = :id', {'id': param})
            result = cursor.fetchone() is not None
        except sqlite3.DatabaseError as e:
            print('Error: ', e)
        finally:
            self.connect.close()
        return result

    def find_students(self, group_id):
        result = []
        try:
            self.connectdb(self.url)
            cursor = self.connect.cursor()
            cursor.execute('SELECT * FROM student s WHERE s.group_id = :group_id', {'group_id': group_id})
            result = cursor.fetchall()
        except sqlite3.DatabaseError as e:
            print('Error: ', e)
        finally:
            self.connect.close()
        return result

    def is_auth_user(self, chat_id):
        result = False
        try:
            cursor = self.connect.cursor()
            cursor.execute('SELECT * FROM user u WHERE u.chat_id = :chat_id AND u.group_id not NULL',
                           {"chat_id": chat_id})
            result = cursor.fetchone() is not None
        except sqlite3.DatabaseError as e:
            print('Error: ', e)
        return result

    def update_user(self, user):
        try:
            cursor = self.connect.cursor()
            cursor.execute("""UPDATE user
                                SET group_id = :group_id
                                WHERE chat_id = :chat_id""", {"group_id": user.group_id, "chat_id": user.chat_id})
            self.connect.commit()
            return self.get_user(user)
        except sqlite3.DatabaseError as e:
            print('Error: ', e)

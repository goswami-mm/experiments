import sqlite3
from sqlite3 import Error


class DbRepositor:
    def openDb(self):
        conn = sqlite3.connect('my_database.sqlite')
        cursor = conn.cursor()
        query = '''CREATE TABLE IF NOT EXISTS USER
                 (id INTEGER PRIMARY KEY,
                 name           TEXT,
                 password        TEXT,
                 phone           TEXT);'''
        cursor.execute(query)
        cursor.close()

    def addUser(self, user):
        conn = sqlite3.connect('my_database.sqlite')
        cursor = conn.cursor()
        query = '''INSERT INTO USER (name, password, phone) VALUES (?, ?, ?); '''
        cursor.execute(query, (user.name, user.password, user.phone))
        conn.commit()
        conn.close()

    def getUser(self, id):
        conn = sqlite3.connect('my_database.sqlite')
        cursor = conn.cursor()
        query = "SELECT id, name, phone FROM USER WHERE id == ? "
        try:
            row = cursor.execute(query, (int(id),)).fetchone()
            user = User(row[0], row[1], '', row[2])
            conn.commit()
            conn.close()
            return user.serialize()
        except Error as e:
            print("error : ", e)
            return {"error": e}.__str__()
        except:
            return {"error"}.__str__()

    def validUser(self, name, password):
        conn = sqlite3.connect('my_database.sqlite')
        cursor = conn.cursor()
        query = "SELECT id, name, phone FROM USER WHERE name == ? AND password == ?"
        try:
            row = cursor.execute(query, (name, password)).fetchone()
            print(row)
            user = User(row[0], row[1], '', row[2])
            conn.commit()
            conn.close()
            return user
        except Error as e:
            return False


class User(object):
    def __init__(self, id, name, password, phone):
        self.id = id
        self.name = name
        self.password = password
        self.phone = phone

    def __str__(self):
        return "User(id='%s' name='%s' )" % (self.id, self.name)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
        }

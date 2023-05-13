import sqlite3
import os


class Db:
    """
    Database class
    """

    def __init__(self, db_name, clear=False):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.clear = clear

    def __enter__(self):
        db_path = os.path.join(os.getcwd(), self.db_name)
        if self.clear:
            os.remove(db_path)
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()

    # def __init__(self, db_name, clear=False):
    #    if os.path.exists(db_name) and clear:
    #        os.remove(db_name)
    #    self.conn = sqlite3.connect(db_name, check_same_thread=False)
    #    self.cursor = self.conn.cursor()

    def create_tables(self):
        """
        Create tables
        :return:
        """
        query_tokens = '''CREATE TABLE IF NOT EXISTS tokens (
                    id INTEGER PRIMARY KEY,
                    token TEXT NOT NULL
                )'''
        self.cursor.execute(query_tokens)
        self.conn.commit()

    def delete_tables(self):
        """
        Delete tables
        :return:
        """
        query_tokens = '''DROP TABLE IF EXISTS tokens'''
        self.cursor.execute(query_tokens)
        self.conn.commit()

    def insert_token(self, token_id, token):
        """
        Insert a token
        :param token_id:
        :param token:
        :return:
        """
        query = '''INSERT INTO tokens (id, token) VALUES (?, ?)'''
        # make sure the user is unique
        if self.get_token(token_id) is not None:
            return False
        self.cursor.execute(query, (token_id, token))
        self.conn.commit()

    def get_token(self, token_id):
        """
        Get a token by id
        :param token_id:
        :return:
        """
        query = '''SELECT * FROM tokens WHERE id = ?'''
        self.cursor.execute(query, (token_id,))
        return self.cursor.fetchone()

    def delete_token(self, token_id):
        """
        Delete a token
        :param token_id:
        :return:
        """
        query = '''DELETE FROM tokens WHERE id = ?'''
        # si l'utilisateur n'existe pas
        if self.get_token(token_id) is None:
            return False
        self.cursor.execute(query, (token_id,))
        self.conn.commit()

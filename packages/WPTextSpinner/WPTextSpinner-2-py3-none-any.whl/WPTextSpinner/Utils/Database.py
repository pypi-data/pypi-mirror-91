import mysql.connector

from WPTextSpinner.Utils import Logger
from WPTextSpinner.Utils import Utils

LOG = False


class Database:
    def __init__(self, db=None):
        if db is None:
            db = self.get_database_con()
        self.db = db

    def select_one(self, query, params=None):
        try:
            cur = self.do_query(query, params)
            output = cur.fetchone()
            cur.close()
            return output
        except:
            return None

    def select_all(self, query, params=None):
        try:
            cur = self.do_query(query, params)
            output = cur.fetchall()
            cur.close()
            return output
        except:
            return []

    def insert(self, query, params=None):
        try:
            cur = self.do_query(query, params)
            last_id = cur.lastrowid
            cur.close()
            return last_id
        except:
            # if Logger.IS_DEBUG:
            #    traceback.print_exc()
            return False

    def insert_many(self, query, params):
        try:
            mycursor = self.db.cursor(buffered=True)

            if LOG:
                Logger.log(query)

            mycursor.executemany(query, params)

            return mycursor
        except:
            # if Logger.IS_DEBUG:
            #    traceback.print_exc()
            return False

    def do_query(self, sql: str, params: dict):
        """
        Executes the given sql-statement and returns a pointer to the resulting cursor
        :param sql: the sql-statement as a string
        :param params: the parameters-dict
        :return: the cursor after executing the query
        """
        try:
            return self.do_sql_query(sql, params)
        except:
            # Update database connection
            self.db = self.get_database_con()
            return self.do_sql_query(sql, params)

    def do_sql_query(self, sql, params):
        mycursor = self.db.cursor(buffered=True)

        if LOG:
            Logger.log((sql, params))

        mycursor.execute(sql, params)

        return mycursor

    def get_database_con(self):
        """
        Returns a connection to the database
        :return: the database connection
        """

        data = Utils.get_config_data()

        host = data['db']['host']
        user = data['db']['user']
        passwd = data['db']['pw']
        database = data['db']['db']
        self.table_prefix = data['db']['wp_table_prefix']

        db = mysql.connector.connect(host=host, user=user, passwd=passwd,
                                     database=database, auth_plugin='mysql_native_password')
        return db

    def close(self):
        self.db.close()
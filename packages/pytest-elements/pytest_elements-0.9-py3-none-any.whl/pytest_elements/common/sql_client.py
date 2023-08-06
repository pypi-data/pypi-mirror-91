import pymysql


class SQLClient(object):
    def __init__(self, connection):
        self.host = connection["database_host"]
        self.port = int(connection["database_port"])
        self.db = connection["database_name"]
        self.user = connection["database_user"]
        self.password = connection["database_password"]
        self.connection = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            db=self.db,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

    def execute_query(self, query):
        """
        Executes the given query string and returns the result.
        :param query: String sql query to execute
        :return: Result of query
        """
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            self.connection.commit()
            return cursor.fetchall()

import mysql.connector


class CreateConnection:
    def __init__(self, database_name):
        self.database_name = database_name
        self._connection_value = {
            'user': 'appuser',
            'password': 'unit123',
            'host': 'localhost',
            'port': 3306,
            'database': 'bibekdb'
            }

    def __get_connection_value(self):
        return self._connection_value

    def create_connection(self):
        value = self.__get_connection_value()
        my_conn = mysql.connector.connect(user=value['user'],
                                          password=value['password'],
                                          port=value['port'],
                                          database=value['database'],
                                          host=value['host'])
        return my_conn

    def get_data_from_table(self, table_name):
        my_conn = self.create_connection()
        my_cursor = my_conn.cursor()
        my_cursor.execute(f"select * from {table_name}")
        data = my_cursor.fetchall()
        return data


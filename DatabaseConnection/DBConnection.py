import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self):
        self.connection = None
        self.connect()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="11052004",
                database="quanlynhanvien"
            )
            if self.connection.is_connected():
                print(f"Kết nối thành công đến MySQL, version: {self.connection.get_server_info()}")
        except Error as e:
            print(f"Lỗi kết nối đến MySQL: {e}")
            self.connection = None

    def disconnect(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Đã đóng kết nối MySQL")

    def execute_query(self, query, params=None):
        cursor = None
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            cursor = self.connection.cursor(dictionary=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor
        except Error as e:
            print(f"Lỗi khi thực thi query: {e}")
            return None

    def fetch_all(self, query, params=None):
        cursor = self.execute_query(query, params)
        if cursor:
            result = cursor.fetchall()
            return result
        return []

    def fetch_one(self, query, params=None):
        cursor = self.execute_query(query, params)
        #print(cursor)
        if cursor:
            result = cursor.fetchone()
            return result
        return None
    def insert(self, query, params=None):
        cursor = None
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            self.connection.commit()
            return cursor.lastrowid
        except Error as e:
            print(f"Lỗi khi thêm bản ghi: {e}")
            return None
        finally:
            if cursor:
                cursor.close()

    def update(self, query, params=None):
        cursor = None
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()

            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            self.connection.commit()
            return cursor.rowcount
        except Error as e:
            print(f"Lỗi khi cập nhật bản ghi: {e}")
            return 0
        finally:
            if cursor:
                cursor.close()

    def delete(self, query, params=None):
        return self.update(query, params)
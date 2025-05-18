import hashlib
from Models.Account import Account
from DatabaseConnection.DBConnection import Database


class AccountService:
    def __init__(self):
        self.db = Database()

    def get_all_accounts(self):
        query = "SELECT * FROM account"
        result = self.db.fetch_all(query)
        return result

    def get_account_by_id(self, id_employee):
        query = "SELECT * FROM account WHERE id_employee = %s"
        result = self.db.fetch_one(query, (id_employee,))
        if result:
            return result
        return None

    def get_account_by_username(self, username):
        query = "SELECT * FROM account WHERE username = %s"
        result = self.db.fetch_one(query, (username,))
        if result:
            return result
        return None

    def create_account(self, account):
        existing = self.get_account_by_id(account.id_employee)
        if existing:
            print(f"Lỗi: Nhân Viên có ID {account.id_employee} đã có tài khoản")
            return None
        query = """
        INSERT INTO account (id_employee, username, password, role)
        VALUES (%s, %s, %s, %s)
        """
        params = (account.id_employee, account.username, account.password, account.role)
        return self.db.insert(query, params)

    def update_password(self, username, new_password):
        # Kiểm tra tài khoản có tồn tại không
        existing = self.get_account_by_username(username)
        if not existing:
            print(f"Lỗi: Không tìm thấy tài khoản với username {username}")
            return False
        query = "UPDATE account SET password = %s WHERE username = %s"
        params = (new_password, username)
        rows_affected = self.db.update(query, params)
        return rows_affected > 0

    def delete_account(self, id_employee):
        query = "DELETE FROM account WHERE id_employee = %s"
        rows_affected = self.db.delete(query, (id_employee,))
        return rows_affected > 0

    def authenticate(self, username, password):
        account = self.get_account_by_username(username)
        if account:
            if account.password == password:
                return True
        return False
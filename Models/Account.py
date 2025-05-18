class Account:
    def __init__(self, id_employee=None, username=None, password=None, role=None):

        self.id_employee = id_employee
        self.username = username
        self.password = password
        self.role = role

    def to_dict(self):
        return {
            'id_employee': self.id_employee,
            'username': self.username,
            'password': self.password,
            'role': self.role
        }

    @staticmethod
    def from_dict(data):
        if not data:
            return None
        return Account(
            id_employee=data.get('id_employee'),
            username=data.get('username'),
            password=data.get('password'),
            role=data.get('role')
        )

    def __str__(self):
        return f"[{self.id_employee}, username={self.username}, role={self.role}]"
    def is_admin(self):
        return self.role and self.role.lower() == 'admin'

    def is_manager(self):
        return self.role and self.role.lower() == 'manager'
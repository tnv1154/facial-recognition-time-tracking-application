from datetime import datetime

class Employee:

    def __init__(self, id_employee=None, name=None, date_of_birth=None,
                 phonenumber=None, email=None, address=None, id_department=None,
                 gender=None, position=None, status="active"):

        self.id_employee = id_employee
        self.name = name
        self.date_of_birth = date_of_birth
        self.phonenumber = phonenumber
        self.email = email
        self.address = address
        self.id_department = id_department
        self.gender = gender
        self.position = position
        self.status = status

    def to_dict(self):
        return {
            'id_employee': self.id_employee,
            'name': self.name,
            'date_of_birth': self.date_of_birth.strftime('%Y-%m-%d') if self.date_of_birth else None,
            'phonenumber': self.phonenumber,
            'email': self.email,
            'address': self.address,
            'id_department': self.id_department,
            'gender': self.gender,
            'position': self.position,
            'status': self.status
        }

    @staticmethod
    def from_dict(data):
        if not data:
            return None
        date_of_birth = None
        if data.get('date_of_birth'):
            try:
                if isinstance(data['date_of_birth'], str):
                    date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
                else:
                    date_of_birth = data['date_of_birth']
            except ValueError:
                print(f"Lỗi định dạng ngày sinh: {data['date_of_birth']}")

        return Employee(
            id_employee=data.get('id_employee'),
            name=data.get('name'),
            date_of_birth=date_of_birth,
            phonenumber=data.get('phonenumber'),
            email=data.get('email'),
            address=data.get('address'),
            id_department=data.get('id_department'),
            gender=data.get('gender'),
            position=data.get('position'),
            status=data.get('status', 'active')
        )

    def __str__(self):
        return f"Employee[id={self.id_employee}, name={self.name}, position={self.position}]"

    def get_age(self):
        if not self.date_of_birth:
            return None

        today = datetime.now().date()
        age = today.year - self.date_of_birth.year

        # Kiểm tra nếu chưa đến ngày sinh trong năm nay
        if (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day):
            age -= 1
        return age

    def is_active(self):
        return self.status and self.status.lower() == 'active'

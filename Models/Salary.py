from calendar import month


class Salary:
    def __init__(self, id_salary=None, basic=0, phucap=0, total=0, id_employee=None,month=None):
        self.id_salary = id_salary
        self.basic = basic
        self.phucap = phucap
        self.total = total if total else (basic + phucap)
        self.id_employee = id_employee
        self.month=month

    def calculate_total(self):
        self.total = self.basic + self.phucap
        return self.total

    def to_dict(self):
        return {
            'id_salary': self.id_salary,
            'basic': self.basic,
            'phucap': self.phucap,
            'total': self.total,
            'id_employee': self.id_employee
        }

    @staticmethod
    def from_dict(data):
        if not data:
            return None
        return Salary(
            id_salary=data.get('id_salary'),
            basic=float(data.get('basic', 0)),
            phucap=float(data.get('phucap', 0)),
            total=float(data.get('total', 0)),
            id_employee=data.get('id_employee'),
            month=data.get('month'),
        )

    def __str__(self):
        return f"Salary[id={self.id_salary}, employee_id={self.id_employee}, basic={self.basic}, total={self.total}, month={self.month}]"

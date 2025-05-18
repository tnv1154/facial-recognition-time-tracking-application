from Models.Employee import Employee
from DatabaseConnection.DBConnection import Database

class EmployeeService:
    def __init__(self):
        self.db = Database()

    def get_all_employees(self):
        query = "SELECT * FROM employee"
        result = self.db.fetch_all(query)
        return result

    def get_employees_by_id_employee(self,id_employee):
        query = "SELECT * FROM employee WHERE id_employee = %s"
        params= (id_employee,)
        result = self.db.fetch_one(query,params)
        return result

    def create_employee(self, employee):
        query = """
        INSERT INTO employee (id_employee,name, date_of_birth, phonenumber, email, address, 
                              department, gender, position, status,cccd)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            employee['id_employee'],
            employee['name'],
            employee['date_of_birth'],
            employee['phonenumber'],
            employee['email'],
            employee['address'],
            employee['department'],
            employee['gender'],
            employee['position'],
            employee['status'],
            employee['cccd'],
        )
        return self.db.insert(query, params)

    def update_employee(self, employee):
        query = """
        UPDATE employee
        SET id_employee = %s, name = %s, date_of_birth = %s, phonenumber = %s, email = %s, 
            address = %s, department = %s, gender = %s, position = %s, status = %s, cccd = %s
        WHERE id_employee = %s
        """
        params = (
            employee['id_employee'],
            employee['name'],
            employee['date_of_birth'],
            employee['phonenumber'],
            employee['email'],
            employee['address'],
            employee['department'],
            employee['gender'],
            employee['position'],
            employee['status'],
            employee['cccd'],
            employee['id_employee'],
        )
        rows_affected = self.db.update(query, params)
        return rows_affected > 0

    def delete_employee(self, id_employee):
        query = "DELETE FROM employee WHERE id_employee = %s"
        rows_affected = self.db.delete(query, (id_employee,))
        return rows_affected > 0

    def count_employees_dang_lam(self):
        query = """
        SELECT *
        FROM employee
        WHERE status = 'Đang làm';
        """
        result = self.db.fetch_all(query)
        return result

    def count_employees_by_department(self):
        query = """
        SELECT department, COUNT(*) as count
        FROM employee
        GROUP BY department
        """
        result = self.db.fetch_all(query)
        return {item['department']: item['count'] for item in result}

from Models.Salary import Salary
from DatabaseConnection.DBConnection import Database
from Service.Employee_Service import EmployeeService

class SalaryService:
    def __init__(self):
        self.db = Database()

    def get_all_salaries(self):
        query = "SELECT * FROM salary"
        result = self.db.fetch_all(query)
        return result

    def get_salary_by_employee(self, id_employee):
        query = "SELECT * FROM salary WHERE id_employee = %s"
        result = self.db.fetch_one(query, (id_employee,))
        if result:
            return result
        return None

    def create_salary(self, salary):
        existing = self.get_salary_by_employee(salary.id_employee)
        if existing:
            print(f"Lỗi: Nhân viên ID {salary.id_employee} đã có bản ghi lương")
            return None
        emp = EmployeeService()
        exist_id_emp=emp.get_all_id_employees()
        print(exist_id_emp)
        if salary.id_employee not in exist_id_emp:
            print(f'Khong ton tai nhan vien co id la {salary.id_employee}')
            return None
        salary.calculate_total()
        query = """
        INSERT INTO salary (basic, phucap, total, id_employee,month)
        VALUES (%s, %s, %s, %s, %s)
        """
        params = (salary.basic, salary.phucap, salary.total, salary.id_employee,salary.month)
        return self.db.insert(query, params)

    def update_salary_by_employee(self, salary):
        # Kiểm tra bản ghi lương có tồn tại không
        existing = self.get_salary_by_employee(salary.id_employee)
        if not existing:
            print(f"Lỗi: Không tìm thấy bản ghi lương cho nhân viên ID {salary.id_employee}")
            return False
        salary.calculate_total()

        query = """
        UPDATE salary
        SET basic = %s, phucap = %s, total = %s
        WHERE id_employee = %s
        """
        params = (salary.basic, salary.phucap, salary.total, salary.id_employee)
        rows_affected = self.db.update(query, params)
        return rows_affected > 0

    def delete_salary_by_employee(self, id_employee):
        query = "DELETE FROM salary WHERE id_employee = %s"
        rows_affected = self.db.delete(query, (id_employee,))
        return rows_affected > 0

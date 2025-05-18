import json
import os
from datetime import datetime
from Service.Employee_Service import EmployeeService

class DatabaseManager:
    def __init__(self):
        self.db_file = "employees.json"
        self.create_sample_data()
        self.employees = self.load_data()
    def load_data(self):
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, 'r', encoding='utf-8') as file:
                    return json.load(file)
            except:
                return []
        else:
            return []

    def save_data(self):
        with open(self.db_file, 'w', encoding='utf-8') as file:
            json.dump(self.employees, file, ensure_ascii=False, indent=4)

    def create_sample_data(self):
        emp=EmployeeService()
        sample_data = emp.get_all_employees()
        self.employees = sample_data
        self.save_data()

    def get_all_employees(self):
        return self.employees

    def get_employee_by_id(self, employee_id):
        for employee in self.employees:
            if employee["id_employee"] == employee_id:
                return employee
        return None

    def add_employee(self, employee_data):
        for employee in self.employees:
            if employee["id_employee"] == int(employee_data["id_employee"]):
                return False
        self.employees.append(employee_data)
        self.save_data()
        emp=EmployeeService()
        emp.create_employee(employee_data)
        return True

    def update_employee(self, employee_id, employee_data):
        for i, employee in enumerate(self.employees):
            if employee["id_employee"] == employee_id:
                self.employees[i] = employee_data
                self.save_data()
                emp = EmployeeService()
                emp.update_employee(employee_data)
                return True
        return False

    def delete_employee(self, employee_id):
        for i, employee in enumerate(self.employees):
            if employee["id_employee"] == employee_id:
                del self.employees[i]
                self.save_data()
                emp = EmployeeService()
                emp.delete_employee(employee_id)
                return True
        return False

    def search_employees(self, search_type, search_term):
        results = []
        search_term = search_term.lower()
        field = None
        if search_type == "ID Nhân viên":
            field = "id_employee"
        elif search_type == "Họ Tên":
            field = "name"
        elif search_type == "Phòng ban":
            field = "department"
        elif search_type == "Chức vụ":
            field = "position"
        if field:
            for employee in self.employees:
                if search_term in employee[field].lower():
                    results.append(employee)
        return results
    def get_max_id_employee(self):
        emp=self.employees
        id_emp=[int(id["id_employee"]) for id in emp]
        id_max=max(id_emp)
        return id_max+1

from datetime import datetime, timedelta
from Service.Employee_Service import EmployeeService
from Service.Timekeeping_Service import TimekeepingService
from Service.Salary_Service import SalaryService
from Models.Employee import Employee
from Models.Timekeeping import Timekeeping
from Models.Salary import Salary

emp = EmployeeService().get_all_employees()
employees = [[str(value) for value in d.values()] for d in emp]

timek = TimekeepingService().get_all_timekeeping()
timekeepings =[[str(value) for value in d.values()] for d in timek]

sala = SalaryService().get_all_salaries()
salarys =[[str(value) for value in d.values()] for d in sala]
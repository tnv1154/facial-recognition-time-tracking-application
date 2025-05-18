from Account_Service import AccountService
from Employee_Service import EmployeeService
from Salary_Service import SalaryService
from Timekeeping_Service import TimekeepingService
from datetime import *

timekeepingService = TimekeepingService()
timekeepingService.check_out_employee(1, "00:10")


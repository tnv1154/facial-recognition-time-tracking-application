from datetime import datetime, date
from Models.Timekeeping import Timekeeping
from DatabaseConnection.DBConnection import Database


class TimekeepingService:
    def __init__(self):
        self.db = Database()

    def get_all_timekeeping(self):
        query = "SELECT * FROM timekeeping"
        result = self.db.fetch_all(query)
        return result

    def get_timekeeping_by_id(self, id_timekeeping):
        query = "SELECT * FROM timekeeping WHERE id_timekeeping = %s"
        result = self.db.fetch_one(query, (id_timekeeping,))
        if result:
            return result
        return None

    def get_timekeeping_by_employee(self, id_employee):
        query = "SELECT * FROM timekeeping WHERE id_employee = %s ORDER BY date DESC"
        result = self.db.fetch_all(query, (id_employee,))
        return result

    def get_timekeeping_by_date(self, date_value):
        query = "SELECT * FROM timekeeping WHERE date = %s"
        result = self.db.fetch_all(query, (date_value,))
        return result

    def get_timekeeping_by_employee_and_date(self, id_employee, date_value):
        query = "SELECT * FROM timekeeping WHERE id_employee = %s AND date = %s"
        print(date_value, id_employee)
        result = self.db.fetch_one(query, (int(id_employee), str(date_value)))
        print(f"result {result}")
        if result:
            return result
        return None


    def create_timekeeping(self, timekeeping):
        # Kiểm tra xem nhân viên đã có bản ghi chấm công trong ngày này chưa
        existing = self.get_timekeeping_by_employee_and_date(timekeeping.id_employee, timekeeping.date)
        if existing:
            print(f"Lỗi: Nhân viên ID {timekeeping.id_employee} đã có bản ghi chấm công cho ngày {timekeeping.date}")
            return None

        query = """
        INSERT INTO timekeeping (check_in, check_out, id_employee, date)
        VALUES (%s, %s, %s, %s)
        """
        params = (
            timekeeping.check_in,
            timekeeping.check_out,
            timekeeping.id_employee,
            str(timekeeping.date)
        )
        return self.db.insert(query, params)

    def update_timekeeping(self, timekeeping):
        # Kiểm tra bản ghi chấm công có tồn tại không
        existing = self.get_timekeeping_by_id(timekeeping.id_timekeeping)
        print(existing)
        if not existing:
            print(f"Lỗi: Không tìm thấy bản ghi chấm công với ID {timekeeping.id_timekeeping}")
            return False
        query = """
        UPDATE timekeeping 
        SET check_in = %s, check_out = %s, id_employee = %s, date = %s
        WHERE id_timekeeping = %s
        """
        params = (
            timekeeping.check_in,
            timekeeping.check_out,
            timekeeping.id_employee,
            str(timekeeping.date),
            timekeeping.id_timekeeping
        )
        print(params)

        return self.db.update(query, params)

    def delete_timekeeping(self, id_timekeeping):
        # Kiểm tra bản ghi có tồn tại không
        existing = self.get_timekeeping_by_id(id_timekeeping)
        if not existing:
            print(f"Lỗi: Không tìm thấy bản ghi chấm công với ID {id_timekeeping}")
            return False

        query = "DELETE FROM timekeeping WHERE id_timekeeping = %s"
        return self.db.execute(query, (id_timekeeping,))

    def check_in_employee(self, id_employee, check_in_time=None):
        if check_in_time is None:
            check_in_time = datetime.now()

        today = date.today()
        existing = self.get_timekeeping_by_employee_and_date(id_employee, today)
        if existing:
            print(f"Lỗi: Nhân viên ID {id_employee} đã check-in cho ngày {today}")
            return None

        # Tạo bản ghi chấm công mới
        new_timekeeping = Timekeeping(
            id_timekeeping=None,
            check_in=check_in_time,
            check_out=None,
            id_employee=id_employee,
            date=today
        )

        return self.create_timekeeping(new_timekeeping)

    def check_out_employee(self, id_employee, check_out_time=None):
        if check_out_time is None:
            check_out_time = datetime.now()

        today = date.today()

        # Lấy bản ghi chấm công của nhân viên trong ngày
        timekeeping = self.get_timekeeping_by_employee_and_date(id_employee, today)
        print(timekeeping)
        if not timekeeping:
            print(f"Lỗi: Nhân viên ID {id_employee} chưa check-in cho ngày {today}")
            return False
        print(check_out_time)
        # Cập nhật giờ check-out
        #.check_out = check_out_time
        new_timekeeping = Timekeeping(
            id_timekeeping=timekeeping["id_timekeeping"],
            check_in = timekeeping["check_in"],
            check_out=check_out_time,
            id_employee=timekeeping["id_employee"],
            date=timekeeping["date"]
        )
        print(new_timekeeping)
        return self.update_timekeeping(new_timekeeping)

    def get_monthly_timekeeping_report(self, id_employee, year, month):
        # Tính ngày đầu và cuối tháng
        start_date = date(year, month, 1)

        # Tính ngày cuối tháng
        if month == 12:
            next_month = 1
            next_year = year + 1
        else:
            next_month = month + 1
            next_year = year

        end_date = date(next_year, next_month, 1)
        end_date = date(end_date.year, end_date.month, 1).replace(day=1) - datetime.timedelta(days=1)

        return self.get_timekeeping_by_employee_and_date_range(id_employee, start_date, end_date)

    def calculate_working_hours(self, timekeeping):
        if not timekeeping.check_out:
            return None

        delta = timekeeping.check_out - timekeeping.check_in
        hours = delta.total_seconds() / 3600  # Chuyển đổi từ giây sang giờ

        return round(hours, 2)

    def get_department_timekeeping(self, id_department, date_value=None):
        if date_value is None:
            date_value = date.today()

        query = """
        SELECT t.* FROM timekeeping t
        JOIN employee e ON t.id_employee = e.id_employee
        WHERE e.id_department = %s AND t.date = %s
        """
        result = self.db.fetch_all(query, (id_department, date_value))
        return [Timekeeping.from_dict(item) for item in result]
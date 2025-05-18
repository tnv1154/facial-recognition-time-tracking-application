from datetime import datetime, time

class Timekeeping:
    def __init__(self, id_timekeeping=None, check_in=None, check_out=None, id_employee=None, date=None):

        self.id_timekeeping = id_timekeeping
        self.check_in = check_in
        self.check_out = check_out
        self.id_employee = id_employee
        self.date=date

    def get_working_hours(self):
        if not self.check_in or not self.check_out:
            return None

        # Tính thời gian làm việc theo giờ
        time_diff = self.check_out - self.check_in
        hours = time_diff.total_seconds() / 3600
        return round(hours, 2)

    def get_overtime(self, standard_hours=8):
        hours = self.get_working_hours()
        if hours is None or hours <= standard_hours:
            return 0

        return round(hours - standard_hours, 2)

    def is_late(self, standard_start=time(8, 0)):
        if not self.check_in:
            return False

        check_in_time = self.check_in.time()
        return check_in_time > standard_start

    def to_dict(self):
        return {
            'id_timekeeping': self.id_timekeeping,
            'check_in': self.check_in,
            'check_out': self.check_out,
            'id_employee': self.id_employee,
            'date': self.date,
        }

    @staticmethod
    def from_dict(data):
        if not data:
            return None
        return Timekeeping(
            id_timekeeping=data.get('id_timekeeping'),
            check_in=data.get("check_in"),
            check_out=data.get('check_out'),
            id_employee=data.get('id_employee'),
            date=data.get('date')
        )

    def __str__(self):
        return (f"Timekeeping[id={self.id_timekeeping}, "
                f"employee_id={self.id_employee}, date={self.date}, check_in={self.check_in}, check_out={self.check_out}]")

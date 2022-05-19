from controllers import front_controller
from repositories.employee_repo import EmployeeRepo


class EmployeeService:
    def __init__(self, employee_repo: EmployeeRepo):
        self.employee_repo = employee_repo

    def get_employees(self):
        return self.employee_repo.get_all_employees()

    def get_employees_by_department(self, dept_id):
        return self.employee_repo.get_employees_by_department(dept_id)

    def get_employees_by_supervisor(self, sup_id):
        return self.employee_repo.get_employees_by_supervisor(sup_id)

    def get_employee(self, employee_id):
        return self.employee_repo.get_employee(employee_id)

    def has_supervisor(self, employee_id):
        return self.employee_repo.has_supervisor(employee_id)

    def is_supervisor(self, sup_id, sub_id):
        return self.employee_repo.is_supervisor(sup_id, sub_id)

    def login(self, username, password):
        return self.employee_repo.get_employee_by_login_info(username, password)

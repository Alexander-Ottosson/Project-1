import unittest

from exceptions.resource_not_found import ResourceNotFound
from models.employee import Employee
from repositories.employee_repo import EmployeeRepo
from services.employee_service import EmployeeService


class TestEmployeeService(unittest.TestCase):
    er = EmployeeRepo()
    es = EmployeeService(er)

    # TODO: Alter test to work if more employees are added
    def test_get_all_employees(self):
        employees = self.es.get_employees()

        self.assertEqual(len(employees), 5)

    # TODO: Alter test to work if more employees are added
    def test_get_employees_by_dept(self):
        employees = self.es.get_employees_by_department(1)

        self.assertEqual(len(employees), 4)

    def test_neg_get_employees_by_dept(self):
        employees = self.es.get_employees_by_department(100)
        self.assertEqual(employees, [])

    # TODO: Alter test to work if more employees are added
    def test_get_employees_by_supervisor(self):
        employees = self.es.get_employees_by_supervisor(3)

        self.assertEqual(len(employees), 2)

    def test_neg_employees_by_supervisor(self):
        employees = self.es.get_employees_by_supervisor(1000)
        self.assertEqual(employees, [])

    def test_get_employee_by_id(self):
        employee = self.es.get_employee(1)

        self.assertEqual(employee, Employee(
            employee_id=1,
            first_name='Alexander',
            last_name='Ottosson',
            dept_id=1,
            username='aottosson',
            password='password',
            is_dept_head=True,
            is_benco=False,
            contact_info_ids=[1],
            subordinate_ids=[3]
        ))

    def test_neg_get_employee_by_id(self):
        try:
            employee = self.es.get_employee(1000)
            self.assertEqual(employee, None)
        except ResourceNotFound as e:
            self.assertEqual(e.message, 'Employee Not Found')

    def test_has_supervisor(self):
        has_sup = self.es.has_supervisor(5)
        self.assertEqual(has_sup, True)

        has_sup = self.es.has_supervisor(1)
        self.assertEqual(has_sup, False)

    def test_is_supervisor(self):
        is_sup = self.es.is_supervisor(5, 3)
        self.assertEqual(is_sup, False)

        is_sup = self.es.is_supervisor(3, 5)
        self.assertEqual(is_sup, True)

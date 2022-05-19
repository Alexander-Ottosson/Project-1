from exceptions.resource_not_found import ResourceNotFound
from models.employee import Employee
from repositories.contact_info_repo import ContactInfoRepo
from util.db_connection import connection
from util.object_builders import build_employee


def _get_full_employee_info(record):
    subordinates_sql = 'SELECT ' \
                       'subordinate_id, ' \
                       'supervisor_id ' \
                       'FROM supervisor ' \
                       'WHERE supervisor_id = %s;'

    cir = ContactInfoRepo()

    cursor = connection.cursor()

    # TODO: move the cursor.execute() calls to their own repos
    employee_id = record[0]
    contact_info_ids = [c.info_id for c in cir.get_by_employee_id(employee_id)]
    cursor.execute(subordinates_sql, [employee_id])
    subs = cursor.fetchall()
    subordinate_ids = [s[0] for s in subs]
    return build_employee(
            record,
            contact_info_ids,
            subordinate_ids
    )


class EmployeeRepo:

    def get_all_employees(self):
        employee_sql = 'SELECT * ' \
                       'FROM employee;'

        cursor = connection.cursor()
        cursor.execute(employee_sql)
        records = cursor.fetchall()
        employees = list()

        for record in records:
            employees.append(_get_full_employee_info(record))
        return employees

    def get_employees_by_department(self, department_id):
        employee_sql = 'SELECT * ' \
                       'FROM employee ' \
                       'WHERE dept_id = %s;'

        cursor = connection.cursor()
        cursor.execute(employee_sql, [department_id])
        records = cursor.fetchall()
        employees = list()

        for record in records:
            employees.append(_get_full_employee_info(record))
        return employees

    def get_employees_by_supervisor(self, sup_id):
        employee_sql = 'SELECT ' \
                       'e.id, ' \
                       'e.first_name, ' \
                       'e.last_name, ' \
                       'e.dept_id, ' \
                       'e.username, ' \
                       'e."password", ' \
                       'e.is_dept_head, ' \
                       'e.is_benco, ' \
                       's.supervisor_id, ' \
                       's.subordinate_id ' \
                       'FROM supervisor s ' \
                       'JOIN employee e ON s.subordinate_id = e.id ' \
                       'WHERE s.supervisor_id = %s'

        cursor = connection.cursor()
        cursor.execute(employee_sql, [sup_id])
        records = cursor.fetchall()
        employees = list()

        for record in records:
            employees.append(_get_full_employee_info(record))
        return employees

    def get_employee(self, employee_id):
        employee_sql = 'SELECT * ' \
                       'FROM employee ' \
                       'WHERE id = %s;'

        cursor = connection.cursor()
        cursor.execute(employee_sql, [employee_id])
        record = cursor.fetchone()

        if record:
            return _get_full_employee_info(record)
        else:
            raise ResourceNotFound('Employee Not Found')

    def has_supervisor(self, employee_id):
        sql = 'SELECT COUNT(supervisor_id) ' \
              'FROM supervisor ' \
              'WHERE subordinate_id = %s'

        cursor = connection.cursor()
        cursor.execute(sql, [employee_id])
        record = cursor.fetchone()

        if record[0] > 0:
            return True
        else:
            return False

    def is_supervisor(self, sup_id, sub_id):
        sql = 'SELECT COUNT(supervisor_id) ' \
              'FROM supervisor ' \
              'WHERE supervisor_id = %s AND subordinate_id = %s'

        cursor = connection.cursor()
        cursor.execute(sql, [sup_id, sub_id])
        record = cursor.fetchone()

        if record[0] > 0:
            return True
        else:
            return False

    def get_employee_by_login_info(self, username, password):
        sql = 'SELECT * ' \
              'FROM employee ' \
              'WHERE username = %s AND password = %s'

        cursor = connection.cursor()
        cursor.execute(sql, [username, password])
        record = cursor.fetchone()

        if record:
            return _get_full_employee_info(record)
        else:
            raise ResourceNotFound('Login Failed')


def _test():
    repo = EmployeeRepo()
    print(repo.get_all_employees())
    # print(repo.get_employees_by_supervisor(1))
    # print(repo.get_employees_by_department(1))
    # print(repo.get_employee(1))


if __name__ == '__main__':
    _test()

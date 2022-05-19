from flask import jsonify, request

from controllers import front_controller as fc
from exceptions.invalid_credentials import InvalidCredentials
from exceptions.resource_not_found import ResourceNotFound
from models.employee import Employee
from repositories.employee_repo import EmployeeRepo
from services.employee_service import EmployeeService

er = EmployeeRepo()
es = EmployeeService(er)


def route(app):

    @app.route('/employees', methods=['GET'])
    def get_permitted_employees():
        # determine what kind of user has logged in, and show the correct employees
        if fc.user.is_benco:
            return get_employees()
        elif fc.user.is_dept_head:
            return get_employees_by_dept()
        else:
            return get_employees_by_supervisor()

    # @app.route('/employees', methods=['GET'])
    def get_employees():
        try:
            # Make sure the user is a Ben_Co
            if not fc.user.is_benco:
                raise InvalidCredentials('You are not a Benefits Coordinator')

            employees = es.get_employees()

            if employees:
                return jsonify([employee.json() for employee in employees]), 200
            else:
                raise ResourceNotFound('')
        except InvalidCredentials as e:
            return e.message, 403
        except ResourceNotFound as e:
            return 'Employees Not Found', 404

    # @app.route('/employees/dept', methods=['GET'])
    def get_employees_by_dept():
        try:
            # Make sure the user is a department head
            if not fc.user.is_dept_head:
                raise InvalidCredentials('You are not a Department Head')

            employees = es.get_employees_by_department(fc.user.dept_id)

            if employees:
                return jsonify([employee.json() for employee in employees])
            else:
                raise ResourceNotFound('')
        except InvalidCredentials as e:
            return e.message, 403
        except ResourceNotFound as e:
            return 'Employees Not Found', 404

    # @app.route('/employees/dept/<dept_id>', methods=['GET'])
    def get_employees_by_dept_id(dept_id):
        try:
            dept_id = int(dept_id)

            # Make sure the user is a benco or the head of the given department
            if not fc.user.is_benco and not (fc.user.dept_id == dept_id and fc.user.is_dept_head):
                raise InvalidCredentials('You do not have valid credentials')

            employees = es.get_employees_by_department(dept_id)
            if employees:
                return jsonify([employee.json() for employee in employees])
            else:
                return ResourceNotFound('')

        except ValueError as e:
            return 'Please Include a valid Department Id', 400
        except InvalidCredentials as e:
            return e.message, 403
        except ResourceNotFound as e:
            return 'Employees Not Found', 404

    # @app.route('/employees/supervisor', methods=['GET'])
    def get_employees_by_supervisor():
        try:
            employees = es.get_employees_by_supervisor(fc.user.employee_id)

            if employees:
                return jsonify([employee.json() for employee in employees])
            else:
                return ResourceNotFound('')

        except ResourceNotFound as e:
            return 'Employees Not Found', 404

    @app.route('/employee/<employee_id>', methods=['GET'])
    def get_employee_by_id(employee_id):
        try:
            employee_id = int(employee_id)

            empl: Employee = es.get_employee(employee_id)

            # User must be either a BenCo, the head of the employee's dept, or their supervisor
            if \
                    not fc.user.is_benco \
                    and not (fc.user.is_dept_head and fc.user.dept_id == empl.dept_id) \
                    and employee_id not in fc.user.subordinate_ids:
                raise InvalidCredentials('Invalid Credentials')

            if empl:
                return empl.json()
            else:
                raise ResourceNotFound('');

        except ValueError as e:
            return 'Please include a valid Employee Id'
        except InvalidCredentials as e:
            return e.message, 403

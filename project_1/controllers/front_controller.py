from flask import request

from controllers import employee_controller, request_controller, approval_controller
from exceptions.resource_not_found import ResourceNotFound
from models.employee import Employee
from repositories.employee_repo import EmployeeRepo
from services.employee_service import EmployeeService

er = EmployeeRepo()
es = EmployeeService(er)

user = es.get_employee(3)
# user = Employee()


def route(app):

    @app.route('/login', methods=['POST'])
    def login():
        try:
            body = request.json
            global user
            user = es.login(body['username'], body['password'])
            return {
                'message': 'Successfully Logged In'
                   }, 200
        except ResourceNotFound as e:
            return 'Invalid Login', 401

    employee_controller.route(app)
    request_controller.route(app)
    approval_controller.route(app)



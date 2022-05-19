import time
from datetime import datetime

from flask import jsonify, request, render_template

from controllers import front_controller as fc
from exceptions.invalid_credentials import InvalidCredentials
from exceptions.resource_not_found import ResourceNotFound
from models.approval import Approval
from models.employee import Employee
from models.request import Request
from repositories.employee_repo import EmployeeRepo
from repositories.event_type_repo import EventTypeRepo
from repositories.request_repo import RequestRepo
from services.employee_service import EmployeeService
from services.event_type_service import EventTypeService
from services.request_service import RequestService

er = EmployeeRepo()
es = EmployeeService(er)

etr = EventTypeRepo()
ets = EventTypeService(etr)

rr = RequestRepo()
rs = RequestService(rr)


# TODO: Get User from a log in feature
# user: Employee = es.get_employee(1)


def route(app):
    @app.route('/requests', methods=['GET'])
    def get_permitted_requests():
        print(fc.user.employee_id)
        if fc.user.is_benco:
            return get_all_requests()
        elif fc.user.is_dept_head:
            return get_requests_by_department()
        elif len(fc.user.subordinate_ids) > 0:
            return get_requests_by_supervisor()
        else:
            return get_requests_by_user()

    def get_requests_by_user():
        requests = rs.get_requests_by_user(fc.user.employee_id)

        if requests:
            requests_JSON = jsonify([r.json() for r in requests])
            return requests_JSON, 200
        else:
            return [], 200

    # @app.route('/requests', methods=['GET'])
    def get_all_requests():
        try:
            # Only a Benefits Coordinator Should be able to access this
            if not fc.user.is_benco:
                raise InvalidCredentials('You are not a Benefits Coordinator')

            requests = rs.get_all_requests()

            if requests:
                return jsonify([r.json() for r in requests]), 200
            else:
                raise ResourceNotFound('')

        except InvalidCredentials as e:
            return e.message, 403
        except ResourceNotFound:
            return 'No requests found', 404

    # @app.route('/requests/dept', methods=['GET'])
    def get_requests_by_department():
        try:
            if not fc.user.is_dept_head:
                raise InvalidCredentials('You are not a Department Head')

            requests = rs.get_requests_by_department(fc.user.dept_id)

            if requests:
                return jsonify([r.json() for r in requests]), 200
            else:
                raise ResourceNotFound('')

        except InvalidCredentials as e:
            return e.message, 403
        except ResourceNotFound:
            return 'No requests found', 400

    # @app.route('/requests/dept/<dept_id>', methods=['GET'])
    def get_requests_by_department_id(dept_id):
        try:
            dept_id = int(dept_id)
            # Make sure the user is a benco or the head of the given department
            is_dept_head = (fc.user.dept_id == dept_id and fc.user.is_dept_head)
            if not fc.user.is_benco and not is_dept_head:
                raise InvalidCredentials('Invalid Credentials')

            requests = rs.get_requests_by_department(dept_id)

            if requests:
                return jsonify([r.json() for r in requests]), 200
            else:
                raise ResourceNotFound('')
        except ValueError as e:
            return 'Please use a valid department id', 400
        except InvalidCredentials as e:
            return e.message, 403
        except ResourceNotFound:
            return 'No requests found', 400

    # @app.route('/requests/supervisor', methods=['GET'])
    def get_requests_by_supervisor():
        try:
            requests = rs.get_requests_by_supervisor(fc.user.employee_id)

            if requests:
                return jsonify([r.json() for r in requests]), 200
            else:
                raise ResourceNotFound('')

        except InvalidCredentials as e:
            return e.message, 403
        except ResourceNotFound:
            return 'No requests found', 400

    @app.route('/requests/<request_id>', methods=['GET'])
    def get_request(request_id):
        try:
            req: Request = rs.get_request(int(request_id))
            if req:
                empl: Employee = es.get_employee(req.employee_id)
            else:
                raise ResourceNotFound('')
            if \
                    not fc.user.is_benco \
                    and not (fc.user.is_dept_head and fc.user.dept_id == empl.dept_id) \
                    and empl.employee_id not in fc.user.subordinate_ids \
                    and fc.user.employee_id != req.employee_id:
                raise InvalidCredentials('Invalid Credentials')

            start_date = req.event_start_date / 1000.0
            req.event_start_date = datetime.fromtimestamp(start_date).strftime('%m/%d/%y')

            end_date = req.event_end_date / 1000.0
            req.event_end_date = datetime.fromtimestamp(end_date).strftime('%m/%d/%y')

            miss_start_date = req.missed_work_start / 1000.0
            req.missed_work_start = datetime.fromtimestamp(miss_start_date).strftime('%m/%d/%y')

            miss_end_date = req.missed_work_end / 1000.0
            req.missed_work_end = datetime.fromtimestamp(miss_end_date).strftime('%m/%d/%y')

            print(req.employee_id)

            print(fc.user.subordinate_ids)

            if req.employee_id in fc.user.subordinate_ids:
                print(True)

            return render_template('view_request_template.html', request=req, user=fc.user), 200

        except InvalidCredentials as e:
            return e.message, 403
        except ResourceNotFound:
            return 'No requests found', 400

    @app.route('/requests', methods=['POST'])
    def create_request():
        try:
            # Benefit Coordinators should not be able to create a request
            if fc.user.is_benco:
                raise InvalidCredentials('Benefits Coordinators can\'t create requests')

            body = request.json

            if not body['eventStartDate']:
                body['eventStartDate'] = 0
            if not body['eventEndDate']:
                body['eventEndDate'] = 0
            if not body['missedWorkStart']:
                body['missedWorkStart'] = 0
            if not body['missedWorkEnd']:
                body['missedWorkEnd'] = 0

            req = Request(
                employee_id=fc.user.employee_id,
                event_start_date=int(body['eventStartDate']),
                event_end_date=int(body['eventEndDate']),
                street=body['street'],
                city=body['city'],
                state=body['state'],
                zip_code=body['zipCode'],
                event_name=body['eventName'],
                event_description=body['eventDescription'],
                event_cost=float(body['eventCost']),
                event_type_id=int(body['eventTypeId']),
                missed_work_start=int(body['missedWorkStart']),
                missed_work_end=int(body['missedWorkEnd']),
                grade_type=body['gradeType'],
                justification=body['justification']
            )

            event_type = ets.get_event_type(req.event_type_id)

            req.reimbursement_amount = req.event_cost * float(event_type.coverage)

            sup_approval = None
            if not es.has_supervisor(fc.user.employee_id):
                # The user effectively approves themselves since there is not anyone to approve for them
                sup_approval = Approval(
                    appr_type_id=1,
                    approver_id=fc.user.employee_id,
                    approved=True,
                )

            dept_approval = None
            if fc.user.is_dept_head:
                # The user effectively approves themselves since there is not anyone to approve for them
                dept_approval = Approval(
                    appr_type_id=2,
                    approver_id=fc.user.employee_id,
                    approved=True
                )

            req = rs.create_request(req, sup_approval, dept_approval)

            return req.json(), 200

        except InvalidCredentials as e:
            return 'Benefit Coordinator\'s cannot create requests', 403

        except ValueError as e:
            return 'Please format all values correctly', 400

    @app.route('/requests/<req_id>', methods=['PUT'])
    def update_request(req_id):
        try:
            body = request.json

            empl_id = rs.get_request(req_id).employee_id

            # Only the request creator or a BenCo can edit a request
            if (fc.user.employee_id != empl_id) and not fc.user.is_dept_head:
                raise InvalidCredentials('')

            req = Request(
                request_id=req_id,
                employee_id=empl_id,
                event_start_date=int(body['eventStartDate']),
                event_end_date=int(body['eventEndDate']),
                street=body['street'],
                city=body['city'],
                state=body['state'],
                zip_code=body['zipCode'],
                event_name=body['eventName'],
                event_description=body['eventDescription'],
                event_cost=float(body['eventCost']),
                event_type_id=int(body['eventTypeId']),
                missed_work_start=int(body['missedWorkStart']),
                missed_work_end=int(body['missedWorkEnd']),
                grade_type=body['gradeType'],
                justification=body['justification'],
                amount=body['amount']
            )

            old_req = rs.get_request(req_id)
            if not old_req:
                raise ResourceNotFound('Request Not Found')

            # Prevent a non BenCo from editing amount, cost, and event type
            if not fc.user.is_benco:
                req.event_cost = old_req.event_cost
                req.reimbursement_amount = old_req.reimbursement_amount
                req.event_type_id = old_req.event_type_id

            return rs.update_request(req).json()

        except InvalidCredentials as e:
            return 'You cannot alter this request', 403
        except ValueError as e:
            return 'Please format all values correctly', 400
        except ResourceNotFound as e:
            return e.message, 404

    @app.route('/requests/<request_id>', methods=['DELETE'])
    def delete_request(request_id):
        try:
            request_id = int(request_id)

            req: Request = rs.get_request(request_id)
            if not req:
                raise ResourceNotFound('Request Not Found')

            if fc.user.is_benco:
                # Continue delete
                rs.delete_request(request_id)
                return 'Successfully Deleted Request', 200
            elif fc.user.employee_id == req.employee_id and time.time() < req.event_start_date:
                # Employee can only cancel request before the event starts
                rs.delete_request(request_id)
                return 'Successfully Deleted Request', 200
            else:
                raise InvalidCredentials('You do not have access to delete this request')

        except ValueError as e:
            return 'Please input a valid ID', 400
        except ResourceNotFound as e:
            return e.message, 404
        except InvalidCredentials as e:
            return e.message, 403

    @app.route('/requests/update-amount/<request_id>', methods=['PATCH'])
    def update_amount(request_id):
        try:
            if not fc.user.is_benco:
                raise InvalidCredentials('Only a BenCo can alter a Reimbursement Amount')

            request_id = int(request_id)
            amount = float(request.json['amount'])

            req = rs.update_amount(amount, request_id)

            return req.json(), 200

        except InvalidCredentials as e:
            return e.message, 403
        except ValueError:
            return 'Please make sure all values are inputted correctly', 400
        except ResourceNotFound as e:
            return e.message, 404

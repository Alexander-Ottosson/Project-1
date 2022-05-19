from flask import request, jsonify

from controllers import front_controller as fc
from exceptions.invalid_credentials import InvalidCredentials
from exceptions.resource_not_found import ResourceNotFound
from models.approval import Approval
from models.employee import Employee
from models.request import Request
from repositories.approval_repo import ApprovalRepo
from repositories.employee_repo import EmployeeRepo
from repositories.request_repo import RequestRepo
from services.approval_service import ApprovalService
from services.employee_service import EmployeeService
from services.request_service import RequestService

er = EmployeeRepo()
es = EmployeeService(er)

rr = RequestRepo()
rs = RequestService(rr)

ar = ApprovalRepo()
aps = ApprovalService(ar)


def route(app):
    @app.route('/approvals/<appr_id>', methods=['GET'])
    def get_approval_by_id(appr_id):
        try:
            approval = aps.get_approval(appr_id)
            return approval.json()
        except ValueError:
            return 'Please input a proper id', 400
        except ResourceNotFound as e:
            return e.message, 404

    @app.route('/approvals/create-or-update/<req_id>', methods=['POST'])
    def create_or_update_approval(req_id):
        has_approved = aps.has_user_approved(req_id, fc.user.employee_id)

        if has_approved:
            return update_approval(req_id)
        else:
            return create_approval_by_request(req_id)

    @app.route('/approvals/<req_id>', methods=['POST'])
    def create_approval_by_request(req_id):
        try:
            body = request.json

            req: Request = rs.get_request(req_id)
            if not req:
                raise ResourceNotFound('Reimbursement Request Not Found')

            empl = es.get_employee(req.employee_id)

            # If user is benco, create a benco approval
            benco_appr = None
            if fc.user.is_benco:
                benco_appr = Approval(
                    approved=bool(body['approved']),
                    reason=body['reason'],
                    appr_type_id=3,
                    request_id=req_id,
                    approver_id=fc.user.employee_id
                )
            # If user is dept head, create a department head approval
            dept_appr = None
            if fc.user.is_dept_head and empl.dept_id == fc.user.dept_id:
                dept_appr = Approval(
                    approved=bool(body['approved']),
                    reason=body['reason'],
                    appr_type_id=2,
                    request_id=req_id,
                    approver_id=fc.user.employee_id
                )
            # If user is a supervisor, create a supervisor request
            sup_approval = None
            if empl.employee_id in fc.user.subordinate_ids:
                sup_approval = Approval(
                    approved=bool(body['approved']),
                    reason=body['reason'],
                    appr_type_id=1,
                    request_id=req_id,
                    approver_id=fc.user.employee_id
                )

            if not benco_appr and not dept_appr and not sup_approval:
                raise InvalidCredentials('You do not have access to this request')

            return jsonify([appr.json() for appr in aps.create_approval(benco_appr, dept_appr, sup_approval)])

        except ValueError as e:
            return 'Please make sure all values are formatted correctly', 400
        except ResourceNotFound as e:
            return e.message, 404
        except InvalidCredentials as e:
            return e.message, 403

    @app.route('/approvals/<req_id>', methods=['PATCH'])
    def update_approval(req_id):
        try:
            body = request.json

            req_id = int(req_id)

            change = Approval(
                request_id=req_id,
                approved=body['approved'],
                reason=body['reason']
            )

            req: Request = rs.get_request(req_id)
            if not req:
                raise ResourceNotFound('Request Not Found')

            req_appr = [a.approver_id for a in req.approvals]

            if fc.user.employee_id not in req_appr:
                raise InvalidCredentials('This request has no approvals you can alter')

            return jsonify([appr.json() for appr in aps.update_approval(change, fc.user.employee_id)])

        except ValueError as e:
            return 'Please make sure all values are formatted properly', 400
        except ResourceNotFound as e:
            return e.message, 404

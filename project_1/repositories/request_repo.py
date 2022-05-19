from exceptions.resource_not_found import ResourceNotFound
from models.approval import Approval
from models.request import Request
from repositories.approval_repo import ApprovalRepo
from util.db_connection import connection
from util.object_builders import build_request, build_approval

_sql_select = 'SELECT ' \
              'rr.id, ' \
              'rr.employee_id, ' \
              'rr.event_start_date, ' \
              'rr.event_end_date, ' \
              'rr.street, ' \
              'rr.city, ' \
              'rr.state, ' \
              'rr.zip, ' \
              'rr.event_name, ' \
              'rr.event_description, ' \
              'rr.event_cost, ' \
              'rr.event_type_id, ' \
              'et.name, ' \
              'rr.missed_work_start, ' \
              'rr.missed_work_end, ' \
              'rr.grade_type, ' \
              'rr.justification, ' \
              'rr.amount, ' \
              'e.first_name, ' \
              'e.last_name '

_sql_join = 'FROM reimbursement_request rr ' \
            'JOIN event_type et ON rr.event_type_id = et.id ' \
            'JOIN employee e ON rr.employee_id = e.id '


def _get_full_request_info(record):
    ar = ApprovalRepo()

    approvals = ar.get_approvals_by_request(record[0])

    # if records:
    #     approvals = [build_approval(r) for r in records]

    return build_request(record, approvals)


class RequestRepo:

    def get_all_requests(self):
        sql = _sql_select + _sql_join + \
              ' ORDER BY rr.event_start_date ASC'

        cursor = connection.cursor()
        cursor.execute(sql)
        records = cursor.fetchall()
        if records:
            return [_get_full_request_info(r) for r in records]
        else:
            return None

    def get_requests_by_employee(self, employee_id):
        sql = _sql_select + \
              _sql_join + \
              'WHERE rr.employee_id = %s ' \
              'ORDER BY rr.event_start_date ASC'

        cursor = connection.cursor()
        cursor.execute(sql, [employee_id])
        records = cursor.fetchall()

        if records:
            return [_get_full_request_info(r) for r in records]
        else:
            return None

    def get_requests_by_department(self, dept_id):
        sql = _sql_select + \
              ', e.dept_id ' + \
              _sql_join + \
              'WHERE e.dept_id = %s ' \
              'ORDER BY rr.event_start_date ASC '

        cursor = connection.cursor()
        cursor.execute(sql, [dept_id])
        records = cursor.fetchall()

        if records:
            return [_get_full_request_info(r) for r in records]
        else:
            return None

    def get_requests_by_supervisor(self, sup_id):
        sql = _sql_select + \
              ', s.supervisor_id, ' \
              's.subordinate_id ' + \
              _sql_join + \
              'JOIN supervisor s ON s.subordinate_id = rr.employee_id ' \
              'WHERE s.supervisor_id = %s ' \
              'ORDER BY rr.event_start_date ASC '

        cursor = connection.cursor()
        cursor.execute(sql, [sup_id])
        records = cursor.fetchall()

        if records:
            return [_get_full_request_info(r) for r in records]
        else:
            return None

    def get_request(self, req_id):
        sql = _sql_select + \
              _sql_join + \
              'WHERE rr.id = %s'

        cursor = connection.cursor()
        cursor.execute(sql, [req_id])
        record = cursor.fetchone()
        if record:
            return _get_full_request_info(record)
        else:
            raise ResourceNotFound('Request Not Found')

    def create_request(self, request, *approvals):
        request_sql = 'WITH new_request AS ( ' \
                      'INSERT INTO reimbursement_request VALUES ' \
                      '(' \
                      'DEFAULT,' \
                      '%(employeeId)s, ' \
                      '%(eventStartDate)s, ' \
                      '%(eventEndDate)s, ' \
                      '%(street)s, ' \
                      '%(city)s, ' \
                      '%(state)s, ' \
                      '%(zipCode)s, ' \
                      '%(eventName)s, ' \
                      '%(eventDescription)s, ' \
                      '%(eventCost)s, ' \
                      '%(eventTypeId)s, ' \
                      '%(missedWorkStart)s, ' \
                      '%(missedWorkEnd)s, ' \
                      '%(gradeType)s, ' \
                      '%(justification)s, ' \
                      '%(amount)s ) ' \
                      'RETURNING *' \
                      ') ' + \
                      _sql_select + \
                      'FROM new_request AS rr ' \
                      'JOIN event_type et ON rr.event_type_id = et.id ' \
                      'JOIN employee e ON rr.employee_id = e.id'

        appr_sql = 'INSERT INTO approval VALUES ' \
                   '(DEFAULT, ' \
                   '%(apprTypeId)s, ' \
                   '%(requestId)s, ' \
                   '%(approved)s, ' \
                   '%(approverId)s, ' \
                   '%(reason)s);'

        cursor = connection.cursor()
        request_dict = request.json()
        cursor.execute(request_sql, request_dict)
        req_record = cursor.fetchone()

        for a in approvals:
            if a:
                a: Approval = a
                a.request_id = req_record[0]
                appr_dict = a.json()
                cursor.execute(appr_sql, appr_dict)

        connection.commit()
        if req_record:
            return _get_full_request_info(req_record)
        else:
            return None

    def update_request(self, request):
        sql = 'WITH new_request AS ( ' \
              'UPDATE reimbursement_request SET ' \
              'employee_id = %(employeeId)s, ' \
              'event_start_date = %(eventStartDate)s, ' \
              'event_end_date = %(eventEndDate)s, ' \
              'street = %(street)s, ' \
              'city = %(city)s, ' \
              'state = %(state)s, ' \
              'zip = %(zipCode)s, ' \
              'event_name = %(eventName)s, ' \
              'event_description = %(eventDescription)s, ' \
              'event_cost = %(eventCost)s, ' \
              'event_type_id = %(eventTypeId)s, ' \
              'missed_work_start = %(missedWorkStart)s, ' \
              'missed_work_end = %(missedWorkEnd)s, ' \
              'grade_type = %(gradeType)s, ' \
              'justification = %(justification)s, ' \
              'amount = %(amount)s ' \
              'WHERE id = %(requestId)s ' \
              'RETURNING *' \
              ') ' + \
              _sql_select + \
              'FROM new_request AS rr ' \
              'JOIN event_type et ON rr.event_type_id = et.id ' \
              'JOIN employee e ON rr.employee_id = e.id'

        cursor = connection.cursor()
        request_dict = request.json()
        cursor.execute(sql, request_dict)
        record = cursor.fetchone()

        connection.commit()
        if record:
            return _get_full_request_info(record)
        else:
            return ResourceNotFound('Request Not Found')

    def delete_request(self, request_id):
        appr_delete = 'DELETE FROM approval ' \
                      'WHERE req_id = %s'
        req_sql = 'DELETE FROM reimbursement_request ' \
                  'WHERE id = %s'

        # Make sure the request exists
        self.get_request(request_id)

        cursor = connection.cursor()
        cursor.execute(appr_delete, [request_id])
        cursor.execute(req_sql, [request_id])
        connection.commit()

    def update_amount(self, amount, request_id):
        sql = 'WITH upd_request as (' \
              'UPDATE reimbursement_request SET ' \
              'amount = %s ' \
              'WHERE id = %s ' \
              'RETURNING *' \
              ') ' + \
              _sql_select + \
              'FROM upd_request AS rr ' \
              'JOIN event_type et ON rr.event_type_id = et.id ' \
              'JOIN employee e ON rr.employee_id = e.id'

        cursor = connection.cursor()
        cursor.execute(sql, [amount, request_id])
        record = cursor.fetchone()
        if record:
            return _get_full_request_info(record)
        else:
            raise ResourceNotFound('Request Not Found')



def _test():
    repo = RequestRepo()
    # print(repo.get_all_requests())
    # print(repo.get_requests_by_department(2))
    # print(repo.get_requests_by_supervisor(3))
    r = Request(employee_id=5,
                event_start_date=1653955200,
                event_end_date=1653955200,
                street='5555 Info Street',
                city='Teufort',
                state='NM',
                zip_code='11111',
                event_name='Explosive Web Design Principals',
                event_description='New web design principals that have been exploding in popularity',
                event_cost=120,
                event_type_id=5,
                missed_work_start=1653955200,
                missed_work_end=1653955200,
                grade_type='Pass/Fail',
                justification='I would like to update my knowledge in web design trends',
                amount=108)
    # print(repo.create_request(r))
    # request = repo.get_request(5)
    # request.event_start_date = 1654041600
    # request.event_end_date = 1654041600
    # request.missed_work_start = 1654041600
    # request.missed_work_end = 1654041600

    # print(repo.update_request(request))

    # repo.delete_request(5)
    # print(repo.get_request(5))


if __name__ == '__main__':
    _test()

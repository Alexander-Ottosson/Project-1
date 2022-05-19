from exceptions.resource_not_found import ResourceNotFound
from models.approval import Approval
from util.db_connection import connection
from util.object_builders import build_approval

_sql_select = 'SELECT ' \
              'a.id, ' \
              'a.appr_type, ' \
              'a.req_id, ' \
              'a.approved, ' \
              'a.approver_id, ' \
              'a.reason, ' \
              'aty.appr_type,' \
              'e.first_name, ' \
              'e.last_name, ' \
              'aty.id '


class ApprovalRepo:
    def get_approval(self, appr_id):
        sql = _sql_select + \
              'FROM approval a ' \
              'JOIN approval_type aty ON a.appr_type = aty.id ' \
              'JOIN employee e ON a.approver_id = e.id ' \
              'WHERE a.id = %s;'

        cursor = connection.cursor()
        cursor.execute(sql, [appr_id])
        record = cursor.fetchone()

        if record:
            return build_approval(record)
        else:
            raise ResourceNotFound('Approval Not Found')

    def get_approvals_by_request(self, req_id):
        sql = _sql_select + \
              'FROM approval a ' \
              'JOIN approval_type aty ON a.appr_type = aty.id ' \
              'JOIN employee e ON a.approver_id = e.id ' \
              'WHERE req_id = %s ' \
              'ORDER by a.appr_type;'

        cursor = connection.cursor()
        cursor.execute(sql, [req_id])
        records = cursor.fetchall()

        if records:
            return [build_approval(r) for r in records]
        else:
            return None

    def create_approvals(self, *approvals):
        sql = 'WITH new_approval AS ( ' \
              'INSERT INTO approval VALUES ' \
              '(DEFAULT, ' \
              '%(apprTypeId)s, ' \
              '%(requestId)s, ' \
              '%(approved)s, ' \
              '%(approverId)s, ' \
              '%(reason)s) RETURNING *' \
              ') ' + \
              _sql_select + \
              ' FROM new_approval AS a ' \
              'JOIN approval_type aty ON a.appr_type = aty.id ' \
              'JOIN employee e ON a.approver_id = e.id '

        cursor = connection.cursor()

        created_approvals = list()

        for appr in approvals:
            if appr:
                approval_dict = appr.json()
                cursor.execute(sql, approval_dict)
                record = cursor.fetchone()
                created_approvals.append(build_approval(record))

        connection.commit()

        if created_approvals:
            return created_approvals
        else:
            return None

    def update_approval(self, approval, user_id):
        sql = 'WITH upd_approval AS (' \
              'UPDATE approval SET ' \
              'approved = %(approved)s, ' \
              'reason = %(reason)s ' \
              'WHERE req_id = %(requestId)s ' \
              'AND approver_id = %(userId)s ' \
              'RETURNING * ' \
              ')' + \
              _sql_select + \
              ' FROM upd_approval AS a ' \
              'JOIN approval_type aty ON a.appr_type = aty.id ' \
              'JOIN employee e ON a.approver_id = e.id '

        cursor = connection.cursor()
        appr_dict = approval.json()
        appr_dict['userId'] = user_id
        cursor.execute(sql, appr_dict)

        records = cursor.fetchall()
        connection.commit()
        return [build_approval(r) for r in records]

    def delete_approval(self, approval_id):
        sql = 'DELETE FROM approval ' \
              'WHERE id = %s;'

        # Check to see if approval exists, should raise ResourceNotFound if it doesn't exist
        self.get_approval(approval_id)

        cursor = connection.cursor()
        cursor.execute(sql, [approval_id])
        connection.commit()

    def delete_approvals_by_request(self, req_id):
        sql = 'DELETE FROM approval ' \
              'WHERE req_id = %s;'

        cursor = connection.cursor()
        cursor.execute(sql, [req_id])
        connection.commit()

    def has_user_approved(self, req_id, employee_id):
        sql = 'SELECT COUNT(id) ' \
              'FROM approval ' \
              'WHERE req_id = %s AND approver_id = %s'

        cursor = connection.cursor()
        cursor.execute(sql, [req_id, employee_id])
        record = cursor.fetchone()
        if record[0] > 0:
            return True
        else:
            return False

def _test():
    ar = ApprovalRepo()
    #
    # print(ar.get_approvals_by_request(4))
    #
    approval1 = Approval(
        appr_type_id=2,
        request_id=1,
        approved=True,
        approver_id=1,
        reason=''
    )
    approval2 = Approval(
        appr_type_id=1,
        request_id=1,
        approved=True,
        approver_id=1,
        reason=''
    )
    approvals = ar.create_approvals(approval1, approval2)
    print(approvals)
    #
    # approval = ar.get_approval(1)
    # print(approval)
    #
    # approval.approved = False
    # approval.reason = 'I don\'t like this particular employee'
    #
    # print(ar.update_approval(approval))


if __name__ == '__main__':
    _test()

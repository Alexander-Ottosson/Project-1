class Approval:
    def __init__(
            self,
            appr_id=0,
            appr_type_id=0,
            request_id=0,
            approved=None,
            approver_id=0,
            reason='',
            appr_type='',
            approver_f_name='',
            approver_l_name=''
    ):
        self.appr_id = appr_id
        self.appr_type_id = appr_type_id
        self.request_id = request_id
        self.approved = approved
        self.approver_id = approver_id
        self.reason = reason
        self.appr_type = appr_type
        self.approver_f_name = approver_f_name
        self.approver_l_name = approver_l_name

    def json(self):
        return {
            'approvalId': self.appr_id,
            'apprTypeId': self.appr_type_id,
            'requestId': self.request_id,
            'approved': self.approved,
            'approverId': self.approver_id,
            'reason': self.reason,
            'apprType': self.appr_type,
            'approverFirstName': self.approver_f_name,
            'approverLastName': self.approver_l_name
        }

    def __repr__(self):
        return str(self.json())

    def __eq__(self, other):
        if not other:
            return False

        if not isinstance(other, Approval):
            return False

        for value1, value2 in zip(vars(self).values(), vars(other).values()):
            if value1 != value2:
                return False

        return True

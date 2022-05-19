class ApprovalType:
    def __init__(
            self,
            type_id=0,
            appr_type=''
    ):
        self.type_id = type_id
        self.appr_type = appr_type

    def json(self):
        return {
            'typeId': self.type_id,
            'approvalType': self.appr_type
        }

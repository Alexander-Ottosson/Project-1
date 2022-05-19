from repositories.approval_repo import ApprovalRepo


class ApprovalService:
    def __init__(self, approval_repo: ApprovalRepo):
        self.approval_repo = approval_repo

    def get_approval(self, appr_id):
        return self.approval_repo.get_approval(appr_id)

    def get_approvals_by_request(self, req_id):
        return self.approval_repo.get_approvals_by_request(req_id)

    def create_approval(self, *approvals):
        return self.approval_repo.create_approvals(*approvals)

    def update_approval(self, change, user_id):
        return self.approval_repo.update_approval(change, user_id)

    def delete_approval(self, appr_id):
        return self.approval_repo.delete_approval(appr_id)

    def delete_approval_by_request(self, req_id):
        return self.approval_repo.delete_approvals_by_request(req_id)

    def has_user_approved(self, req_id, employee_id):
        return self.approval_repo.has_user_approved(req_id, employee_id)

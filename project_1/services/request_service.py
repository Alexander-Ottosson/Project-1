from repositories.request_repo import RequestRepo


class RequestService:
    def __init__(self, request_repo: RequestRepo):
        self.request_repo = request_repo

    def get_requests_by_user(self, user_id):
        return self.request_repo.get_requests_by_employee(user_id)

    def get_all_requests(self):
        return self.request_repo.get_all_requests()

    def get_requests_by_department(self, dept_id):
        return self.request_repo.get_requests_by_department(dept_id)

    def get_requests_by_supervisor(self, sup_id):
        return self.request_repo.get_requests_by_supervisor(sup_id)

    def get_request(self, req_id):
        return self.request_repo.get_request(req_id)

    def create_request(self, request, *approvals):
        return self.request_repo.create_request(request, *approvals)

    def update_request(self, change):
        return self.request_repo.update_request(change)

    def update_amount(self, amount, request_id):
        return self.request_repo.update_amount(amount, request_id)

    def delete_request(self, req_id):
        return self.request_repo.delete_request(req_id)

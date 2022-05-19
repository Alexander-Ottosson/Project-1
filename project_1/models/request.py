class Request:
    def __init__(
            self,
            request_id=0,
            employee_id=0,
            event_start_date=0,
            event_end_date=0,
            street='',
            city='',
            state='',
            zip_code='',
            event_name='',
            event_description='',
            event_cost=0,
            event_type_id=0,
            event_type_name='',
            missed_work_start=0,
            missed_work_end=0,
            grade_type='',
            justification='',
            amount=0,
            employee_f_name='',
            employee_l_name='',
            approvals=None
    ):
        if approvals is None:
            approvals = []
        self.request_id = request_id
        self.employee_id = employee_id
        self.event_start_date = event_start_date
        self.event_end_date = event_end_date
        self.street = street
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.event_name = event_name
        self.event_description = event_description
        self.event_cost = event_cost
        self.event_type_id = event_type_id
        self.event_type_name = event_type_name
        self.missed_work_start = missed_work_start
        self.missed_work_end = missed_work_end
        self.grade_type = grade_type
        self.justification = justification
        self.reimbursement_amount = amount
        self.employee_f_name = employee_f_name
        self.employee_l_name = employee_l_name
        self.approvals = approvals

    def json(self):
        return {
            'requestId': self.request_id,
            'employeeId': self.employee_id,
            'eventStartDate': self.event_start_date,
            'eventEndDate': self.event_end_date,
            'street': self.street,
            'city': self.city,
            'state': self.state,
            'zipCode': self.zip_code,
            'eventName': self.event_name,
            'eventDescription': self.event_description,
            'eventCost': self.event_cost,
            'eventTypeId': self.event_type_id,
            'missedWorkStart': self.missed_work_start,
            'missedWorkEnd': self.missed_work_end,
            'gradeType': self.grade_type,
            'justification': self.justification,
            'amount': self.reimbursement_amount,
            'employeeFirstName': self.employee_f_name,
            'employeeLastName': self.employee_l_name,
            'approvals': [a.json() for a in self.approvals]
        }

    def __repr__(self):
        return str(self.json())

    def __eq__(self, other):
        if not other:
            return False

        if not isinstance(other, Request):
            return False

        for value1, value2 in zip(vars(self).values(), vars(other).values()):
            if value1 != value2:
                return False

        return True

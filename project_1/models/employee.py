class Employee:
    # TODO: de-normalize database so that employee has fields for is_dept_head and is_benco

    def __init__(
            self,
            employee_id=0,
            first_name='',
            last_name='',
            dept_id='',
            username='',
            password='',
            is_dept_head=False,
            is_benco=False,
            contact_info_ids=None,
            subordinate_ids=None
    ):
        if contact_info_ids is None:
            contact_info_ids = []
        if subordinate_ids is None:
            subordinate_ids = []
        self.employee_id = employee_id
        self.first_name = first_name
        self.last_name = last_name
        self.dept_id = dept_id
        self.username = username
        self.password = password
        self.contact_info_ids = contact_info_ids
        self.subordinate_ids = subordinate_ids
        self.is_dept_head = is_dept_head
        self.is_benco = is_benco

    def json(self):
        return {
            'employeeId': self.employee_id,
            'firstName': self.first_name,
            'lastName': self.last_name,
            'deptId': self.dept_id,
            'username': self.username,
            'password': self.password,
            'isDeptHead': self.is_dept_head,
            'isBenCo': self.is_benco,
            'contactInfoIds': self.contact_info_ids,
            'subordinateIds': self.subordinate_ids
        }

    def __repr__(self):
        return str(self.json())

    def __eq__(self, other):
        if not other:
            return False

        if not isinstance(other, Employee):
            return False

        for value1, value2 in zip(vars(self).values(), vars(other).values()):
            if value1 != value2:
                return False

        return True

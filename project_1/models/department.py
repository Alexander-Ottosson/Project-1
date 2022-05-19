class Department:
    def __init__(
            self,
            dept_id=0,
            name='',
            dept_head_id=0
    ):
        self.dept_id = dept_id
        self.name = name
        self.dept_head_id = dept_head_id

    def json(self):
        return {
            'deptId': self.dept_id,
            'name': self.name,
            'deptHeadId': self.dept_head_id
        }

    def __repr__(self):
        return str(self.json())

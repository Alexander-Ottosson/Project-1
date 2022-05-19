class ContactInfo:
    def __init__(
            self,
            info_id=0,
            contact='',
            type_id=0,
            info_type='',
            employee_id=0
    ):
        self.info_id = info_id
        self.contact_info = contact
        self.type_id = type_id
        self.info_type = info_type
        self.employee_id = employee_id

    def json(self):
        return {
            'infoId': self.info_id,
            'contactInfo': self.contact_info,
            'typeId': self.type_id,
            'infoType': self.info_type,
            'employeeId': self.employee_id
        }

    def __repr__(self):
        return str(self.json())

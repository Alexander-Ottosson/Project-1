class ContactInfoType:
    def __init__(
            self,
            type_id,
            info_type
    ):
        self.type_id = type_id
        self.info_type = info_type

    def json(self):
        return {
            'typeId': self.type_id,
            'infoType': self.info_type
        }

    def __repr__(self):
        return str(self.json())

class JustificationType:
    def __init__(
            self,
            type_id=0,
            name=''
    ):
        self.type_id = type_id
        self.name = name

    def json(self):
        return {
            'typeId': self.type_id,
            'name': self.name
        }

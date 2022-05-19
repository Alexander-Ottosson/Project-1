class EventType:
    def __init__(
            self,
            type_id=0,
            name='',
            coverage=0
    ):
        self.type_id = type_id
        self.name = name
        self.coverage = coverage

    def json(self):
        return {
            'typeId': self.type_id,
            'name': self.name,
            'coverage': self.coverage
        }

    def __repr__(self):
        return str(self.json())

    def __eq__(self, other):
        if not other:
            return False

        if not isinstance(other, EventType):
            return False

        for value1, value2 in zip(vars(self).values(), vars(other).values()):
            if value1 != value2:
                return False

        return True

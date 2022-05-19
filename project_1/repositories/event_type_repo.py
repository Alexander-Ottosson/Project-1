from exceptions.resource_not_found import ResourceNotFound
from util.db_connection import connection
from util.object_builders import build_event_type


class EventTypeRepo:
    def get_all_types(self):
        sql = 'SELECT * FROM event_type;'

        cursor = connection.cursor()
        cursor.execute(sql)
        records = cursor.fetchall()

        return [build_event_type(r) for r in records]

    def get_type_by_id(self, type_id):
        sql = 'SELECT * FROM event_type ' \
              'WHERE id = %s;'

        cursor = connection.cursor()
        cursor.execute(sql, [type_id])
        record = cursor.fetchone()
        if record:
            return build_event_type(record)
        else:
            raise ResourceNotFound('Event Type Not Found')

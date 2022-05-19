from models.contact_info import ContactInfo
from util.db_connection import connection
from util.object_builders import build_contact_info

select_sql = 'SELECT ' \
              'ci.id, ' \
              'ci.contact_info, ' \
              'ci.type_id, ' \
              'cit.info_type, ' \
              'ci.employee_id ' \
              'FROM contact_info ci ' \
              'JOIN contact_info_type cit ON ci.type_id = cit.id '


class ContactInfoRepo:
    def get_info_by_id(self, info_id):
        sql = select_sql + \
              'WHERE ci.id = %s;'

        cursor = connection.cursor()
        cursor.execute(sql, [info_id])
        record = cursor.fetchone()
        return build_contact_info(record)

    def get_by_employee_id(self, employee_id):
        sql = select_sql + \
              'WHERE ci.employee_id = %s;'

        cursor = connection.cursor()
        cursor.execute(sql, [employee_id])
        records = cursor.fetchall()
        return [build_contact_info(r) for r in records]


from models.approval import Approval
from models.contact_info import ContactInfo
from models.employee import Employee
from models.event_type import EventType
from models.request import Request


def build_employee(record, cii, si):
    return Employee(
        employee_id=record[0],
        first_name=record[1],
        last_name=record[2],
        dept_id=record[3],
        username=record[4],
        password=record[5],
        is_dept_head=record[6],
        is_benco=record[7],
        contact_info_ids=cii,
        subordinate_ids=si,
    )


def build_contact_info(record):
    return ContactInfo(
        info_id=record[0],
        contact=record[1],
        type_id=record[2],
        info_type=record[3],
        employee_id=record[4]
    )


def build_request(record, approvals=None):
    if approvals is None:
        approvals = []
    return Request(
        request_id=int(record[0]),
        employee_id=int(record[1]),
        event_start_date=int(record[2]),
        event_end_date=int(record[3]),
        street=record[4],
        city=record[5],
        state=record[6],
        zip_code=record[7],
        event_name=record[8],
        event_description=record[9],
        event_cost=float(record[10]),
        event_type_id=int(record[11]),
        event_type_name=record[12],
        missed_work_start=int(record[13]),
        missed_work_end=int(record[14]),
        grade_type=record[15],
        justification=record[16],
        amount=float(record[17]),
        employee_f_name=record[18],
        employee_l_name=record[19],
        approvals=approvals)


def build_approval(record):
    return Approval(
        appr_id=record[0],
        appr_type_id=record[1],
        request_id=record[2],
        approved=record[3],
        approver_id=record[4],
        reason=record[5],
        appr_type=record[6],
        approver_f_name=record[7],
        approver_l_name=record[8]
    )


def build_event_type(record):
    return EventType(
        type_id=record[0],
        name=record[1],
        coverage=float(record[2])
    )

import unittest

from exceptions.resource_not_found import ResourceNotFound
from models.approval import Approval
from models.request import Request
from repositories.request_repo import RequestRepo
from services.request_service import RequestService
unittest.TestLoader.sortTestMethodsUsing = None


# PLEASE RUN THE SQL CREATE STATEMENTS FILE BEFORE RUNNING


class TestRequestService(unittest.TestCase):
    rr = RequestRepo()
    rs = RequestService(rr)

    # tests are named as test_<letter> so they execute in the correct order
    def test_a_get_all_requests(self):
        requests = self.rs.get_all_requests()
        self.assertEqual(len(requests), 3)

    def test_b_get_dept_requests(self):
        requests = self.rs.get_requests_by_department(1)
        self.assertEqual(len(requests), 3)

        # There should be no requests
        requests = self.rs.get_requests_by_department(2)
        self.assertEqual(requests, None)

    def test_c_get_sup_requests(self):
        requests = self.rs.get_requests_by_supervisor(3)
        self.assertEqual(len(requests), 2)

        requests = self.rs.get_requests_by_supervisor(1)
        self.assertEqual(len(requests), 1)

        requests = self.rs.get_requests_by_supervisor(2)
        self.assertEqual(requests, None)

    def test_d_get_request(self):
        request = self.rs.get_request(1)
        exp_request = Request(
            request_id=1,
            employee_id=3,
            event_start_date=1652313600000,
            event_end_date=1652313600000,
            street='2222, Strt CC',
            city='NormalCity',
            state='FL',
            zip_code='55555',
            event_name='CSS Grid and You',
            event_description='A Seminar if innovative ways of using CSS grid for UI design',
            event_cost=100.0,
            event_type_id=2,
            event_type_name='Seminar',
            missed_work_start=1652313600000,
            missed_work_end=1652313600000,
            grade_type='Presentation',
            justification='I think it is good to keep up with current web design trends',
            amount=60.0,
            employee_f_name='John',
            employee_l_name='Doe'
        )

        print(request)
        print(exp_request)

        self.assertEqual(request, exp_request)

    def test_e_neg_get_request(self):
        try:
            request = self.rs.get_request(1000)
        except ResourceNotFound as e:
            self.assertEqual(e.message, 'Request Not Found')

    def test_f_create_request(self):
        request = self.rs.create_request(
            Request(employee_id=5,
                    event_start_date=1653955200000,
                    event_end_date=1653955200000,
                    street='5555 Info Street',
                    city='Teufort',
                    state='NM',
                    zip_code='11111',
                    event_name='Explosive Web Design Principals',
                    event_description='New web design principals that have been exploding in popularity',
                    event_cost=120,
                    event_type_id=5,
                    missed_work_start=1653955200000,
                    missed_work_end=1653955200000,
                    grade_type='Pass/Fail',
                    justification='I would like to update my knowledge in web design trends',
                    amount=108))
        self.assertEqual(
            request,
            Request(
                request_id=request.request_id,
                employee_id=5,
                event_start_date=1653955200000,
                event_end_date=1653955200000,
                street='5555 Info Street',
                city='Teufort',
                state='NM',
                zip_code='11111',
                event_name='Explosive Web Design Principals',
                event_description='New web design principals that have been exploding in popularity',
                event_cost=120.0,
                event_type_id=5,
                event_type_name='Technical Training',
                missed_work_start=1653955200000,
                missed_work_end=1653955200000,
                grade_type='Pass/Fail',
                justification='I would like to update my knowledge in web design trends',
                amount=108,
                employee_f_name='Tavish',
                employee_l_name='DeGroot'
            ))

        request = self.rs.create_request(
            Request(
                employee_id=1,
                event_start_date=1653868800000,
                event_end_date=1653868800000,
                street='444 Highway Road',
                city='Beeg City',
                state='FL',
                zip_code='21212',
                event_name='Team Management 101',
                event_description='A seminar that discusses important skills for managing a team',
                event_cost=200,
                event_type_id=2,
                missed_work_start=1653868800000,
                missed_work_end=1653868800000,
                grade_type='Presentation',
                justification='I would like to learn how to manage my team better'
            ),
            Approval(
                approver_id=1,
                appr_type_id=2,
                approved=True
            ),
            Approval(
                approver_id=1,
                appr_type_id=1,
                approved=True
            ))
        print(request.approvals[0])
        print(request.approvals[1])
        print(Approval(
                appr_id=request.approvals[0].appr_id,
                request_id=request.request_id,
                appr_type_id=2,
                approved=True,
                approver_id=1,
                reason='',
                appr_type='Department Head Approval'
            ))
        print(Approval(
                appr_id=request.approvals[1].appr_id,
                request_id=request.request_id,
                appr_type_id=1,
                approved=True,
                approver_id=1,
                reason='',
                appr_type='Supervisor Approval'
            ))
        self.assertListEqual(request.approvals, [
            Approval(
                appr_id=request.approvals[0].appr_id,
                request_id=request.request_id,
                appr_type_id=1,
                approved=True,
                approver_id=1,
                reason='',
                approver_f_name='Alexander',
                approver_l_name='Ottosson',
                appr_type='Supervisor Approval'
            ),
            Approval(
                appr_id=request.approvals[1].appr_id,
                request_id=request.request_id,
                appr_type_id=2,
                approved=True,
                approver_id=1,
                reason='',
                approver_f_name='Alexander',
                approver_l_name='Ottosson',
                appr_type='Department Head Approval'
            )
        ])

    def test_g_update_request(self):
        old_request = self.rs.get_request(4)

        new_request1 = old_request

        new_request1.event_start_date = 1653868800000
        new_request1.event_end_date = 1653868800000
        new_request1.missed_work_start = 1653868800000
        new_request1.missed_work_end = 1653868800000

        new_request2 = self.rs.update_request(new_request1)

        self.assertEqual(new_request1, new_request2)

    def test_h_neg_update_request(self):
        try:
            request = self.rs.update_request(Request(request_id=1000))
        except ResourceNotFound as e:
            self.assertEqual(e.message, 'Request Not Found')

    def test_i_delete_request(self):
        self.rs.delete_request(5)

        try:
            self.rs.get_request(5)
            self.assertEqual(1, 2)
        except ResourceNotFound as e:
            self.assertEqual(e.message, 'Request Not Found')

    def test_j_neg_delete_request(self):
        try:
            self.rs.delete_request(10000)
        except ResourceNotFound as e:
            self.assertEqual(e.message, 'Request Not Found')


import unittest

from exceptions.resource_not_found import ResourceNotFound
from models.approval import Approval
from repositories.approval_repo import ApprovalRepo
from services.approval_service import ApprovalService
unittest.TestLoader.sortTestMethodsUsing = None

# PLEASE RUN THE SQL CREATE STATEMENTS FILE BEFORE RUNNING


class TestApprovalService(unittest.TestCase):
    ar = ApprovalRepo()
    aps = ApprovalService(ar)

    # tests are named as test_<letter> so they execute in the correct order
    def test_a_get_approval(self):
        approval = self.aps.get_approval(1)
        self.assertEqual(approval, Approval(
            appr_id=1,
            appr_type_id=1,
            request_id=2,
            approved=True,
            approver_id=3,
            appr_type='Supervisor Approval',
            approver_f_name='John',
            approver_l_name='Doe'
        ))

    def test_b_neg_get_approval(self):
        try:
            self.aps.get_approval(1000000)
        except ResourceNotFound as e:
            self.assertEqual(e.message, 'Approval Not Found')

    def test_c_get_approval_by_request(self):
        approvals = self.aps.get_approvals_by_request(2)
        self.assertEqual(len(approvals), 3)

    def test_d_create_approval(self):
        approval = Approval(
            appr_type_id=3,
            request_id=3,
            approved=True,
            approver_id=2,
            reason=''
        )
        approval = self.aps.create_approval(approval)
        self.assertListEqual(
            approval,
            [Approval(
                appr_id=approval[0].appr_id,
                appr_type_id=3,
                request_id=3,
                appr_type='Benefits Coordinator Approval',
                approved=True,
                approver_id=2,
                reason='',
                approver_f_name='Benni',
                approver_l_name='Fittz'
            )]
        )

    def test_e_create_multiple_approvals(self):
        approval1 = Approval(
            appr_type_id=2,
            request_id=1,
            approved=True,
            approver_id=1,
            reason=''
        )
        approval2 = Approval(
            appr_type_id=1,
            request_id=1,
            approved=True,
            approver_id=1,
            reason=''
        )
        approvals = self.aps.create_approval(approval1, approval2)
        self.assertListEqual(approvals, [
            Approval(
                appr_id=approvals[0].appr_id,
                request_id=1,
                appr_type_id=2,
                appr_type='Department Head Approval',
                approved=True,
                approver_id=1,
                reason='',
                approver_f_name='Alexander',
                approver_l_name='Ottosson'
             ),
            Approval(
                appr_id=approvals[1].appr_id,
                request_id=1,
                appr_type_id=1,
                appr_type='Supervisor Approval',
                approved=True,
                approver_id=1,
                reason='',
                approver_f_name='Alexander',
                approver_l_name='Ottosson'
            )
        ])

    def test_f_update_approval(self):
        old_approval = self.aps.get_approval(4)

        new_approval1 = old_approval
        new_approval1.approved = False
        new_approval1.reason = 'Reason goes here'
        new_approval2 = self.aps.update_approval(new_approval1, new_approval1.approver_id)
        self.assertListEqual([new_approval1], new_approval2)

    def test_g_delete_approval(self):
        try:
            self.aps.delete_approval(4)
        except ResourceNotFound as e:
            # The approval to delete was not found
            self.assertEqual(1, 2)

        try:
            self.aps.get_approval(4)
        except ResourceNotFound as e:
            self.assertEqual(e.message, 'Approval Not Found')

    def test_h_neg_delete_approval(self):
        try:
            self.aps.delete_approval(100000)
        except ResourceNotFound as e:
            # The approval to delete was not found
            self.assertEqual(e.message, 'Approval Not Found')

    def test_i_delete_by_request(self):
        self.aps.delete_approval_by_request(1)
        approvals = self.aps.get_approvals_by_request(1)
        self.assertEqual(approvals, None)

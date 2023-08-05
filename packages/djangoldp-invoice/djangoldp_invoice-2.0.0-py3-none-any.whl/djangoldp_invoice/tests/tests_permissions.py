import uuid
import json
from datetime import datetime, timedelta

from django.urls import reverse
from djangoldp.permissions import LDPPermissions

from djangoldp.serializers import LDListMixin, LDPSerializer
from rest_framework.test import APITestCase, APIClient
from guardian.shortcuts import assign_perm

from djangoldp_project.models import Project, Member
from djangoldp_invoice.models import Task, Batch, FreelanceInvoice, CustomerInvoice
from djangoldp_invoice.tests.models import User


class PermissionsTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        LDListMixin.to_representation_cache.reset()
        LDPSerializer.to_representation_cache.reset()
        # LDPPermissions.invalidate_cache()

    def setUpLoggedInUser(self):
        self.user = User(email='test@mactest.co.uk', first_name='Test', last_name='Mactest', username='test',
                         password='glass onion')
        self.user.save()
        self.client.force_authenticate(user=self.user)

    def _get_random_project(self):
        return Project.objects.create(name=str(uuid.uuid4()), status='Public')

    def _get_random_customer_invoice(self, project=None, customer=None):
        return CustomerInvoice.objects.create(project=project, customer=customer, identifier=str(uuid.uuid4()),
                                              title=str(uuid.uuid4()), tvaRate=20)

    def _get_random_user(self):
        return User.objects.create(email='{}@test.co.uk'.format(str(uuid.uuid4())), first_name='Test', last_name='Test',
                                   username=str(uuid.uuid4()))

    # accessing the invoices directly - whether anonymous or authenticated, should return empty list
    def test_list_invoices_anonymous_user(self):
        self._get_random_customer_invoice()

        response = self.client.get('/customer-invoices/')
        self.assertEqual(response.status_code, 403)

    # accessing the invoices directly - whether anonymous or authenticated, should return empty list
    def test_list_invoices_authenticated(self):
        self.setUpLoggedInUser()
        self._get_random_customer_invoice()

        response = self.client.get('/customer-invoices/')
        self.assertEqual(response.status_code, 403)

    # accessing in a nested object (project) is OK if I am authenticated
    def test_list_invoice_nested_in_project_anonymous(self):
        project = self._get_random_project()
        self._get_random_customer_invoice(project=project)

        response = self.client.get('/projects/{}/customerInvoices/'.format(project.pk))
        self.assertEqual(response.status_code, 403)

    # accessing in a nested object (project) is OK if I am authenticated
    def test_list_invoice_nested_in_project_authenticated(self):
        self.setUpLoggedInUser()
        project = self._get_random_project()
        self._get_random_customer_invoice(project=project)

        response = self.client.get('/projects/{}/customerInvoices/'.format(project.pk))
        self.assertEqual(response.status_code, 200)
        self.assertIn('ldp:contains', response.data)
        self.assertEqual(len(response.data['ldp:contains']), 1)

    def test_get_invoice_anonymous_user(self):
        invoice = self._get_random_customer_invoice()

        response = self.client.get('/customer-invoices/{}/'.format(invoice.pk))
        self.assertEqual(response.status_code, 403)

    def test_get_invoice_authenticated(self):
        self.setUpLoggedInUser()
        invoice = self._get_random_customer_invoice()

        response = self.client.get('/customer-invoices/{}/'.format(invoice.pk))
        self.assertEqual(response.status_code, 200)

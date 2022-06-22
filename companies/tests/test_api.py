from urllib import response
import pytest
import json
from unittest import TestCase

from django.urls import reverse
from django.test import Client
from companies.models import Company


'''class for generic initializer'''
class BasicCompanyAPITestCase(TestCase):
    # set to hold all duplicate code(this runs before our other tests run)
    def setUp(self) -> None:
        self.client = Client()
        self.companies_url = reverse("companies-list")

    '''this runs after our tests have run'''
    def tearDown(self) -> None:
        pass

# django_db ---test database
@pytest.mark.django_db
class TestGetCompanies(BasicCompanyAPITestCase):

    """test with zero companies"""

    def test_zero_companies_should_return_empty_list(self):
        """similar to postman sending post and get requests"""
        # client = Client()
        """similar to placing http://localhost:8000/companies"""
        # companies_url = reverse("companies-list")
        response = self.client.get(self.companies_url)
        self.assertEqual(response.status_code, 200)
        """load json package"""
        self.assertEqual(json.loads(response.content), [])

    def test_one_company_should_exist(self) -> None:
        """create a company in our db"""
        # client = Client()
        test_company = Company.objects.create(name='Amazon')
        # companies_url = reverse("companies-list")
        response = self.client.get(self.companies_url)
        # get the response body
        response_content = json.loads(response.content)[0]
        self.assertEqual(response.status_code, 200)
        # assert the name of company is amazon
        self.assertEqual(response_content.get('name'), test_company.name)
        self.assertEqual(response_content.get('status'), test_company.status)
        self.assertEqual(response_content.get('application_link'), test_company.application_link)
        self.assertEqual(response_content.get('notes'), test_company.notes)

'''test post functionality'''
# django_db ---test database
@pytest.mark.django_db
class TestPostCompanies(BasicCompanyAPITestCase):
    'create a company without arguments'
    def test_create_company_arguments_should_fail(self) -> None:
        '''here we can add data to it, wch is our json payload'''
        response = self.client.post(path=self.companies_url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content), {'name': ['This field is required.']}
        )
    '''create existing company should fail'''
    def test_create_existing_company_fails(self) -> None:
          Company.objects.create(name='betterdata')
          response = self.client.post(path=self.companies_url, data={'name': 'betterdata'})
          self.assertEqual(response.status_code, 400)
          self.assertEqual(
              json.loads(response.content),
              {'name': ['company with this name already exists.']}
          )

    def test_create_company_with_only_name_all_fields_should_be_default(self) -> None:
        response = self.client.post(path=self.companies_url, data={'name': 'test company name'})
        self.assertEqual(response.status_code, 201)
        response_content = json.loads(response.content)
        self.assertEqual(response_content.get('name'), 'test company name')
        self.assertEqual(response_content.get('status'), 'Hiring')
        self.assertEqual(response_content.get('application_link'), '')
        self.assertEqual(response_content.get('notes'), '')

    def test_create_company_with_layoffs_status_should_succed(self) -> None:
        '''assert that we are creating the layoff status'''
        response = self.client.post(path=self.companies_url, data={'name': 'test company name', 'status': 'Layoffs'})
        response_content = json.loads(response.content)
        self.assertEqual(response_content.get('status'), 'Layoffs')

    def test_create_company_with_wrong_status(self) -> None:
        response = self.client.post(path=self.companies_url, data={'name': 'test company name', 'status': 'WrongStatus'})
        self.assertEqual(response.status_code, 400)
        # assert that wrong status in our response
        self.assertIn('WrongStatus', str(response.content))
        #   checks that is not a valid choice is not in response.content string
        self.assertIn('is not a valid choice', str(response.content))

    # test that may pass or not 
    @pytest.mark.xfail
    def test_should_be_ok_if_fails(self) -> None:
        self.assertEqual(1, 2)

    @pytest.mark.skip
    def test_should_be_ok_if_fails(self) -> None:
        self.assertEqual(1, 2)
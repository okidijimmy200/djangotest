import pytest
import json

from django.urls import reverse
from companies.models import Company

companies_url = reverse("companies-list")
pytestmark = pytest.mark.django_db # this sets a python fixture for every function in this file


"""test with zero companies"""
def test_zero_companies_should_return_empty_list(client): # client is a param from pytest-django and works as Client from Django
    """similar to postman sending post and get requests"""
    # client = Client()
    """similar to placing http://localhost:8000/companies"""
    # companies_url = reverse("companies-list")
    response = client.get(companies_url)
    assert response.status_code == 200
    """load json package"""
    assert json.loads(response.content) == []

def test_one_company_should_exist(client) -> None:
    """create a company in our db"""
    # client = Client()
    test_company = Company.objects.create(name='Amazon')
    # companies_url = reverse("companies-list")
    response = client.get(companies_url)
    # get the response body
    response_content = json.loads(response.content)[0]
    assert response.status_code == 200
    # assert the name of company is amazon
    assert response_content.get('name') == test_company.name
    assert response_content.get('status') == test_company.status
    assert response_content.get('application_link') == test_company.application_link
    assert response_content.get('notes') == test_company.notes

'''test post functionality'''

'create a company without arguments'
def test_create_company_arguments_should_fail(client) -> None:
    '''here we can add data to it, wch is our json payload'''
    response = client.post(path=companies_url)
    assert response.status_code == 400
    assert json.loads(response.content) == {'name': ['This field is required.']}
    
'''create existing company should fail'''
def test_create_existing_company_fails(client) -> None:
        Company.objects.create(name='betterdata')
        response = client.post(path=companies_url, data={'name': 'betterdata'})
        assert response.status_code == 400
        assert json.loads(response.content) == {'name': ['company with this name already exists.']}
        

def test_create_company_with_only_name_all_fields_should_be_default(client) -> None:
    response = client.post(path=companies_url, data={'name': 'test company name'})
    assert response.status_code == 201
    response_content = json.loads(response.content)
    assert response_content.get('name') == 'test company name'
    assert response_content.get('status') == 'Hiring'
    assert response_content.get('application_link') == ''
    assert response_content.get('notes') == ''

def test_create_company_with_layoffs_status_should_succed(client) -> None:
    '''assert that we are creating the layoff status'''
    response = client.post(path=companies_url, data={'name': 'test company name', 'status': 'Layoffs'})
    response_content = json.loads(response.content)
    assert response_content.get('status') == 'Layoffs'

def test_create_company_with_wrong_status(client) -> None:
    response = client.post(path=companies_url, data={'name': 'test company name', 'status': 'WrongStatus'})
    assert response.status_code, 400
    # assert that wrong status in our response
    assert 'WrongStatus' in str(response.content)
    #   checks that is not a valid choice is not in response.content string
    assert 'is not a valid choice' in str(response.content)

# test that may pass or not 
@pytest.mark.xfail
def test_should_be_ok_if_fails() -> None:
    assert 1 == 2

@pytest.mark.skip
def test_should_be_ok_if_fails() -> None:
    assert 1 == 2
from . models import Contact
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse



class ContactTestCase(APITestCase):

    """
    Test suite for Contact
    """
    
    def setUp(self):
        self.client = APIClient()
        self.data = {
            "name": "Billy Smith",
            "message": "This is a test message",
            "email": "billysmith@test.com"
        }
        self.url = '/contact/'
    def test_create_contact(self):
        """
        Test creating a new contact
        """
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Contact.objects.count(), 1)
        self.assertEqual(Contact.objects.get().name, "Billy Smith")


    def test_create_contact_without_name(self):
        '''
        test ContactViewSet create method when name is not in data
        '''
        data = self.data
        data.pop("name")
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_contact_when_name_equals_blank(self):
        '''
        test ContactViewSet create method when name is blank
        '''
        data = self.data
        data["name"] = ""
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_create_contact_without_message(self):
    #     '''
    #     test ContactViewSet create method when message is not in data
    #     '''
    #     data = self.data
    #     data.pop("message")
    #     response = self.client.post(self.url, data, format='json')
    #     print(response.status_code)
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    # def test_create_contact_when_message_equals_blank(self):
    #     '''
    #     test ContactViewSet create method when message is blank
    #     '''
    #     data = self.data
    #     data["message"] = ""
    #     response = self.client.post(self.url, data)
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_create_contact_without_email(self):
    #     '''
    #     test ContactViewSet create method when email is not in data
    #     '''
    #     data = self.data
    #     data.pop("email")
    #     response = self.client.post(self.url, data)
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    # def test_create_contact_when_email_equals_blank(self):
    #     '''
    #     test ContactViewSet create method when email is blank
    #     '''
    #     data = self.data
    #     data["email"] = ""
    #     response = self.client.post(self.url, data)
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_create_contact_when_email_equals_non_email(self):
    #     '''
    #     test ContactViewSet create method when email is not email
    #     '''
    #     data = self.data
    #     data["email"] = "test"
    #     response = self.client.post(self.url, data)
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
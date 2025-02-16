from django.test import TestCase
from .forms import AccountRegisterForm
# Create your tests here.

class TestAccountRegisterForm(TestCase):
    def test_valid_form(self):
        form = AccountRegisterForm(data={
            'username': 'test',
            'email': 'john.doe@example.com',
            'password': '<PASSWORD>',
            'confirm_password': '<PASSWORD>',
        })
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = AccountRegisterForm(data={
            'username': '',
            'email': 'invalid email',
            'password': '',
            'confirm_password': '',
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)

    def test_clean_confirm_password_valid(self):
        form = AccountRegisterForm(data={
            'username': 'test',
            'email': 'john.doe@example.com',
            'password': '<PASSWORD>',
            'confirm_password': '<PASSWORD>',
        })
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['confirm_password'], form.cleaned_data['password'])

    def test_clean_confirm_password_invalid(self):
        form = AccountRegisterForm(data={
            'username': 'test',
            'email': 'john.doe@example.com',
            'password': '<PASSWORD>',
            'confirm_password': '<PASSWOR>',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('confirm_password', form.errors)


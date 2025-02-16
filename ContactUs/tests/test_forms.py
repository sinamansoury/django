from django.test import TestCase
from ..forms import ContactUsModelForm


class TestContactUsModelForm(TestCase):
    def test_valid_form(self):
        form = ContactUsModelForm(data={
            'fullname': 'sina',
            'email': 'john.doe@example.com',
            'title': 'Test Title',
            'message': 'This is a test message.'
        })
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = ContactUsModelForm(data={
            'fullname': '',
            'email': 'invalid email',
            'title': '',
            'message': ''
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)

    def test_form_widget(self):
        form = ContactUsModelForm(data={})
        self.assertEqual(form.fields['fullname'].widget.attrs['class'], 'form-control')
        self.assertEqual(form.fields['fullname'].widget.attrs['placeholder'], 'نام و نام خانوادگی')


    def test_error_message(self):
        form = ContactUsModelForm(data={})
        form.is_valid()  # صراحتاً اعتبارسنجی انجام می‌شود
        self.assertEqual(form.errors['fullname'], ['لطفا نام و نام خانوادکی خود را بنویسید'])


from django.test import TestCase, Client
from django.urls import reverse

from ..forms import ContactUsModelForm
from ..views import ContactUsCreateView


class TestContactUsCreateView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_contact_us_create_view_GET(self):
        response = self.client.get(reverse('contact_us'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shared/contact_us_page.html')
        self.assertIsInstance(response.context['form'], ContactUsModelForm)

    def test_contact_us_create_view_POST_valid(self):
        response = self.client.post(reverse('contact_us'), data={
            'fullname':'sina',
            'email':'john.doe@example.com',
            'title':'sina',
            'message':'sina',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('contact_us'))

    def test_contact_us_create_view_POST_invalid(self):
        response = self.client.post(reverse('contact_us'), data={
            'fullname': 'sina',
            'email': '',
            'title': 'sina',
            'message': 'sina',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shared/contact_us_page.html')
        self.assertIsInstance(response.context['form'], ContactUsModelForm)
        self.assertFalse(response.context['form'].is_valid())
        self.assertFormError(response.context['form'], 'email', 'لطفا ایمیل خود را بنویسید')
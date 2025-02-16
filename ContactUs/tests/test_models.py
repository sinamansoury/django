from django.template.defaultfilters import title
from django.test import TestCase
from ..models import ContactUs
from model_bakery import baker

class TestContactUs(TestCase):
    def setUp(self):
        self.ContactUs = baker.make(ContactUs ,title = 'مشکل خرید')

    def test_contactus(self):
        model = self.ContactUs
        self.assertEqual(str(model) , 'مشکل خرید')
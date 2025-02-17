from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from .views import EditUserInfo
from django.urls import reverse
from .forms import EditInfoForm


User = get_user_model()
# Create your tests here.
class TestEditUserInfo(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user_test', email='test@example.com', password='123')
        self.client = Client()
        self.client.login(username='user_test', password='123')

    def test_edit_user_info_get(self):
        response = self.client.get(reverse('Edit-profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'User_panel/edit-info-page.html')
        self.assertIsInstance(response.context['form'], EditInfoForm)

    def test_edit_user_info_post(self):
        response = self.client.post(reverse('Edit-profile'), {
            'first_name':'user_test',
            'email':'snam@snam.com'
        })
        self.assertTrue(response.context['form'].is_valid())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'User_panel/edit-info-page.html')
        self.assertIsInstance(response.context['form'], EditInfoForm)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'user_test')
        self.assertEqual(self.user.email, 'snam@snam.com')

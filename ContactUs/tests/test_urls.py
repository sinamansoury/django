from django.test import SimpleTestCase, TestCase
from django.urls import reverse, resolve
from ..views import ContactUsCreateView, ProfileImagesCreateView, ContactUsUploadFileView

class TestContactUsUrls(SimpleTestCase):
    def test_contact_us_create_view(self):
        url = reverse('contact_us')
        self.assertEqual(resolve(url).func.view_class, ContactUsCreateView)

    def test_contact_us_upload_file_view(self):
        url = reverse('ContactUsProfile')
        self.assertEqual(resolve(url).func.view_class, ContactUsUploadFileView)

    def test_profile_images_create_view(self):
        url = reverse('ProfileImagesCreate')
        self.assertEqual(resolve(url).func.view_class, ProfileImagesCreateView)
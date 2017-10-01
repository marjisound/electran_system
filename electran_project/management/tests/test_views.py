from django.test import TestCase, RequestFactory
from management.views import homePage, semester_create, SemesterListView
from django.test import Client
from django.core.urlresolvers import reverse
from custom_accounts.models import MyUser
from django.contrib.auth.models import AnonymousUser


class HomePageViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = MyUser.objects.create(username='john',first_name='marjan',
                                          last_name='kalak',email='lennon@thebeatles.com', password='johnpassword')
        self.factory = RequestFactory()

    def test_index_view_basic(self):
        """
        test that the home page view returns 200 response
        and uses the correct template
        """
        request = self.factory.get('/')
        with self.assertTemplateUsed('management/index.html'):
            request.user = self.user
            request.session = {}
            response = homePage(request)
            self.assertEqual(response.status_code, 200)




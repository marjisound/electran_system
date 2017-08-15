from django.test import TestCase
from django.core.urlresolvers import resolve

from management.views import homePage, semester_create


class QuestionsURLsTestCase(TestCase):

    def test_root_url_uses_homePage_view(self):
        """
        Test that the root of the site resolves
        to the correct view function
        """
        root = resolve('/')
        self.assertEqual(root.func, homePage)

    def test_root_url_uses_semester_create_view(self):
        """
        Test that the semester_create of the site resolves
        to the correct view function
        """
        root = resolve('/management/semester_create')
        self.assertEqual(root.func, semester_create)
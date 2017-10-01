from django.test import TestCase
from django.core.urlresolvers import resolve
from management.views import homePage, semester_create, SemesterListView, report_marks


class QuestionsURLsTestCase(TestCase):
    allow_database_queries = True

    def test_root_url_uses_homePage_view(self):
        """
        Test that the root of the site resolves
        to the correct view function (homePage)
        """
        root = resolve('/')
        self.assertEqual(root.func, homePage)

    def test_root_url_uses_semester_create_view(self):
        """
        Test that the semester_create of the site resolves
        to the correct view function (semester_create)
        """
        root = resolve('/management/semester_create')
        self.assertEqual(root.func, semester_create)

    def test_root_url_uses_semester_list_view(self):
        """
        Test that the /management/semester_list resolves
        to the correct view class (SemesterListView)
        """
        root = resolve('/management/semester_list')
        self.assertEqual(root.func.view_class, SemesterListView)

    def test_root_url_uses_report_marks(self):
        """
        Test that the semester_create of the site resolves
        to the correct view function (semester_create)
        """
        root = resolve('/management/report_marks')
        self.assertEqual(root.func, report_marks)
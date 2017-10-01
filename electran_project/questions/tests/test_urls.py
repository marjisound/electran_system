from django.test import TestCase
from django.core.urlresolvers import resolve
from questions.views import all_questions


class QuestionsURLsTestCase(TestCase):
    allow_database_queries = True

    def test_questions_url_uses_all_questions_view(self):
        """
        Test that questions/<slug> url in the site resolves
        to the correct view function (all_questions)
        """
        root = resolve('/questions/hex_to_binary/')
        self.assertEqual(root.func, all_questions)



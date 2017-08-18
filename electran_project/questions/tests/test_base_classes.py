from django.test import TestCase
from questions.custom.question_classes import base_classes


class FixedLength(TestCase):

    def setUp(self):
        self.sub_signed_negative_positive = {'val1': 4294906129, 'val2': 536870911}
        self.sub_signed_negative_positive2 = {'val1': 4022364619, 'val2': 81383}
        self.sub_signed_negative_positive3 = {'val1': 4022364619, 'val2': 2004221952}

    def test_sub_rtype(self):
        """
        This test is for signed subtraction
        """
        question = base_classes.MipsInstructionsBase()
        expected = question.sub_rtype(self.sub_signed_negative_positive)

        correct_result = ('dfff1112', False)
        self.assertEqual(correct_result, expected)

        expected = question.sub_rtype(self.sub_signed_negative_positive2)
        correct_result = ('efbf2be4', False)
        self.assertEqual(correct_result, expected)

        expected = question.sub_rtype(self.sub_signed_negative_positive3)
        correct_result = ('784a69cb',  True)
        self.assertEqual(correct_result, expected)

    def test_subu_rtype(self):
        """
        This test is for signed subtraction
        """
        question = base_classes.MipsInstructionsBase()
        expected = question.subu_rtype(self.sub_signed_negative_positive)

        correct_result = ('dfff1112', None)
        self.assertEqual(correct_result, expected)

        expected = question.subu_rtype(self.sub_signed_negative_positive2)
        correct_result = ('efbf2be4', None)
        self.assertEqual(correct_result, expected)

        expected = question.subu_rtype(self.sub_signed_negative_positive3)
        correct_result = ('784a69cb',  None)
        self.assertEqual(correct_result, expected)

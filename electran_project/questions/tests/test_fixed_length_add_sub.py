from django.test import TestCase
from questions.custom.question_classes import fix_length_subtraction_signed
from questions.custom.question_classes import fix_length_subtraction_unsigned
from questions.custom.question_classes import fix_length_addition_signed
from questions.custom.question_classes import fix_length_addition_unsigned


class FixedLength(TestCase):

    def setUp(self):
        self.sub_signed_negative_positive = {'random1': 'ffff1111', 'random2': '1fffffff', 'base': 16}
        self.sub_signed_negative_negative = {'random1': '10001101', 'random2': '11101000', 'base': 2}
        self.sub_signed_positive_negative = {'random1': '00100110', 'random2': '10011001', 'base': 2}
        self.sub_signed_positive_negative2 = {'random1': '01111111', 'random2': '10001001', 'base': 2}
        self.sub_signed_positive_positive_signed = {'random1': '00100110', 'random2': '01100111', 'base': 2}

        self.add_signed_negative_positive = {'random1': 4294906129, 'random2': 536870911, 'base': 16}
        self.add_signed_negative_negative = {'random1': 141, 'random2': 232, 'base': 2}
        self.add_signed_positive_negative = {'random1': 38, 'random2': 153, 'base': 2}
        self.add_signed_positive_negative2 = {'random1': 127, 'random2': 137, 'base': 2}
        self.add_signed_positive_positive_signed = {'random1': 38, 'random2': 103, 'base': 2}

    def test_fixed_length_sub_signed(self):
        """
        This test is for signed subtraction
        """
        question = fix_length_subtraction_signed.Question()
        expected = question.expected_answer(self.sub_signed_negative_positive)

        correct_result = {'value': 'dfff1112', 'overflow': False}
        self.assertEqual(correct_result, expected)

        expected = question.expected_answer(self.sub_signed_negative_negative)
        correct_result = {'value': '10100101', 'overflow': False}
        self.assertEqual(correct_result, expected)

        expected = question.expected_answer(self.sub_signed_positive_negative)
        correct_result = {'value': '10001101', 'overflow': True}
        self.assertEqual(correct_result, expected)

        expected = question.expected_answer(self.sub_signed_positive_negative2)
        correct_result = {'value': '11110110', 'overflow': True}
        self.assertEqual(correct_result, expected)

        expected = question.expected_answer(self.sub_signed_positive_positive_signed)
        correct_result = {'value': '10111111', 'overflow': False}
        self.assertEqual(correct_result, expected)

    def test_fixed_length_sub_unsigned(self):
        """
        This test is for unsigned subtraction
        """
        question = fix_length_subtraction_unsigned.Question()
        expected = question.expected_answer(self.sub_signed_negative_positive)

        correct_result = {'value': 'dfff1112'}
        self.assertEqual(correct_result, expected)

        expected = question.expected_answer(self.sub_signed_negative_negative)
        correct_result = {'value': '10100101'}
        self.assertEqual(correct_result, expected)

        expected = question.expected_answer(self.sub_signed_positive_negative)
        correct_result = {'value': '10001101'}
        self.assertEqual(correct_result, expected)

        expected = question.expected_answer(self.sub_signed_positive_negative2)
        correct_result = {'value': '11110110'}
        self.assertEqual(correct_result, expected)

        expected = question.expected_answer(self.sub_signed_positive_positive_signed)
        correct_result = {'value': '10111111'}
        self.assertEqual(correct_result, expected)

    def test_fixed_length_add_signed(self):
        """
        This test is for signed addition
        """
        question = fix_length_addition_signed.Question()
        expected = question.expected_answer(self.add_signed_negative_positive)

        correct_result = {'value': '1fff1110', 'overflow': False}
        self.assertEqual(correct_result, expected)

        expected = question.expected_answer(self.add_signed_negative_negative)
        correct_result = {'value': '01110101', 'overflow': True}
        self.assertEqual(correct_result, expected)

        expected = question.expected_answer(self.add_signed_positive_negative)
        correct_result = {'value': '10111111', 'overflow': False}
        self.assertEqual(correct_result, expected)

        expected = question.expected_answer(self.add_signed_positive_negative2)
        correct_result = {'value': '00001000', 'overflow': False}
        self.assertEqual(correct_result, expected)

        expected = question.expected_answer(self.add_signed_positive_positive_signed)
        correct_result = {'value': '10001101', 'overflow': True}
        self.assertEqual(correct_result, expected)

    def test_fixed_length_add_unsigned(self):
        """
        This test is for signed addition
        """
        question = fix_length_addition_unsigned.Question()
        expected = question.expected_answer(self.add_signed_negative_positive)

        correct_result = {'value': '1fff1110'}
        self.assertEqual(correct_result, expected)

        expected = question.expected_answer(self.add_signed_negative_negative)
        correct_result = {'value': '01110101'}
        self.assertEqual(correct_result, expected)

        expected = question.expected_answer(self.add_signed_positive_negative)
        correct_result = {'value': '10111111'}
        self.assertEqual(correct_result, expected)

        expected = question.expected_answer(self.add_signed_positive_negative2)
        correct_result = {'value': '00001000'}
        self.assertEqual(correct_result, expected)

        expected = question.expected_answer(self.add_signed_positive_positive_signed)
        correct_result = {'value': '10001101'}
        self.assertEqual(correct_result, expected)




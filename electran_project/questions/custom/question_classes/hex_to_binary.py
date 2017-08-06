from questions.custom.question_classes.base_classes import BinaryHexBase
import os
import codecs


class Question(BinaryHexBase):

    def generate_user_random_display(self, value):
        return {'random1': value['random1']}

    def generate_random(self):
        random_value = codecs.encode(os.urandom(4), 'hex').decode()
        return {'random1': random_value}

    def expected_answer(self, value):
        expected = self.hex_to_binary(value['random1'])
        if expected.startswith('0b') or expected.startswith('0B'):
            expected = expected[2:]
        return expected

    def test_answer(self, student_answer, correct_answer):
        if type(student_answer) == str:
            formatted_answer = student_answer.replace(' ', '')
            if formatted_answer.startswith('0b') or formatted_answer.startswith('0B'):
                formatted_answer = formatted_answer[2:]

            if formatted_answer == correct_answer:
                True
            else:
                False
        else:
            raise TypeError('student answer must be of type string')

    def is_valid(self, binary_num):
        """
        :type binary_num: binary number string
        :rtype: dict
        """
        return self.is_valid_binary(binary_num)

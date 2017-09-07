from questions.custom.question_classes.base_classes import BinaryHexBase
import os
import codecs


class Question(BinaryHexBase):

    def generate_user_random_display(self, value):
        return {'random1': '0x' + value['random1']}

    def generate_random(self):
        random_value = codecs.encode(os.urandom(4), 'hex').decode()
        return {'random1': random_value}

    def expected_answer(self, value):
        expected = self.hex_to_binary(value['random1'])
        if expected.startswith('0b') or expected.startswith('0B'):
            expected = expected[2:]
        return expected

    def expected_answer_display_format(self, value):
        value = '{:0>32}'.format(value)
        return self.spacing_binary_numbers(value)

    def test_answer(self, student_answer, correct_answer):
        if type(student_answer) == str:
            answer_lower = student_answer.lower()
            formatted_answer = answer_lower.replace(' ', '')
            if formatted_answer.startswith('0b'):
                formatted_answer = formatted_answer[2:]

            while formatted_answer.startswith('0'):
                formatted_answer = formatted_answer[1:]

            if formatted_answer == correct_answer:
                return True
            else:
                return False
        else:
            raise TypeError('student answer must be of type string')

    def is_valid(self, binary_num):
        """
        :type binary_num: binary number string
        :rtype: dict
        """
        is_valid, message_type = self.is_valid_binary(binary_num)
        if not is_valid:
            if message_type == 'format':
                self.wrong_format_message = 'Your answer did not have a correct binary format. Please try again'
            else:
                self.wrong_format_message = 'The answer field must be filled in. Please try again'

        return is_valid


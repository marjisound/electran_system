from questions.custom.question_classes.base_classes import BinaryHexBase
import random


class Question(BinaryHexBase):

    def generate_user_random_display(self, value):
        random_value = ' '.join([value['random1'][i:i + 4] for i in range(0, len(value['random1']), 4)])
        return {'random1': random_value}

    def generate_random(self):
        random_int = random.randint(30000000, 267108880)
        random_value = '{:0>28b}'.format(random_int)
        return {'random1': random_value}

    def expected_answer(self, value):
        expected = self.binary_to_hex(value['random1'])[2:]
        return expected

    def expected_answer_display_format(self, value):
        return '0x' + value

    def test_answer(self, student_answer, correct_answer):
        if type(student_answer) == str:
            formatted_answer = student_answer.replace(' ', '')
            if formatted_answer.startswith('0x') or formatted_answer.startswith('0X'):
                formatted_answer = formatted_answer[2:]

            if formatted_answer == correct_answer:
                return True
            else:
                return False
        else:
            raise TypeError('student answer must be of type string')

    def is_valid(self, hex_num):
        """
        :type hex_num: hex number string
        :rtype: dict
        """
        is_valid, message_type = self.is_valid_hex(hex_num)
        if not is_valid:
            if message_type == 'format':
                self.wrong_format_message = 'Your answer did not have a correct hexadecimal format. Please try again'
            else:
                self.wrong_format_message = 'The answer field must be filled in. Please try again'

        return is_valid


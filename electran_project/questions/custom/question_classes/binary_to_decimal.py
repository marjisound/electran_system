from questions.custom.question_classes.base_classes import BinaryHexBase
import random


class Question(BinaryHexBase):

    def generate_user_random_display(self, value):
        random_value = self.spacing_binary_numbers(bin(value['random1'])[2:])
        return {'random1': random_value}

    def generate_random(self):
        random_int = random.randint(300, 511)
        return {'random1': random_int}

    def expected_answer(self, value):
        return value['random1']

    def test_answer(self, student_answer, correct_answer):
        if type(student_answer) == str:
            formatted_answer = int(student_answer.replace(' ', '').replace('\t', ''))

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
        is_valid, message_type = self.is_valid_int(hex_num)
        if not is_valid:
            if message_type == 'format':
                self.wrong_format_message = 'Your answer did not have a correct decimal format. Please try again'
            else:
                self.wrong_format_message = 'The answer field must be filled in. Please try again'

        return is_valid


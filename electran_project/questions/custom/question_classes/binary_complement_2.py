from questions.custom.question_classes.base_classes import BinaryHexBase
import random


class Question(BinaryHexBase):

    def generate_user_random_display(self, value):
        formatted_random_value = ' '.join([value['random1'][i:i + 4] for i in range(0, len(value['random1']), 4)])
        return {'random1': formatted_random_value}

    def generate_random(self):
        random_int = random.randint(70, 256)
        random_value = '{:0>8}'.format(bin(random_int)[2:])
        return {'random1': random_value}

    def expected_answer(self, value):
        trimmed_value = value['random1'].replace(' ', '')
        length = len(trimmed_value)
        if length > 8:
            extra_bit = length - 8
            trimmed_value = trimmed_value[extra_bit:]
        int_value = int(trimmed_value, 2)
        expected = bin(int_value - (1 << 8))
        if expected.startswith('0b') or expected.startswith('0B'):
            expected = expected[2:]
        elif expected.startswith('-0b') or expected.startswith('-0B'):
            expected = expected[3:]
        expected = '{:0>8}'.format(expected)
        return expected

    def expected_answer_display_format(self, value):
        modulo_value = len(value) % 4
        separate_value = value[:modulo_value]
        rest_of_value = value[modulo_value:]
        result = ' '.join([rest_of_value[i:i + 4] for i in range(0, len(rest_of_value), 4)])
        result = separate_value + ' ' + result
        return result

    def test_answer(self, student_answer, correct_answer):
        if type(student_answer) == str:
            formatted_answer = student_answer.replace(' ', '')
            formatted_answer = formatted_answer.lower()
            if formatted_answer.startswith('0b'):
                formatted_answer = formatted_answer[2:]
            # To Do: does the answer need to be exactly 8 bits?????

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


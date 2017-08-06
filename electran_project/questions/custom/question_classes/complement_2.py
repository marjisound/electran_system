from questions.custom.question_classes.base_classes import BinaryHexBase
import random


class Question(BinaryHexBase):

    def generate_user_random_display(self, value):
        random_value = value['random1']
        formatted_random_value = ' '.join([random_value[i:i + 4] for i in range(0, len(random_value), 4)])
        return {'random1': formatted_random_value}

    def generate_random(self):
        random_int = random.randint(70, 256)
        random_value = bin(random_int)
        if random_value.startswith('0b'):
            random_value = random_value[2:]
        while len(random_value) != 8:
            random_value = '0' + random_value
        return {'random1': random_value}

    def expected_answer(self, value):
        trimmed_value = value['random1'].replace(' ', '')
        int_value = int(trimmed_value, 2)
        expected = bin(int_value - (1 << 8))
        if expected.startswith('0b') or expected.startswith('0B'):
            expected = expected[2:]
        return expected

    def test_answer(self, student_answer, correct_answer):
        if type(student_answer) == str:
            formatted_answer = student_answer.replace(' ', '')
            if formatted_answer.startswith('0b') or formatted_answer.startswith('0B'):
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


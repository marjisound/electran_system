from questions.custom.question_classes.base_classes import BinaryHexBase
import random


class Question(BinaryHexBase):

    def generate_user_random_display(self, value):
        return {'random1': value['random1']}

    def generate_random(self):
        random_int = random.randint(268435456, 4294967295)
        random_value = hex(random_int)
        if random_value.startswith('0x'):
            random_value = random_value[2:]
        return {'random1': random_value}

    def expected_answer(self, value):
        int_value = int(value['random1'], 16)
        expected = hex(int_value - (1 << 32))
        if expected.startswith('0x') or expected.startswith('0X'):
            expected = expected[2:]
        elif expected.startswith('-0x') or expected.startswith('-0X'):
            expected = expected[3:]
        return expected

    def test_answer(self, student_answer, correct_answer):
        if type(student_answer) == str:
            formatted_answer = student_answer.replace(' ', '')
            formatted_answer = formatted_answer.lower()
            if formatted_answer.startswith('0x') or formatted_answer.startswith('0X'):
                formatted_answer = formatted_answer[2:]
            if formatted_answer.startswith('-0x') or formatted_answer.startswith('-0X'):
                formatted_answer = formatted_answer[3:]
            while formatted_answer.startswith('0'):
                formatted_answer = formatted_answer[1:]

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
                self.wrong_format_message = 'Your answer did not have a correct binary format. Please try again'
            else:
                self.wrong_format_message = 'The answer field must be filled in. Please try again'

        return is_valid


from questions.custom.question_classes.base_classes import BinaryHexBase
import random


class Question(BinaryHexBase):

    def __init__(self):
        self.base = None

    def generate_user_random_display(self, value):
        if value['base'] == 2:
            self.base = 2
            random_value1 = bin(value['random1'])
            random_value1 = self.delete_binary_identifier(random_value1)
            while len(random_value1) < 8:
                random_value1 = '0' + random_value1
            random_value1 = ' '.join([random_value1[i:i + 4] for i in range(0, len(random_value1), 4)])

            random_value2 = bin(value['random2'])
            random_value2 = self.delete_binary_identifier(random_value2)
            while len(random_value2) < 8:
                random_value2 = '0' + random_value2
            random_value2 = ' '.join([random_value2[i:i + 4] for i in range(0, len(random_value2), 4)])

        elif value['base'] == 8:
            self.base = 8
            random_value1 = oct(value['random1'])
            random_value1 = self.delete_octal_identifier(random_value1)

            random_value2 = oct(value['random2'])
            random_value2 = self.delete_octal_identifier(random_value2)

        elif value['base'] == 16:
            self.base = 16
            random_value1 = hex(value['random1'])
            random_value1 = self.delete_hex_identifier(random_value1)

            random_value2 = hex(value['random2'])
            random_value2 = self.delete_hex_identifier(random_value2)

        user_random_value = '0' + random_value1 + ' + 0' + random_value2
        return {'random1': user_random_value, 'base': value['base']}

    def generate_random(self):
        random_value1 = ''
        random_value2 = ''
        base_options = [2, 8, 16]
        random_base = random.choice(base_options)
        if random_base == 2:
            random_value1 = random.randint(70, 256)
            random_value2 = random.randint(70, 256)

        elif random_base == 8:
            random_value1 = random.randint(16777216, 134217727)
            random_value2 = random.randint(16777216, 134217727)

        elif random_base == 16:
            random_value1 = random.randint(268435456, 4294967295)
            random_value2 = random.randint(268435456, 4294967295)

        return {'random1': random_value1, 'random2': random_value2, 'base': random_base}

    def expected_answer(self, value):
        expected = value['random1'] + value['random2']
        if value['base'] == 2:
            expected = bin(expected)
            formatted_expected = self.delete_binary_identifier(expected)
            formatted_expected = '0' + formatted_expected
        elif value['base'] == 8:
            expected = oct(expected)
            formatted_expected = self.delete_octal_identifier(expected)
            formatted_expected = '0' + formatted_expected
        elif value['base'] == 16:
            expected = hex(expected)
            formatted_expected = self.delete_hex_identifier(expected)
            formatted_expected = '0' + formatted_expected

        return formatted_expected

    def test_answer(self, student_answer, correct_answer):
        if type(student_answer) == str:
            formatted_answer = student_answer.replace(' ', '')
            formatted_answer = self.delete_binary_identifier(formatted_answer)
            formatted_answer = self.delete_binary_identifier(formatted_answer)
            formatted_answer = self.delete_binary_identifier(formatted_answer)

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
        if self.base == 2:
            is_valid, message_type = self.is_valid_binary(hex_num)
            self.create_message_by_base(is_valid, message_type, 'binary')
        elif self.base == 8:
            is_valid, message_type = self.is_valid_oct(hex_num)
            self.create_message_by_base(is_valid, message_type, 'octal')
        elif self.base == 16:
            is_valid, message_type = self.is_valid_hex(hex_num)
            self.create_message_by_base(is_valid, message_type, 'hex')

        if not is_valid:
            if message_type == 'format':
                self.wrong_format_message = 'Your answer did not have a correct hexadecimal format. Please try again'
            else:
                self.wrong_format_message = 'The answer field must be filled in. Please try again'

        return is_valid

    def create_message_by_base(self, is_valid, message_type,  value_type):
        if not is_valid:
            if message_type == 'format':
                self.wrong_format_message = 'Your answer did not have a correct'+value_type+'format. Please try again'
            else:
                self.wrong_format_message = 'The answer field must be filled in. Please try again'




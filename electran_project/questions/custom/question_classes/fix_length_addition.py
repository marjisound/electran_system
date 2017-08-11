from questions.custom.question_classes.base_classes import BinaryHexBase
import random


class Question(BinaryHexBase):

    ANSWER_TYPE = 'multiple'
    ANSWER_NUMS = 2

    def __init__(self):
        self.base = None

    def generate_user_random_display(self, value):
        if value['base'] == 2:
            self.base = 2
            random_value1 = bin(value['random1'])
            random_value1 = self.delete_binary_identifier(random_value1)
            random_value1 = '{:0>8}'.format(random_value1)
            random_value1 = ' '.join([random_value1[i:i + 4] for i in range(0, len(random_value1), 4)])

            random_value2 = bin(value['random2'])
            random_value2 = self.delete_binary_identifier(random_value2)
            random_value2 = '{:0>8}'.format(random_value2)
            random_value2 = ' '.join([random_value2[i:i + 4] for i in range(0, len(random_value2), 4)])

        elif value['base'] == 16:
            self.base = 16
            random_value1 = hex(value['random1'])
            random_value1 = self.delete_hex_identifier(random_value1)
            random_value1 = '{:0>8}'.format(random_value1)

            random_value2 = hex(value['random2'])
            random_value2 = self.delete_hex_identifier(random_value2)
            random_value2 = '{:0>8}'.format(random_value2)

        user_random_value = random_value1 + ' + ' + random_value2
        return {'random1': user_random_value, 'base': value['base']}

    def generate_random(self):
        random_value1 = ''
        random_value2 = ''
        base_options = [2, 16]
        random_base = random.choice(base_options)
        if random_base == 2:
            random_value1 = random.randint(70, 256)
            random_value2 = random.randint(70, 256)

        elif random_base == 16:
            random_value1 = random.randint(16777216, 4294967295)
            random_value2 = random.randint(16777216, 4294967295)

        return {'random1': random_value1, 'random2': random_value2, 'base': random_base}

    def expected_answer(self, value):
        expected = value['random1'] + value['random2']
        if value['base'] == 2:
            expected = bin(expected)
            formatted_expected = self.delete_binary_identifier(expected)
            formatted_expected, overflow = self.make_specific_number_of_bits(formatted_expected, 8)
        elif value['base'] == 16:
            expected = hex(expected)
            formatted_expected = self.delete_hex_identifier(expected)
            formatted_expected, overflow = self.make_specific_number_of_bits(formatted_expected, 8)

        return {'value': formatted_expected, 'overflow': overflow}

    def expected_answer_display_format(self, value):
        spaced_value = self.spacing_binary_numbers(value['value'])
        return {'value': spaced_value, 'overflow': value['overflow']}

    def test_answer(self, student_answer, correct_answer):
        if type(student_answer['answer1']) == str:
            formatted_answer = student_answer['answer1'].replace(' ', '')
            formatted_answer = self.delete_binary_identifier(formatted_answer)
            formatted_answer = self.delete_hex_identifier(formatted_answer)

            if not student_answer['answer2']:
                student_answer['answer2'] = False

            if formatted_answer == correct_answer['value'] and student_answer['answer2'] == correct_answer['overflow']:
                return True
            else:
                return False
        else:
            raise TypeError('student answer must be of type string')

    def is_valid(self, value):
        """
        :type value: hex number string
        :rtype: dict
        """
        if self.base == 2:
            is_valid, message_type = self.is_valid_binary(value['answer1'])
            self.create_message_by_base(is_valid, message_type, 'binary')
        elif self.base == 16:
            is_valid, message_type = self.is_valid_hex(value['answer1'])
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




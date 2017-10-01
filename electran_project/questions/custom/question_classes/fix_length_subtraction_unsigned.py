from questions.custom.question_classes.base_classes import BinaryHexBase
import random


class Question(BinaryHexBase):

    ANSWER_TYPE = 'multiple'
    ANSWER_NUMS = 2

    def __init__(self):
        self.base = None
        self.sign = None

    def generate_user_random_display(self, value):
        random_value1 = '{:0>8}'.format(value['random1'])
        random_value2 = '{:0>8}'.format(value['random2'])

        if value['base'] == 2:
            singed_value = int(random_value1, 2) - int(random_value2, 2)
            self.sign = singed_value >= 0
            self.base = 2

            random_value1 = ' '.join([random_value1[i:i + 4] for i in range(0, len(random_value1), 4)])

            random_value2 = ' '.join([random_value2[i:i + 4] for i in range(0, len(random_value2), 4)])

        elif value['base'] == 16:
            singed_value = int(random_value1, 16) - int(random_value2, 16)
            self.sign = singed_value >= 0
            self.base = 16

        user_random_value = random_value1 + ' - ' + random_value2
        return {'random1': user_random_value, 'base': value['base']}

    def generate_random(self):
        random_value1 = ''
        random_value2 = ''
        base_options = [2, 16]
        random_base = random.choice(base_options)
        if random_base == 2:
            random_value1 = bin(random.randint(70, 256))[2:]
            random_value2 = bin(random.randint(70, 256))[2:]

        elif random_base == 16:
            random_value1 = hex(random.randint(16777216, 4294967295))[2:]
            random_value2 = hex(random.randint(16777216, 4294967295))[2:]

        return {'random1': random_value1, 'random2': random_value2, 'base': random_base}

    def expected_answer(self, value):

        if value['base'] == 2:
            # create a list of the value binary digits and
            # complement every digit
            # and create a string from the list of complemented digits
            lst_int = list(map(int, value['random2']))
            complemented_int = list(map(lambda x: 1 - x, lst_int))
            complemented_str = ''.join(list(map(str, complemented_int)))

            # adding two values in int format and add the result to 1
            # then convert the result to binary
            expected = bin(int(value['random1'], 2) + int(complemented_str, 2) + 1)[2:]
            formatted_expected = self.make_specific_number_of_bits(expected, 8)

        elif value['base'] == 16:
            # create a list of the value binary digits and
            # complement every digit
            # and create a string from the list of complemented digits
            lst_int = list(map(lambda x: int(x, 16), value['random2']))
            complemented_int = list(map(lambda x: hex(15 - x)[2:], lst_int))
            complemented_str = ''.join(list(map(str, complemented_int)))

            # adding two values in int format and add the result to 1
            # then convert the result to binary
            expected_bin = bin(int(value['random1'], 16) + int(complemented_str, 16) + 1)[2:]
            expected_bin = self.make_specific_number_of_bits(expected_bin, 32)

            expected = hex(int(value['random1'], 16) + int(complemented_str, 16) + 1)[2:]
            formatted_expected = self.make_specific_number_of_bits(expected, 8)

        return {'value': formatted_expected}

    def test_answer(self, student_answer, correct_answer):
        if type(student_answer['answer1']) == str:
            formatted_answer = student_answer['answer1'].replace(' ', '').replace('\t', '')
            formatted_answer = self.delete_binary_identifier(formatted_answer)
            formatted_answer = self.delete_hex_identifier(formatted_answer)

            if formatted_answer == correct_answer['value']:
                return True
            else:
                return False
        else:
            raise TypeError('student answer must be of type string')

    def is_valid(self, value):
        """
        :type value: string
        :rtype: dict
        """

        if self.base == 2:
            is_valid, message_type = self.is_valid_binary(value['answer1'])
            self.create_message_by_base(is_valid, message_type, 'binary', value['answer1'])
        elif self.base == 16:
            is_valid, message_type = self.is_valid_hex(value['answer1'])
            self.create_message_by_base(is_valid, message_type, 'hex', value['answer1'])

        if not is_valid:
            if message_type == 'format':
                self.wrong_format_message = 'Your answer did not have a correct hexadecimal format. Please try again'
            else:
                self.wrong_format_message = 'The answer field must be filled in. Please try again'

        return is_valid

    def create_message_by_base(self, is_valid, message_type,  value_type, answer):
        if not is_valid:
            if message_type == 'format':
                self.wrong_format_message = 'Your answer \"' + answer + '\" did not have a correct '\
                                            + value_type + ' format. Please try again'
            else:
                self.wrong_format_message = 'The answer field must be filled in. Please try again'

    def remove_negative_signed_bits(self, formatted_answer, correct_answer, neg_value):
        if len(formatted_answer) > len(correct_answer):
            if not self.sign:
                diff = len(formatted_answer) - len(correct_answer)
                diff_value = formatted_answer[:diff]
                if diff_value == diff * neg_value:
                    formatted_answer = formatted_answer[diff:]
        return formatted_answer



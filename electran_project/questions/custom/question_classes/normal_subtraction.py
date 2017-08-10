from questions.custom.question_classes.base_classes import BinaryHexBase
import random


class Question(BinaryHexBase):

    def __init__(self):
        self.base = None
        self.sign = None

    def generate_user_random_display(self, value):
        random_value1 = value['random1']
        random_value2 = value['random2']

        if value['base'] == 2:
            singed_value = int(random_value1, 2) - int(random_value2, 2)
            self.sign = singed_value >= 0
            self.base = 2
            while len(random_value1) < 8:
                random_value1 = '0' + random_value1
            random_value1 = ' '.join([random_value1[i:i + 4] for i in range(0, len(random_value1), 4)])

            while len(random_value2) < 8:
                random_value2 = '0' + random_value2
            random_value2 = ' '.join([random_value2[i:i + 4] for i in range(0, len(random_value2), 4)])

        elif value['base'] == 8:
            singed_value = int(random_value1, 8) - int(random_value2, 8)
            self.sign = singed_value >= 0
            self.base = 8
        elif value['base'] == 16:
            singed_value = int(random_value1, 16) - int(random_value2, 16)
            self.sign = singed_value >= 0
            self.base = 16

        user_random_value = '0' + random_value1 + ' - 0' + random_value2
        return {'random1': user_random_value, 'base': value['base']}

    def generate_random(self):
        random_value1 = ''
        random_value2 = ''
        base_options = [2, 8, 16]
        random_base = random.choice(base_options)
        if random_base == 2:
            random_value1 = bin(random.randint(70, 256))
            random_value2 = bin(random.randint(70, 256))

            random_value1 = self.delete_binary_identifier(random_value1)
            random_value2 = self.delete_binary_identifier(random_value2)

        elif random_base == 8:
            random_value1 = oct(random.randint(16777216, 134217727))
            random_value2 = oct(random.randint(16777216, 134217727))

            random_value1 = self.delete_octal_identifier(random_value1)
            random_value2 = self.delete_octal_identifier(random_value2)

        elif random_base == 16:
            random_value1 = hex(random.randint(268435456, 4294967295))
            random_value2 = hex(random.randint(268435456, 4294967295))

            random_value1 = self.delete_hex_identifier(random_value1)
            random_value2 = self.delete_hex_identifier(random_value2)

        return {'random1': random_value1, 'random2': random_value2, 'base': random_base}

    def expected_answer(self, value):

        if value['base'] == 2:
            lst_int = list(map(int, value['random2']))
            complemented_int = list(map(lambda x: 1 - x, lst_int))
            complemented_str = ''.join(list(map(str, complemented_int)))

            expected = bin(int(value['random1'], 2) + int(complemented_str, 2) + 1)
            expected = self.delete_binary_identifier(expected)

        elif value['base'] == 8:
            lst_int = list(map(lambda x: int(x, 8), value['random2']))
            complemented_int = list(map(lambda x: hex(7 - x)[2:], lst_int))
            complemented_str = ''.join(list(map(str, complemented_int)))

            expected = oct(int(value['random1'], 8) + int(complemented_str, 8) + 1)
            expected = self.delete_octal_identifier(expected)

        elif value['base'] == 16:
            lst_int = list(map(lambda x: int(x, 16), value['random2']))
            complemented_int = list(map(lambda x: hex(15 - x)[2:], lst_int))
            complemented_str = ''.join(list(map(str, complemented_int)))

            expected = hex(int(value['random1'], 16) + int(complemented_str, 16) + 1)
            expected = self.delete_hex_identifier(expected)

        return expected

    def test_answer(self, student_answer, correct_answer):
        if type(student_answer) == str:
            formatted_answer = student_answer.replace(' ', '')
            if self.base == 2:
                formatted_answer = self.delete_binary_identifier(formatted_answer)
                formatted_answer = self.remove_negative_signed_bits(formatted_answer, correct_answer, '1')

            elif self.base == 8:
                formatted_answer = self.delete_octal_identifier(formatted_answer)
                formatted_answer = self.remove_negative_signed_bits(formatted_answer, correct_answer, '7')
            elif self.base == 16:
                formatted_answer = self.delete_hex_identifier(formatted_answer)
                formatted_answer = self.remove_negative_signed_bits(formatted_answer, correct_answer, 'f')

            if formatted_answer == correct_answer:
                return True
            else:
                return False
        else:
            raise TypeError('student answer must be of type string')

    def is_valid(self, answer):
        """
        :type answer: string
        :rtype: dict
        """
        if self.base == 2:
            is_valid, message_type = self.is_valid_binary(answer)
            self.create_message_by_base(is_valid, message_type, 'binary', answer)
        elif self.base == 8:
            is_valid, message_type = self.is_valid_oct(answer)
            self.create_message_by_base(is_valid, message_type, 'octal', answer)
        elif self.base == 16:
            is_valid, message_type = self.is_valid_hex(answer)
            self.create_message_by_base(is_valid, message_type, 'hex', answer)

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



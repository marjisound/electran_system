from questions.custom.question_classes.base_classes import BinaryHexBase
import random


class Question(BinaryHexBase):

    def generate_user_random_display(self, value):
        exponent = value['bias'] - 127
        int_section_of_mantissa = value['mantissa'][:exponent]
        int_section_of_result = '1' + int_section_of_mantissa

        fraction = value['mantissa'][exponent:]

        while fraction.endswith('0'):
            fraction = fraction[:-1]

        if value['sign'] == '0':
            sign = ''
        else:
            sign = '-'

        result = sign + int_section_of_result + '.' + fraction

        return {'random1': result}

    def generate_random(self):
        bias = random.randint(128, 142)
        mantissa_15_bit = bin(random.randint(1, 32767))[2:]
        mantissa_15_bit = self.make_specific_number_of_bits(mantissa_15_bit, 15)
        mantissa = mantissa_15_bit + ('0' * 8)
        sign_bit = random.choice(['0', '1'])

        return {'bias': bias,
                'mantissa': mantissa,
                'sign': sign_bit}

    def expected_answer(self, value):
        bias = bin(value['bias'])[2:]
        result_bin = value['sign'] + bias + value['mantissa']
        result = hex(int(result_bin, 2))[2:]

        return result

    def test_answer(self, student_answer, correct_answer):
        if type(student_answer) == str:
            formatted_answer = student_answer.replace(' ', '')
            formatted_answer = formatted_answer.replace('\t', '')
            formatted_answer = formatted_answer.lower()

            if formatted_answer == correct_answer:
                return True
            else:
                return False
        else:
            raise TypeError('student answer must be of type string')

    def is_valid(self, hex_num):
        """
        :type binary_num: binary number string
        :rtype: dict
        """
        formatted_answer = hex_num.replace(' ', '')
        formatted_answer = formatted_answer.replace('\t', '')
        formatted_answer = formatted_answer.lower()

        is_valid, message_type = self.is_valid_hex(formatted_answer)
        if not is_valid:
            if message_type == 'format':
                self.wrong_format_message = 'Your answer did not have a correct Hexadecimal format. Please try again'
            else:
                self.wrong_format_message = 'The answer field must be filled in. Please try again'

        return is_valid


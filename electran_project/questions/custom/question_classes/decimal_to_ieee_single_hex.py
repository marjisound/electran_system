from questions.custom.question_classes.base_classes import BinaryHexBase
import random


class Question(BinaryHexBase):

    def generate_user_random_display(self, value):
        random_fraction = str(value['fraction'])
        while random_fraction.endswith('0'):
            random_fraction = random_fraction[:-1]

        if value['sign'] == '0':
            sign = '+'
        else:
            sign = '-'
        return {'random1': sign + str(value['integer']),
                'random2': random_fraction}

    def generate_random(self):
        random_int = random.randint(100, 16384)
        random_fraction = 25 * 5 * random.randint(1, 7) * (5 ** random.randrange(5))
        sign = random.choice(['1', '0'])

        return {'integer': random_int, 'fraction': random_fraction, 'sign': sign}

    def expected_answer(self, value):
        bin_value = bin(value['integer'])[2:]
        fract = float('0.' + str(value['fraction']))
        fract_bin = ''
        while not fract.is_integer():
            temp_fract = fract * 2
            fract_bin += str(int(temp_fract))
            fract = temp_fract - int(temp_fract)

        exponent = len(bin_value[1:])
        mantissa = '{:0<23}'.format(bin_value[1:] + fract_bin)

        bias = bin(exponent + 127)[2:]

        result_bin = value['sign'] + bias + mantissa
        result = hex(int(result_bin, 2))[2:]

        return result

    def test_answer(self, student_answer, correct_answer):
        if type(student_answer) == str:
            formatted_answer = student_answer.replace(' ', '')
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
        formatted_answer = formatted_answer.lower()

        is_valid, message_type = self.is_valid_hex(formatted_answer)
        if not is_valid:
            if message_type == 'format':
                self.wrong_format_message = 'Your answer did not have a correct Hexadecimal format. Please try again'
            else:
                self.wrong_format_message = 'The answer field must be filled in. Please try again'

        return is_valid


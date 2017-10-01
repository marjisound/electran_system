from questions.custom.question_classes.base_classes import BinaryHexBase
import random


class Question(BinaryHexBase):

    def generate_user_random_display(self, value):
        random_int = value['random1']
        random_fraction = value['random2']

        bin_value = bin(random_int)[2:]
        fract = float('0.' + str(random_fraction))
        fract_bin = ''
        while not fract.is_integer():
            temp_fract = fract * 2
            fract_bin += str(int(temp_fract))
            fract = temp_fract - int(temp_fract)

        formatted_fract_bin = '{:0<3}'.format(fract_bin)
        formatted_fract_bin = formatted_fract_bin[:3]
        result = bin_value + formatted_fract_bin
        result = self.make_specific_number_of_bits(result, 12)
        new_value = self.spacing_binary_numbers(result)
        return {'random1': new_value}

    def generate_random(self):
        random_int = random.randint(100, 500)
        random_fraction = 25 * 5 * random.randint(1, 7)

        return {'random1': random_int, 'random2': random_fraction}

    def expected_answer(self, value):
        expected = str(value['random1']) + '.' + str(value['random2'])
        return expected

    def test_answer(self, student_answer, correct_answer):
        if type(student_answer) == str:
            formatted_answer = student_answer.replace(' ', '').replace('\t', '')
            formatted_answer = formatted_answer.replace('\t', '')

            if float(formatted_answer) == float(correct_answer):
                return True
            else:
                return False
        else:
            raise TypeError('student answer must be of type string')

    def is_valid(self, num):
        """
        :type hex_num: hex number string
        :rtype: dict
        """
        is_valid, message_type = self.is_valid_float(num)
        if not is_valid:
            if message_type == 'format':
                self.wrong_format_message = 'Your answer did not have a correct real number format. Please try again'
            else:
                self.wrong_format_message = 'The answer field must be filled in. Please try again'

        return is_valid


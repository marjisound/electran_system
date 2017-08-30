from questions.custom.question_classes.base_classes import BinaryHexBase
import random


class Question(BinaryHexBase):

    def generate_user_random_display(self, value):
        return {'random1': value['memory_locations'],
                'random2': value['result']}

    def generate_random(self):

        address_bus_size = 32

        memory_bit_length = random.randint(6, 26)

        if memory_bit_length >= 20:
            memory_locations = str(2 ** (memory_bit_length-20)) + 'M'
        elif memory_bit_length >= 10:
            memory_locations = str(2 ** (memory_bit_length - 10)) + 'K'
        else:
            memory_locations = 2 ** memory_bit_length

        memory_starting = '0' * memory_bit_length

        chip_length = address_bus_size - memory_bit_length
        chip_identifier = random.randint(0, (2**chip_length - 1))

        prepared_format = '{:0>' + str(chip_length) + '}'

        chip_identifier_bin = prepared_format.format(bin(chip_identifier)[2:])
        result = hex(int(chip_identifier_bin + memory_starting, 2))[2:]

        result = '{:0>8}'.format(result)

        return {'bus_size': address_bus_size,
                'memory_locations': memory_locations,
                'pattern': chip_identifier_bin,
                'result': result}

    def expected_answer(self, value):

        return value['pattern']

    def test_answer(self, student_answer, correct_answer):

        if type(student_answer) == str:
            formatted_answer = student_answer.replace(' ', '')

            if formatted_answer == correct_answer:
                return True
            else:
                return False
        else:
            raise TypeError('student answer must be of type string')

    def is_valid(self, student_answer):
        """
        :type student_answer: binary number string
        :rtype: dict
        """
        is_valid, message_type = self.is_valid_binary(student_answer)
        if not is_valid:
            if message_type == 'format':
                self.wrong_format_message = 'Your answer did not have a correct binary format. Please try again'
            else:
                self.wrong_format_message = 'The answer field must be filled in. Please try again'

        return is_valid


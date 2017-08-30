from questions.custom.question_classes.base_classes import BinaryHexBase
import random


class Question(BinaryHexBase):

    ANSWER_TYPE = 'multiple'
    display_correct = []

    def generate_user_random_display(self, value):
        return {'random1': value['bus_size'],
                'random2': value['memory_locations'],
                'random3': value['pattern']}

    def generate_random(self):

        address_bus_size = 16

        chip_identifier_length = random.randint(2, 8)
        chip_identifier = random.randint(0, (2**chip_identifier_length)-1)

        prepare_format = '{:0>' + str(chip_identifier_length) + '}'
        chip_identifier = prepare_format.format(bin(chip_identifier)[2:])

        memory_bit_length = address_bus_size - chip_identifier_length

        if memory_bit_length >= 10:
            memory_locations = str(2 ** (memory_bit_length-10)) + 'K'
        else:
            memory_locations = 2 ** memory_bit_length

        return {'bus_size': address_bus_size,
                'memory_locations': memory_locations,
                'pattern': chip_identifier}

    def expected_answer(self, value):

        lowest_address = value['pattern'] + ('0' * (value['bus_size'] - len(value['pattern'])))
        highest_address = value['pattern'] + ('1' * (value['bus_size'] - len(value['pattern'])))

        result = {
            'answer_lowest_address': '{:0>4}'.format(hex(int(lowest_address, 2))[2:]),
            'answer_highest_address': '{:0>4}'.format(hex(int(highest_address, 2))[2:])
        }

        return result

    def test_answer(self, student_answer, correct_answer):

        student_answer['answer_lowest_address'] = student_answer['answer_lowest_address'].replace(' ', '')
        student_answer['answer_highest_address'] = student_answer['answer_highest_address'].replace(' ', '')

        diff_list = self.compare_dictionaries(student_answer, correct_answer)

        self.display_correct = diff_list

        if len(diff_list) == 0:

            return True
        else:
            return False

    def is_valid(self, student_answer):
        """
        :type student_answer: dictionary {answer_lowest_address: value, answer_highest_address: value}
        :rtype: dict
        """
        student_answer['answer_lowest_address'] = student_answer['answer_lowest_address'].replace(' ', '')
        student_answer['answer_highest_address'] = student_answer['answer_highest_address'].replace(' ', '')

        is_valid_lowest, message_type_lowest = self.is_valid_hex(student_answer['answer_lowest_address'])
        is_valid_highest, message_type_highest = self.is_valid_hex(student_answer['answer_highest_address'])

        if not is_valid_lowest:
            if message_type_lowest == 'format':
                self.wrong_format_message = ('Your lowest memory answer did not have a correct Binary'
                                             'format. Please try again')
            else:
                self.wrong_format_message = 'The lowest memory answer field for must be filled in. Please try again'
        elif not is_valid_highest:
            if message_type_lowest == 'format':
                self.wrong_format_message = ('Your highest memory answer did not have a correct' 
                                             'Hexadecimal format. Please try again')
            else:
                self.wrong_format_message = 'The highest memory answer field must be filled in. Please try again'

        return is_valid_lowest and is_valid_highest


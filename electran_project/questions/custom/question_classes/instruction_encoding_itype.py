from questions.custom.question_classes.base_classes import BinaryHexBase, MipsInstructionsBase
import random


class Question(MipsInstructionsBase, BinaryHexBase):

    def generate_user_random_display(self, value):

        user_random_value = {'rs': str(value['rs']), 'rt': str(value['rt']),
                             'instruction_type': value['instruction_type'], 'instruction_format': 'R',
                             'offset': hex(value['offset'])}

        return user_random_value

    def generate_random(self):
        rs = random.randint(0, 31)
        rt = random.randint(0, 31)
        offset = random.randint(0, 65535)

        instruction_type = random.choice([i for i, j in self.MIPS_INS_TYPES['I'].items()])

        return {'rs': rs, 'rt': rt, 'instruction_type': instruction_type,
                'instruction_format': 'R', 'offset': offset}

    def expected_answer(self, value):

        rs = '{:0>5}'.format(bin(value['rs'])[2:])
        rt = '{:0>5}'.format(bin(value['rt'])[2:])

        op_value = '{:0>6}'.format(bin(self.ITYPE_VALUES[value['instruction_type']])[2:])

        offset = '{:0>16}'.format(bin(value['offset'])[2:])

        expected = op_value + rs + rt + offset

        return expected

    def expected_answer_display_format(self, value):
        return value[:6] + ' ' + value[6:11] + ' ' + value[11:16] + ' ' + value[16:]

    def test_answer(self, student_answer, correct_answer):
        if type(student_answer) == str:
            formatted_answer = student_answer.replace(' ', '')

            formatted_answer = self.delete_binary_identifier(formatted_answer)

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

        is_valid, message_type = self.is_valid_binary(answer)
        if message_type == 'format':
            self.wrong_format_message = ('Your answer \"' + answer + '\" did not have a' 
                                         ' correct binary format. Please try again')
        else:
            self.wrong_format_message = 'The answer field must be filled in. Please try again'

        return is_valid





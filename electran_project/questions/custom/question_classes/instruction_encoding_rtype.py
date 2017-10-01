from questions.custom.question_classes.base_classes import BinaryHexBase, MipsInstructionsBase
import random


class Question(MipsInstructionsBase, BinaryHexBase):

    def generate_user_random_display(self, value):

        random_value = ''

        if value['instruction_type'] in self.RTYPE_GROUPS['no_shift']:
            random_value = '{0} ${1}, ${2}, ${3}'.format(value['instruction_type'],  value['rd'],
                                                         value['rs'], value['rt'])

        elif value['instruction_type'] in self.RTYPE_GROUPS['no_rs']:
            random_value = '{0} ${1}, ${2}, {3}'.format(value['instruction_type'], value['rd'],
                                                        value['rt'], hex(value['shift']))

        elif value['instruction_type'] in self.RTYPE_GROUPS['no_rt_shift']:
            random_value = '{0} ${1}, ${2}'.format(value['instruction_type'], value['rd'], value['rs'])

        elif value['instruction_type'] in self.RTYPE_GROUPS['no_rt_rd_shift']:
            random_value = '{0} ${1}'.format(value['instruction_type'], value['rs'])

        user_random_value = {'instruction_format': 'R', 'random_value': random_value}

        return user_random_value

    def generate_random(self):
        rs = random.randint(0, 31)
        rt = random.randint(0, 31)
        rd = random.randint(0, 31)
        shift = 0

        instruction_type = random.choice([i for i, j in self.MIPS_INS_TYPES['R'].items()])

        if instruction_type in self.RTYPE_GROUPS['no_rs']:
            rs = 0
            shift = random.randint(0, 31)
        elif instruction_type in self.RTYPE_GROUPS['no_rt_shift']:
            rt = 0
        elif instruction_type in self.RTYPE_GROUPS['no_rt_rd_shift']:
            rt = 0
            rd = 0

        return {'rs': rs, 'rt': rt, 'rd': rd, 'shift': shift,
                'instruction_type': instruction_type, 'instruction_format': 'R'}

    def expected_answer(self, value):
        op_value = '000000'
        shamt_value = '{:0>5}'.format(bin(value['shift'])[2:])
        rs = '{:0>5}'.format(bin(value['rs'])[2:])
        rt = '{:0>5}'.format(bin(value['rt'])[2:])
        rd = '{:0>5}'.format(bin(value['rd'])[2:])
        funct_value = '{:0>6}'.format(bin(self.RTYPE_VALUES[value['instruction_type']])[2:])

        expected = op_value + rs + rt + rd + shamt_value + funct_value

        return expected

    def expected_answer_display_format(self, value):
        expected = value[:6] + ' ' + value[6:11] + ' ' + value[11:16] \
                   + ' ' + value[16:21] + ' ' + value[21:26] + ' ' + value[26:]
        return expected

    def test_answer(self, student_answer, correct_answer):
        if type(student_answer) == str:
            formatted_answer = student_answer.replace(' ', '').replace('\t', '')

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





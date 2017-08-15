from questions.custom.question_classes.base_classes import BinaryHexBase, MipsInstructionsBase
import random


class Question(MipsInstructionsBase, BinaryHexBase):

    def generate_user_random_display(self, value):

        rs = '{:0>5}'.format(bin(value['rs'])[2:])
        rt = '{:0>5}'.format(bin(value['rt'])[2:])
        rd = '{:0>5}'.format(bin(value['rd'])[2:])
        op_value = '000000'
        shamt_value = '{:0>5}'.format(bin(value['shift'])[2:])
        funct_value = '{:0>6}'.format(bin(self.RTYPE_VALUES[value['instruction_type']])[2:])

        user_random_value = op_value + ' ' + rs + ' ' + rt + ' ' + rd + ' ' + shamt_value + ' ' + funct_value

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
        expected = ''

        if value['instruction_type'] in self.RTYPE_GROUPS['no_shift']:
            expected = '{0} ${1}, ${2}, ${3}'.format(value['instruction_type'],  value['rd'],
                                                         value['rs'], value['rt'])

        elif value['instruction_type'] in self.RTYPE_GROUPS['no_rs']:
            expected = '{0} ${1}, ${2}, {3}'.format(value['instruction_type'], value['rd'],
                                                    value['rt'], hex(value['shift']))

        elif value['instruction_type'] in self.RTYPE_GROUPS['no_rt_shift']:
            expected = '{0} ${1}, ${2}'.format(value['instruction_type'], value['rd'], value['rs'])

        elif value['instruction_type'] in self.RTYPE_GROUPS['no_rt_rd_shift']:
            expected = '{0} ${1}'.format(value['instruction_type'], value['rs'])

        return expected

    def test_answer(self, student_answer, correct_answer):
        if type(student_answer) == str:
            formatted_correct_answer = correct_answer.replace(' ', '')
            formatted_answer = student_answer.replace(' ', '')
            formatted_answer = formatted_answer.lower()
            if formatted_answer == formatted_correct_answer:
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
        if not answer or type(answer) != str:
            self.wrong_format_message = 'The answer field must be filled in. Please try again'
            return False, 'field'
        else:

            answer_list = answer.split(' ')
            if answer_list[0] not in self.MIPS_INS_TYPES['R'] or '$' not in answer_list[1]:
                self.wrong_format_message = ('Your answer did not have a correct R-Type ' 
                                             'instruction format. e.g. \"add $8, $1, $2\".Please try again')
                return False
            else:
                return True





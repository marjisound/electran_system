from questions.custom.question_classes.base_classes import BinaryHexBase, MipsInstructionsBase
import random


class Question(MipsInstructionsBase, BinaryHexBase):

    def generate_user_random_display(self, value):

        user_random_value = {'rs': str(value['rs']), 'rt': str(value['rt']), 'rd': str(value['rd']),
                             'instruction_type': value['instruction_type'], 'instruction_format': 'R'}

        return user_random_value

    def generate_random(self):
        rs = random.randint(0, 31)
        rt = random.randint(0, 31)
        rd = random.randint(0, 31)

        instruction_type = random.choice([i for i, j in self.MIPS_INS_TYPES['R'].items()])

        return {'rs': rs, 'rt': rt, 'rd': rd,
                'instruction_type': instruction_type, 'instruction_format': 'R'}

    def expected_answer(self, value):
        op_value = '000000'
        shamt_value = '00000'
        rs = bin(value['rs'])[2:]
        while len(rs) < 5:
            rs = '0' + rs

        rt = bin(value['rt'])[2:]
        while len(rt) < 5:
            rt = '0' + rt

        rd = bin(value['rd'])[2:]
        while len(rd) < 5:
            rd = '0' + rd

        funct_value = bin(self.RTYPE_VALUES[value['instruction_type']])[2:]
        while len(funct_value) < 6:
            funct_value = '0' + funct_value

        expected = op_value + rs + rt + rd + shamt_value + funct_value

        return expected

    def expected_answer_display_format(self, value):
        expected = value[:6] + ' ' + value[6:11] + ' ' + value[11:16] \
                   + ' ' + value[16:21] + ' ' + value[21:26] + ' ' + value[26:]
        return expected

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





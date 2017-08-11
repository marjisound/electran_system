from questions.custom.question_classes.base_classes import BinaryHexBase, MipsInstructionsBase
import random


class Question(MipsInstructionsBase, BinaryHexBase):

    def generate_user_random_display(self, value):

        rs = '{:0>5}'.format(bin(value['rs'])[2:])
        rt = '{:0>5}'.format(bin(value['rt'])[2:])

        op_value = '{:0>6}'.format(bin(self.ITYPE_VALUES[value['instruction_type']])[2:])

        offset = '{:0>16}'.format(bin(value['offset'])[2:])

        expected = op_value + ' ' + rs + ' ' + rt + ' ' + offset

        return expected

    def generate_random(self):
        rs = random.randint(0, 31)
        rt = random.randint(0, 31)
        offset = random.randint(0, 65535)

        instruction_type = random.choice([i for i, j in self.MIPS_INS_TYPES['I'].items()])

        return {'rs': rs, 'rt': rt, 'instruction_type': instruction_type,
                'instruction_format': 'R', 'offset': offset}

    def expected_answer(self, value):

        expected = value['instruction_type'] + ' $' +\
                   str(value['rt']) + ', ' + hex(value['offset']) + '($' + str(value['rs']) + ')'

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
            self.wrong_format_message = ('Your answer did not have a correct I-Type '
                                         'instruction format. e.g. \"lw $20, 0x1234($5)\". Please try again')
            answer_list = answer.split(',')
            if len(answer_list) != 2:
                return False
            else:
                if '$' not in answer_list[0] or '$' not in answer_list[1]:
                    return False

                else:
                    return True





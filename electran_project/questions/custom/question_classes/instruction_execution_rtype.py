from questions.custom.question_classes.base_classes import BinaryHexBase, MipsInstructionsBase
import random
import os
import codecs


class Question(MipsInstructionsBase, BinaryHexBase):
    ANSWER_TYPE = 'multiple'

    def generate_user_random_display(self, value):

        formatted_memory_locations = {}
        formatted_registers = {}

        for key, memory_value in value['memory_locations'].items():
            formatted_memory_locations[hex(key)] = memory_value

        for key, memory_value in value['registers'].items():
            formatted_registers[key] = '{:0>8}'.format(hex(memory_value)[2:])

        user_random_value = {'rs': str(value['rs']), 'rt': str(value['rt']), 'rd': str(value['rd']),
                             'instruction_type': value['instruction_type'], 'instruction_format': 'R',
                             'registers': formatted_registers, 'memory_locations': formatted_memory_locations,
                             'pc': hex(self.PC_VALUE)}

        return user_random_value

    def generate_random(self):
        rs = random.randint(0, 31)
        rt = random.randint(0, 31)
        rd = random.randint(0, 31)

        instruction_type = random.choice([i for i, j in self.MIPS_INS_TYPES['R'].items()])

        register_dict = self.REGISTER_VALUES

        memory_dict = {}
        fst_memory = self.MEMORY_LOCATION_STARTING_POINT
        for i in range(32):
            memory_dict[fst_memory+i] = codecs.encode(os.urandom(1), 'hex').decode()

        return {'rs': rs, 'rt': rt, 'rd': rd, 'pc': self.PC_VALUE,
                'instruction_type': instruction_type, 'instruction_format': 'R',
                'registers': register_dict, 'memory_locations': memory_dict}

    def expected_answer(self, value):
        func_values = {
            'val1': value['rs'],
            'val2': value['rt']
        }
        expected = {
            'answer_register': 'written',
            'answer_register_num': value['rd'],
            'answer_register_value': self.RTYPE_CALCULATIONS[value['instruction_type']](func_values),
            'answer_pc': 'written',
            'answer_pc_value': value['pc'] + 4,
            'answer_memory_0': 'unchanged',
            'answer_memory_0_address': None,
            'answer_memory_0_value': None,
            'answer_memory_1': 'unchanged',
            'answer_memory_1_address': None,
            'answer_memory_1_value': None,
            'answer_memory_2': 'unchanged',
            'answer_memory_2_address': None,
            'answer_memory_2_value': None,
            'answer_memory_3': 'unchanged',
            'answer_memory_3_address': None,
            'answer_memory_3_value': None,
        }

        return expected

    def expected_answer_display_format(self, value):
        pass

    def test_answer(self, student_answer, correct_answer):
        pass

    def is_valid(self, answer):
        return True





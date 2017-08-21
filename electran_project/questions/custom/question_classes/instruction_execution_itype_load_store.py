from questions.custom.question_classes.base_classes import BinaryHexBase, MipsInstructionsBase
import random
import os
import codecs


class Question(MipsInstructionsBase, BinaryHexBase):
    ANSWER_TYPE = 'multiple'
    memory_storage_address = None

    def generate_user_random_display(self, value):
        new_value = value.copy()
        new_value['immediate'] = hex(value['immediate'])
        return new_value

    def generate_random(self):
        rs = random.randint(1, 31)
        rt = random.randint(1, 31)
        immediate = random.randrange(65535)

        #  do the sign extension for the immediate value
        immediate_bin = '{:0>16}'.format(bin(immediate)[2:])
        immediate_msb = immediate_bin[0]
        prepared_sign = '{:' + immediate_msb + '>32}'
        sign_extended_immediate_bin = prepared_sign.format(immediate_bin)

        memory_dict = self.random_memories()
        type(self).memory_storage_address = random.choice(range(int(min(memory_dict), 16), int(max(memory_dict), 16), 4))

        instruction_type = random.choice(['lw', 'sw'])
        # instruction_type = 'lw'

        register_dict = self.random_registers()

        test, overflow = self.subu_rtype({'val1': Question.memory_storage_address, 'val2': int(sign_extended_immediate_bin, 2)})

        register_dict[str(rs)] = test

        pc = '0x' + '{:0>8}'.format(codecs.encode(os.urandom(4), 'hex').decode())

        return {'rs': rs, 'rt': rt, 'immediate': immediate, 'pc': pc,
                'instruction_type': instruction_type, 'instruction_format': 'R',
                'registers': register_dict, 'memory_locations': memory_dict}

    def expected_answer(self, value):

        rt = '{:0>8}'.format(value['registers'][str(value['rt'])])
        rt_list = [rt[i:i + 2] for i in range(0, len(rt), 2)]
        expected = {}

        if value['instruction_type'] == 'sw':
            expected = {
                'answer_register': 'unchanged',
                'answer_register_num': None,
                'answer_register_value': None,
                'answer_pc': 'written',
                'answer_pc_value': '{:0>8}'.format(hex(int(value['pc'], 16) + 4)[2:]),
                'answer_memory_0': 'written',
                'answer_memory_0_address': hex(Question.memory_storage_address)[2:],
                'answer_memory_0_value': rt_list[0],
                'answer_memory_1': 'written',
                'answer_memory_1_address': hex(Question.memory_storage_address + 1)[2:],
                'answer_memory_1_value': rt_list[1],
                'answer_memory_2': 'written',
                'answer_memory_2_address': hex(Question.memory_storage_address + 2)[2:],
                'answer_memory_2_value': rt_list[2],
                'answer_memory_3': 'written',
                'answer_memory_3_address': hex(Question.memory_storage_address + 3)[2:],
                'answer_memory_3_value': rt_list[3],
                'answer_overflow': None
            }
        elif value['instruction_type'] == 'lw':
            reg_val = ''.join(value['memory_locations'][hex(Question.memory_storage_address + n)[2:]] for n in range(4))
            expected = {
                'answer_register': 'written',
                'answer_register_num': str(value['rt']),
                'answer_register_value': reg_val,
                'answer_pc': 'written',
                'answer_pc_value': '{:0>8}'.format(hex(int(value['pc'], 16) + 4)[2:]),
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
                'answer_overflow': None
            }

        return expected

    def expected_answer_display_format(self, value):
        return value

    def test_answer(self, student_answer, correct_answer):

        new_student_list = student_answer.copy()

        pc_value = student_answer['answer_pc_value'].replace(' ', '')
        pc_value = self.delete_hex_identifier(pc_value.lower())
        new_student_list['answer_pc_value'] = '{:0>8}'.format(pc_value)

        if correct_answer['answer_register'] == 'written':
            register_value = self.delete_hex_identifier(student_answer['answer_register_value'].replace(' ', '').lower())
            new_student_list['answer_register_value'] = '{:0>8}'.format(register_value)

        elif correct_answer['answer_register'] == 'unchanged':
            for i in range(4):
                memory = self.delete_hex_identifier(student_answer['answer_memory_' + str(i) + '_value'].replace(' ', '').lower())
                new_student_list['answer_memory_' + str(i) + '_value'] = '{:0>2}'.format(memory)

        for key, value in new_student_list.items():
            if value == 'None' or value == '':
                new_student_list[key] = None

        # convert overflow value to boolean
        if new_student_list['answer_overflow'] == '1':
            new_student_list['answer_overflow'] = True
        elif new_student_list['answer_overflow'] == '0':
            new_student_list['answer_overflow'] = False

        diff_list = self.compare_dictionaries(new_student_list, correct_answer)

        self.display_correct = diff_list

        if len(diff_list) == 0:

            return True
        else:
            return False


    def is_valid(self, answer):
        return True





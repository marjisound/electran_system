import random
import codecs
import os


class QuestionBase:
    """Common base class for all questions"""
    wrong_answer_message = 'Wrong Answer'
    correct_answer_message = 'Correct Answer'
    wrong_format_message = 'Your answer did not have a correct format. Please try again'

    def generate_random(self):
        return None

    def expected_answer(self, value):
        return None

    def test_answer(self, student_answer, correct_answer):
        return False

    def expected_answer_display_format(self, value):
        return value

    def generate_user_random_display(self, value):
        return value

    @staticmethod
    def compare_dictionaries(student, correct):
        diff_list = []
        shared_keys = set(student.keys()).intersection(correct.keys())
        for key in shared_keys:
            if student[key] != correct[key]:
                diff_list.append((key, (student[key], correct[key])))
        return diff_list

    @staticmethod
    def remove_list_from_list(parent_list, removing_list):
        for item in removing_list:
            if item in parent_list:
                parent_list.remove(item)


class BinaryHexBase(QuestionBase):
    """Common base class for all binary/hex questions"""

    POWER_DICT = {
        'K': 10,
        'M': 20,
        'G': 30
    }

    @staticmethod
    def delete_binary_identifier(value):
        if value.startswith('0b') or value.startswith('0B'):
            return value[2:]
        elif value.startswith('-0b') or value.startswith('-0B'):
            formatted_value = value[3:]
            return '-' + formatted_value
        else:
            return value

    @staticmethod
    def delete_hex_identifier(value):
        if value.startswith('0x') or value.startswith('0X'):
            return value[2:]
        elif value.startswith('-0x') or value.startswith('-0X'):
            formatted_value = value[3:]
            return '-' + formatted_value
        else:
            return value

    @staticmethod
    def delete_octal_identifier(value):
        if value.startswith('0o') or value.startswith('0O'):
            return value[2:]
        elif value.startswith('-0o') or value.startswith('-0O'):
            formatted_value = value[3:]
            return '-' + formatted_value
        else:
            return value

    @staticmethod
    def hex_to_binary(hex_num):
        return bin(int(hex_num, 16))

    @staticmethod
    def binary_to_hex(binary_num):
        return hex(int(binary_num, 2))

    def is_valid_hex(self, hex_num):
        if not hex_num or type(hex_num) != str:
            self.wrong_format_message = 'The answer field must be filled in. Please try again'
            return False, 'field'
        else:
            try:
                hex_num = hex_num.replace(' ', '')
                int(hex_num, 16)
            except ValueError:
                self.wrong_format_message = 'Your answer did not have a correct binary format. Please try again'
                return False, 'format'
            else:
                return True, 'format'

    def is_valid_binary(self, binary_num):
        if not binary_num or type(binary_num) != str:
            self.wrong_format_message = 'The answer field must be filled in. Please try again'
            return False, 'field'
        else:
            try:
                binary_num = binary_num.replace(' ', '')
                int(binary_num, 2)
            except ValueError:
                self.wrong_format_message = 'Your answer did not have a correct binary format. Please try again'
                return False, 'format'
            else:
                return True, 'format'

    def is_valid_oct(self, octal_num):
        if not octal_num or type(octal_num) != str:
            self.wrong_format_message = 'The answer field must be filled in. Please try again'
            return False, 'field'
        else:
            try:
                binary_num = octal_num.replace(' ', '')
                int(binary_num, 8)
            except ValueError:
                self.wrong_format_message = 'Your answer did not have a correct octal format. Please try again'
                return False, 'format'
            else:
                return True, 'format'

    @staticmethod
    def spacing_binary_numbers(value):
        modulo_value = len(value) % 4
        separate_value = value[:modulo_value]
        rest_of_value = value[modulo_value:]
        result = ' '.join([rest_of_value[i:i + 4] for i in range(0, len(rest_of_value), 4)])
        if separate_value:
            result = separate_value + ' ' + result
        return result

    @staticmethod
    def make_specific_number_of_bits(value, bit_length):
        result = value
        if len(value) > bit_length:
            extra = len(value) - bit_length
            result = value[extra:]
        elif len(value) < bit_length:
            format_str = '{:0>' + str(bit_length) + '}'
            result = format_str.format(value)
        return result


class MipsInstructionsBase(QuestionBase):

    RTYPE_OP = 0
    RTYPE_SHAMT = 0

    RTYPE_VALUES = {
        'add': 0x20,
        'addu': 0x21,
        'sub': 0x22,
        'subu': 0x23,
        'and': 0x24,
        'or': 0x25,
        'xor': 0x26,
        'nor': 0x27,
        'slt': 0x2a,
        'sltu': 0x2b,
        'sll': 0x00,
        'srl': 0x02,
        'sra': 0x03,
        'jr': 0x08,
        'jalr': 0x09
    }

    RTYPE_GROUPS = {
        'no_shift': ['add', 'addu', 'sub', 'subu', 'and', 'nor', 'or', 'slt', 'sltu'],
        'no_rs': ['sll', 'srl', 'sra'],
        'no_rt_shift': ['jalr'],
        'no_rt_rd_shift': ['jr'],
    }

    ITYPE_VALUES = {
        'addi': 0x8,
        'addiu': 0x9,
        'andi': 0xc,
        'ori': 0xd,
        'slti': 0xa,
        'sltui': 0xb,
        'lw': 0x23,
        'sw': 0x2b,
        'lui': 0xf,
        'beq': 0x4,
        'bne': 0x5,
        'bgez': 0x1,
        'bgtz': 0x7,
        'blez': 0x6,
        'bltz': 0x1,

    }

    ITYPE_GROUPS = {
        'rt_rs': ['addi', 'addiu', 'andi', 'ori', 'slti', 'sltui'],
        'rs_end': ['lw', 'sw'],
        'no_rs': ['lui'],
        'rs_rt': ['beq', 'bne'],
        'no_rt': ['bgez', 'bgtz', 'blez', 'bltz']
    }

    JTYPE_VALUES = {
        'j': 0x2,
        'jal': 0x3
    }
    MIPS_INS_TYPES = {'R': RTYPE_VALUES, 'I': ITYPE_VALUES, 'J': JTYPE_VALUES}

    MEMORY_LOCATION_STARTING_POINT = 268435456  # this is 0x10000000

    @staticmethod
    def make_specific_number_of_bits(value, bit_length):
        result = value
        if len(value) > bit_length:
            extra = len(value) - bit_length
            result = value[extra:]
        elif len(value) < bit_length:
            format_str = '{:0>' + str(bit_length) + '}'
            result = format_str.format(value)
        return result

    @staticmethod
    def add_rtype(value):
        """
        :param value: dict {val1: int, val2: int}
        :return: dict {result: str hex 8 digit, overflow: boolean}
        """
        # convert both values to binary
        # get the most significant bit of both values
        val1_msb = '{:0>32}'.format(bin(value['val1'])[2:])[0]
        val2_msb = '{:0>32}'.format(bin(value['val2'])[2:])[0]

        # adding 2 values in int format
        result = value['val1'] + value['val2']
        result_hex = MipsInstructionsBase.make_specific_number_of_bits(hex(result)[2:], 8)

        # convert the result to binary and make it exactly 32 bits
        result_bin = MipsInstructionsBase.make_specific_number_of_bits(bin(result)[2:], 32)

        # check for overflow
        if val1_msb == val2_msb:
            if result_bin[0] != val1_msb:
                return result_hex, True
        return result_hex, False

    @staticmethod
    def addu_rtype(value):
        """
        :param value: dict {val1: int, val2: int}
        :return: dict {result: str hex 8 digit, overflow: boolean}
        """
        # adding 2 values in int format
        result = value['val1'] + value['val2']

        # convert to hex and check the length
        result_hex = MipsInstructionsBase.make_specific_number_of_bits(hex(result)[2:], 8)

        return result_hex, None


    @staticmethod
    def sub_rtype(value):

        value1_bin = '{:0>32}'.format(bin(value['val1'])[2:])
        value2_bin = '{:0>32}'.format(bin(value['val2'])[2:])

        val1_msb = value1_bin[0]
        val2_msb = value2_bin[0]
        overflow = False

        # create a list of the value binary digits and
        # complement every digit
        # and create a string from the list of complemented digits
        lst_int = list(map(int, value2_bin))
        complemented_int = list(map(lambda x: 1 - x, lst_int))
        complemented_str = ''.join(list(map(str, complemented_int)))

        # adding two values in int format and add the result to 1
        # then convert the result to binary
        expected = value['val1'] + int(complemented_str, 2) + 1
        formatted_expected = MipsInstructionsBase.make_specific_number_of_bits(hex(expected)[2:], 8)

        expected_bin = MipsInstructionsBase.make_specific_number_of_bits(bin(expected)[2:], 32)

        # check the overflow
        if val1_msb != val2_msb:
            if expected_bin[0] != val1_msb:
                overflow = True

        return formatted_expected, overflow

    @staticmethod
    def subu_rtype(value):
        value2_bin = '{:0>32}'.format(bin(value['val2'])[2:])

        # create a list of the value binary digits and
        # complement every digit
        # and create a string from the list of complemented digits
        lst_int = list(map(int, value2_bin))
        complemented_int = list(map(lambda x: 1 - x, lst_int))
        complemented_str = ''.join(list(map(str, complemented_int)))

        # adding two values in int format and add the result to 1
        # then convert the result to binary
        expected = value['val1'] + int(complemented_str, 2) + 1
        formatted_expected = MipsInstructionsBase.make_specific_number_of_bits(hex(expected)[2:], 8)

        return formatted_expected, None

    @staticmethod
    def and_rtype(value):
        result = value['val1'] & value['val2']
        result_hex = MipsInstructionsBase.make_specific_number_of_bits(hex(result)[2:], 8)
        return result_hex, None

    @staticmethod
    def or_rtype(value):
        result = value['val1'] | value['val2']
        result_hex = MipsInstructionsBase.make_specific_number_of_bits(hex(result)[2:], 8)
        return result_hex, None

    @staticmethod
    def xor_rtype(value):
        result = value['val1'] ^ value['val2']
        result_hex = MipsInstructionsBase.make_specific_number_of_bits(hex(result)[2:], 8)
        return result_hex, None

    @staticmethod
    def nor_rtype(value):
        result = ~ (value['val1'] | value['val2'])
        result_hex = MipsInstructionsBase.make_specific_number_of_bits(hex(result)[2:], 8)
        return result_hex, None

    @staticmethod
    def slt_rtype(value):
        val1_msb = '{:0>32}'.format(bin(value['val1'])[2:])[0]
        val2_msb = '{:0>32}'.format(bin(value['val2'])[2:])[0]

        if val1_msb == val2_msb:
            result = 1 if value['val1'] < value['val2'] else 0
        elif val1_msb == '0':
            result = 0
        elif val1_msb == '1':
            result = 1

        result_hex = MipsInstructionsBase.make_specific_number_of_bits(result, 8)
        return result_hex, None

    @staticmethod
    def sltu_rtype(value):
        result = 1 if value['val1'] < value['val2'] else 0
        result_hex = MipsInstructionsBase.make_specific_number_of_bits(result, 8)
        return result_hex, None

    @staticmethod
    def sll_rtype(value):
        result = value['val1'] << value['shift']
        result_hex = MipsInstructionsBase.make_specific_number_of_bits(hex(result)[2:], 8)
        return result_hex, None

    @staticmethod
    def srl_rtype(value):
        result = value['val1'] >> value['shift']
        result_hex = MipsInstructionsBase.make_specific_number_of_bits(hex(result)[2:], 8)
        return result_hex, None

    @staticmethod
    def sra_rtype(value):
        bin_value = '{:0>32}'.format(bin(value['val1'])[2:])
        most_significant_bit = bin_value[0]

        shifted = bin(value['val1'] >> value['shift'])[2:]
        prepared_sign = '{:' + str(most_significant_bit) + '>32}'
        result = prepared_sign.format(shifted)
        result_hex = '{:0>8}'.format(hex(int(result, 2))[2:])
        return result_hex, None

    @staticmethod
    def addi_itype(value):
        """
        :param value: dict {val1: int, val2: int}
        :return: dict {result: str hex 8 digit, overflow: boolean}
        """
        immediate_bin = '{:0>16}'.format(bin(value['val2'])[2:])

        # convert both values to binary
        # get the most significant bit of both values
        val1_msb = '{:0>32}'.format(bin(value['val1'])[2:])[0]
        val2_msb = immediate_bin[0]

        # extend the sign bit to get a 32 bit binary number
        prepared_sign = '{:' + val2_msb + '>32}'
        sign_extended_immediate_bin = prepared_sign.format(immediate_bin)

        # adding 2 values in int format
        result = value['val1'] + int(sign_extended_immediate_bin, 2)
        result_hex = MipsInstructionsBase.make_specific_number_of_bits(hex(result)[2:], 8)

        # convert the result to binary and make it exactly 32 bits
        result_bin = MipsInstructionsBase.make_specific_number_of_bits(bin(result)[2:], 32)

        # check for overflow
        if val1_msb == val2_msb:
            if result_bin[0] != val1_msb:
                return result_hex, True
        return result_hex, False

    @staticmethod
    def addiu_itype(value):
        """
        :param value: dict {val1: int, val2: int}
        :return: dict {result: str hex 8 digit, overflow: boolean}
        """
        immediate_bin = '{:0>16}'.format(bin(value['val2'])[2:])
        val2_msb = immediate_bin[0]

        # extend the sign bit to get a 32 bit binary number
        prepared_sign = '{:' + val2_msb + '>32}'
        sign_extended_immediate_bin = prepared_sign.format(immediate_bin)

        # adding 2 values in int format
        result = value['val1'] + int(sign_extended_immediate_bin, 2)

        # convert to hex and check the length
        result_hex = MipsInstructionsBase.make_specific_number_of_bits(hex(result)[2:], 8)

        return result_hex, None

    @staticmethod
    def slti_itype(value):
        immediate_bin = '{:0>16}'.format(bin(value['val2'])[2:])

        # convert both values to binary
        # get the most significant bit of both values
        val1_msb = '{:0>32}'.format(bin(value['val1'])[2:])[0]
        val2_msb = immediate_bin[0]

        # extend the sign bit to get a 32 bit binary number
        prepared_sign = '{:' + val2_msb + '>32}'
        sign_extended_immediate_bin = prepared_sign.format(immediate_bin)

        if val1_msb == val2_msb:
            result = 1 if value['val1'] < int(sign_extended_immediate_bin, 2) else 0
        elif val1_msb == '0':
            result = 0
        elif val1_msb == '1':
            result = 1

        result_hex = MipsInstructionsBase.make_specific_number_of_bits(str(result), 8)
        return result_hex, None

    @staticmethod
    def sltiu_itype(value):
        immediate_bin = '{:0>16}'.format(bin(value['val2'])[2:])

        # convert both values to binary
        # get the most significant bit of both values
        val2_msb = immediate_bin[0]

        # extend the sign bit to get a 32 bit binary number
        prepared_sign = '{:' + val2_msb + '>32}'
        sign_extended_immediate_bin = prepared_sign.format(immediate_bin)

        result = 1 if value['val1'] < int(sign_extended_immediate_bin, 2) else 0

        result_hex = MipsInstructionsBase.make_specific_number_of_bits(str(result), 8)
        return result_hex, None

    @staticmethod
    def andi_itype(value):
        result = value['val1'] & value['val2']
        result_hex = MipsInstructionsBase.make_specific_number_of_bits(hex(result)[2:], 8)
        return result_hex, None

    @staticmethod
    def ori_itype(value):
        result = value['val1'] | value['val2']
        result_hex = MipsInstructionsBase.make_specific_number_of_bits(hex(result)[2:], 8)
        return result_hex, None

    RTYPE_CALCULATIONS = {
        'add': add_rtype.__func__,
        'addu': addu_rtype.__func__,
        'sub': sub_rtype.__func__,
        'subu': subu_rtype.__func__,
        'and': and_rtype.__func__,
        'or': or_rtype.__func__,
        'xor': xor_rtype.__func__,
        'nor': nor_rtype.__func__,
        'slt': slt_rtype.__func__,
        'sltu': sltu_rtype.__func__,
        'sll': sll_rtype.__func__,
        'srl': srl_rtype.__func__,
        'sra': sra_rtype.__func__,
        'jalr': sra_rtype.__func__,
        'jr': sra_rtype.__func__,
    }

    ITYPE_CALCULATIONS = {
        'addi': addi_itype.__func__,
        'addiu': addiu_itype.__func__,
        'ori': ori_itype.__func__,
        'andi': andi_itype.__func__,
        'slti': slti_itype.__func__,
        'sltiu': sltiu_itype.__func__
    }

    PC_VALUE = 113983136

    @staticmethod
    def random_registers():
        register_dict = {}
        for i in range(32):
            random_small = random.choice([2, 3])
            pick_random = random.choice([random_small, 4, 4])
            random_hex = codecs.encode(os.urandom(pick_random), 'hex').decode()
            register_dict[str(i)] = '{:0>8}'.format(random_hex)
        return register_dict

    @staticmethod
    def random_memories():
        memory_dict = {}
        fst_memory = 268435456
        for i in range(32):
            memory_dict[hex(fst_memory+i)[2:]] = codecs.encode(os.urandom(1), 'hex').decode()

        return memory_dict

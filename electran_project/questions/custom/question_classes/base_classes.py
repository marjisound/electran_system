class QuestionBase:
    """Common base class for all questions"""
    wrong_answer_message = 'Wrong Answer'
    correct_answer_message = 'Correct Answer'
    wrong_format_message = 'Your answer did not have a correct format. Please try again'

    def generate_random(self):
        return None

    def expected_answer(self):
        return None

    def test_answer(self):
        return False


class BinaryHexBase(QuestionBase):
    """Common base class for all binary/hex questions"""

    @staticmethod
    def delete_binary_identifier(value):
        if value.startswith('0b') or value.startswith('0B'):
            return value[2:]
        else:
            return value

    @staticmethod
    def delete_hex_identifier(value):
        if value.startswith('0x') or value.startswith('0X'):
            return value[2:]
        else:
            return value

    @staticmethod
    def delete_octal_identifier(value):
        if value.startswith('0o') or value.startswith('0O'):
            return value[2:]
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

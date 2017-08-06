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
    def hex_to_binary(hex_num):
        return bin(int(hex_num, 16))

    @staticmethod
    def binary_to_hex(binary_num):
        return hex(int(binary_num, 2))

    @staticmethod
    def is_valid_hex(hex_num):
        if not hex_num or type(hex_num) != str:
            return {'result': False, 'message': 'the answer field must be filled'}
        else:
            try:
                int(hex_num, 16)
            except ValueError:
                return {'result': False, 'message': 'the answer did not have a correct binary format'}
            else:
                return {'result': True, 'message': ''}

    @staticmethod
    def is_valid_binary(binary_num):
        if not binary_num or type(binary_num) != str:
            return {'result': False, 'message': 'the answer field must be filled'}
        else:
            try:
                int(binary_num, 2)
            except ValueError:
                return {'result': False, 'message': 'the answer did not have a correct binary format'}
            else:
                return {'result': True, 'message': ''}
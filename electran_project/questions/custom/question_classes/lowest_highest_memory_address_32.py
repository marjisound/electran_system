from questions.custom.question_classes import lowest_highest_memory_address_16
import random


class Question(lowest_highest_memory_address_16.Question):

    def generate_random(self):

        address_bus_size = 32

        chip_identifier_length = random.randint(2, 20)
        chip_identifier = random.randint(0, (2**chip_identifier_length)-1)

        prepare_format = '{:0>' + str(chip_identifier_length) + '}'
        chip_identifier = prepare_format.format(bin(chip_identifier)[2:])

        memory_bit_length = address_bus_size - chip_identifier_length

        if memory_bit_length >= 20:
            memory_locations = str(2 ** (memory_bit_length-20)) + 'M'
        elif memory_bit_length >= 10:
            memory_locations = str(2 ** (memory_bit_length - 10)) + 'K'
        else:
            memory_locations = 2 ** memory_bit_length

        return {'bus_size': address_bus_size,
                'memory_locations': memory_locations,
                'pattern': chip_identifier}





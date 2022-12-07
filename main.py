from decimal import Decimal, getcontext
import sys


class AdaptiveArithmeticEncoding:

    def __init__(self, alphabet):
        self.alphabet = alphabet

    def encode(self, message: str):
        encoder_probabilities = []

        segment_min = Decimal(0.0)
        segment_max = Decimal(1.0)

        for i in range(len(message)):
            probability_table = self.calculate_probability_table(message[0:i])
            segment_probabilities = self.process_segment(probability_table, segment_min, segment_max)

            message_term = message[i]
            segment_min = segment_probabilities[message_term][0]
            segment_max = segment_probabilities[message_term][1]

            encoder_probabilities.append(segment_probabilities)

        segment_probabilities = self.process_segment(probability_table, segment_min, segment_max)
        encoder_probabilities.append(segment_probabilities)

        encoded_message = self.calculate_encoded_value(encoder_probabilities)

        return encoded_message

    def decode(self, encoded_message: Decimal, message_length: int):

        decoder_segment_probabilities = []
        decoded_message = ""

        segment_min = Decimal(0.0)
        segment_max = Decimal(1.0)

        for _ in range(message_length):
            probability_table = self.calculate_probability_table(decoded_message)
            segment_probabilities = self.process_segment(probability_table, segment_min, segment_max)

            for message_term, value in segment_probabilities.items():
                if encoded_message >= value[0] and encoded_message <= value[1]:
                    break

            decoded_message = decoded_message + message_term
            segment_min = segment_probabilities[message_term][0]
            segment_max = segment_probabilities[message_term][1]

            decoder_segment_probabilities.append(segment_probabilities)

        segment_probabilities = self.process_segment(probability_table, segment_min, segment_max)
        decoder_segment_probabilities.append(segment_probabilities)

        return decoded_message



    def process_segment(self, probability_table: dict, min_val: Decimal, max_val: Decimal):
        segment_probabilities = {}
        diff = max_val - min_val
        for i in range(len(probability_table.items())):
            term = list(probability_table.keys())[i]
            term_probability = Decimal(probability_table[term])
            cum_probability = term_probability * diff + min_val
            segment_probabilities[term] = [min_val, cum_probability]
            min_val = cum_probability
        return segment_probabilities

    def calculate_probability_table(self, previous_sequence: str):
        probability_table = {}
        for char in alphabet:
            probability_table[char] = self.laplace(char, previous_sequence, self.alphabet )

        return probability_table

    # Calculates conditional probability of character occurence after previously encoded sequence
    def laplace(self, current_char: str, previous_sequence: str, alphabet: set):
        current_frequency = previous_sequence.count(current_char)

        frequencies = []
        for letter in alphabet:
            frequencies.append(previous_sequence.count(letter))

        return (current_frequency + 1) / (sum(frequencies) + len(alphabet))

    def calculate_encoded_value(self, encoder: list):
        last_segment = list(encoder[-1].values())
        last_segment_values = []
        for sublist in last_segment:
            for element in sublist:
                last_segment_values.append(element)

        last_segment_min = min(last_segment_values)
        last_segment_max = max(last_segment_values)

        return (last_segment_min + last_segment_max) / 2

    

def get_message_alphabet(message: str):
    alphabet = set()
    for i in range(len(message)):
        alphabet.add(message[i])
    return alphabet

if __name__ == '__main__':
    getcontext().prec = 70
    print("Adaptive Arithmetic Encoding Algorithm")
    print("Please input message to encode:")
    
    message = input()
    alphabet = get_message_alphabet(message)
    algo = AdaptiveArithmeticEncoding(alphabet)

    print("Input message to encode: {message}".format(message=message))

    encoded_message = algo.encode(message)
    print("Encoded Message (one decimal number): {message}".format(message=encoded_message))

    decoded_message = algo.decode(encoded_message, len(message))
    print("Decoded Message: {message}".format(message=decoded_message))

    print("Input message is equal to decoded message: {result}".format(result=message == decoded_message))

    before_compression_size = len(message) * 8
    after_compression_size = sys.getsizeof(encoded_message)
    print("Size of input message (in bits):", before_compression_size)
    print("Size of encoded message (in bits):", after_compression_size)
    print("Compression ratio: {ratio}".format(ratio=after_compression_size/before_compression_size) )

    print("End")


import sys
from os import path

sys.path.append('../')

from utils.exceptions import ErrorCantBeDetectedException


class HammingCode:
    """

    """

    def __init__(self, **kwargs):
        """
        """
        if 'inp_data' in kwargs:
            self.inp_data = kwargs['inp_data'][::-1]
        else:
            self.inp_data = None

        if 'ham_code' in kwargs:
            self.ham_code = kwargs['ham_code']
        else:
            self.ham_code = None

        self.no_parity_bits = 0

    def cal_parity_bit_cnt(self):
        """
        """
        parity_cntr = 0
        while (len(self.inp_data) + parity_cntr + 1) > pow(2, parity_cntr):
            parity_cntr += 1

        return parity_cntr

    def position_parity_bits(self):
        """
        """
        no_parity_bits = self.cal_parity_bit_cnt()
        parity_pos = 0
        data_pos = 0
        par_pos_list = list()

        for i in range(0, no_parity_bits + len(self.inp_data)):
            pos = 2 ** parity_pos

            if pos == i + 1:
                par_pos_list.append(0)
                parity_pos += 1

            else:
                par_pos_list.append(int(self.inp_data[data_pos]))
                data_pos += 1

        return par_pos_list

    def calc_parity_bits(self):
        """
        """
        par_pos_list = self.position_parity_bits()
        parity_pos = 0

        for parity in range(0, len(par_pos_list)):
            pos = 2 ** parity_pos

            if pos == (parity + 1):
                start_index = pos - 1
                i = start_index
                xor_list = list()

                while i < len(par_pos_list):
                    block = par_pos_list[i:i + pos]
                    xor_list.extend(block)
                    i += 2 * pos

                for z in range(1, len(xor_list)):
                    par_pos_list[start_index] ^= xor_list[z]

                parity_pos += 1

        par_pos_list.reverse()

        return par_pos_list

    def generate_hamming_code(self):
        ham_code_lst = self.calc_parity_bits()
        return int(''.join(map(str, ham_code_lst)))

    def dtct_err_in_hamcode(self):
        data = list(self.ham_code)
        data.reverse()
        c, ch, j, r, error, h, parity_list, h_copy = 0, 0, 0, 0, 0, [], [], []

        for k in range(0, len(data)):
            p = (2 ** c)
            h.append(int(data[k]))
            h_copy.append(data[k])
            if p == (k + 1):
                c = c + 1

        self.process_parity_for_dtct_ham(ch, h, parity_list)
        parity_list.reverse()
        error = sum(int(parity_list) * (2 ** i) for i, parity_list in enumerate(parity_list[::-1]))

        if error == 0:
            print('There is no error in the hamming code received')

        elif error >= len(h_copy):
            print('Error cannot be detected')
            raise ErrorCantBeDetectedException

        else:
            print('Error is in', error, 'bit')

            if h_copy[error - 1] == '0':
                h_copy[error - 1] = '1'

            elif h_copy[error - 1] == '1':
                h_copy[error - 1] = '0'
                print('After correction hamming code is:- ')
            h_copy.reverse()
            print(int(''.join(map(str, h_copy))))

        # The following exception needs to be called when ever
        # We can't detect the error based on the code provided


    def process_parity_for_dtct_ham(self, ch, h, parity_list):
        for parity in range(0, (len(h))):
            ph = (2 ** ch)
            if (ph == (parity + 1)):

                startIndex = ph - 1
                i = startIndex
                toXor = []

                while (i < len(h)):
                    block = h[i:i + ph]
                    toXor.extend(block)
                    i += 2 * ph

                for z in range(1, len(toXor)):
                    h[startIndex] = h[startIndex] ^ toXor[z]
                parity_list.append(h[parity])
                ch += 1

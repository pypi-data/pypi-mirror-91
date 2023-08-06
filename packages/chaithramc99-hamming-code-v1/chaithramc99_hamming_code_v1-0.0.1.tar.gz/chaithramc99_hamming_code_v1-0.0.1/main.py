import argparse
from lib.hamming import HammingCode

parser = argparse.ArgumentParser(description='Hamming Code generator')


parser.add_argument('--inp_data',
                    type=str,
                    help="input data to generate hamming code!")
parser.add_argument('--ham_code',
                    type=str,
                    help="Detect the error in the hamming code!")

args = parser.parse_args()

if __name__ == "__main__":
    if args.inp_data is not None:
        ham_obj = HammingCode(inp_data = args.inp_data)
        print("The hamming code is ->",ham_obj.generate_hamming_code())

    if args.ham_code is not None:
        ham_obj = HammingCode(ham_code=args.ham_code)
        ham_obj.dtct_err_in_hamcode()




    #TO-DO implent printing
import math


def bin_hex(exp_bin):
    hexstr=f'{int(exp_bin,2):X}'
    return hexstr

def hex_bin(exp_hex):
    binstr="{0:08b}".format(int(exp_hex,16))
    return binstr

def hex_dec(exp_hex):
    return int(exp_hex,16)

def bin_dec(exp_bin):
    return int(exp_bin,2)

def main():
    num="FF"
    print(hex_bin(num))
main()

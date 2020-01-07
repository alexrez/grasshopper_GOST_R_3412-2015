import argparse
import os
import sys
import testfiles


parser = argparse.ArgumentParser(prog='grasshopper', usage='%(prog)s [options] [param]',
                                 description='GOST 34.12-2015 ("Grasshopper")')

parser.add_argument('-mode', dest='mode', type=str)
parser.add_argument('-k', dest='key', type=str, help='key file')
parser.add_argument('-i', dest='infile', type=str, help='source file (default: stdin)')
parser.add_argument('-o', dest='outfile', type=str, help='result file (default: stdout)')
parser.add_argument('-v', dest='IV', type=str, help='IV file')
parser.add_argument('-e', dest='encrypt', default=False, action='store_const', const=True, help='encryption mode')
parser.add_argument('-d', dest='decrypt', default=False, action='store_const', const=True, help='decrypt mode')
parser.add_argument('-t', dest='test', default=False, action='store_const', const=True, help='compare encryption/decrypt result with given files')


class Grasshopper():
    def __init__(self):
        self._block_size = 16

        self.__pi = [252, 238, 221, 17,  207, 110, 49,  22,  251, 196, #0
                     250, 218, 35,  197, 4,   77,  233, 119, 240, 219,
                     147, 46,  153, 186, 23,  54,  241, 187, 20,  205, #2
                     95,  193, 249, 24,  101, 90,  226, 92,  239, 33,
                     129, 28,  60,  66,  139, 1,   142, 79,  5,   132, #4
                     2,   174, 227, 106, 143, 160, 6,   11,  237, 152,
                     127, 212, 211, 31,  235, 52,  44,  81,  234, 200, #6
                     72,  171, 242, 42,  104, 162, 253, 58,  206, 204,
                     181, 112, 14,  86,  8,   12,  118, 18,  191, 114, #8
                     19,  71,  156, 183, 93,  135, 21,  161, 150, 41,
                     16,  123, 154, 199, 243, 145, 120, 111, 157, 158, #10
                     178, 177, 50,  117, 25,  61,  255, 53,  138, 126,
                     109, 84,  198, 128, 195, 189, 13,  87,  223, 245, #12
                     36,  169, 62,  168, 67,  201, 215, 121, 214, 246,
                     124, 34,  185, 3,   224, 15,  236, 222, 122, 148, #14
                     176, 188, 220, 232, 40,  80,  78,  51,  10,  74,
                     167, 151, 96,  115, 30,  0,   98,  68,  26,  184, #16
                     56,  130, 100, 159, 38,  65,  173, 69,  70,  146,
                     39,  94,  85,  47,  140, 163, 165, 125, 105, 213, #18
                     149, 59,  7,   88,  179, 64,  134, 172, 29,  247,
                     48,  55,  107, 228, 136, 217, 231, 137, 225, 27,  #20
                     131, 73,  76,  63,  248, 254, 141, 83,  170, 144,
                     202, 216, 133, 97,  32,  113, 103, 164, 45,  43,  #22
                     9,   91,  203, 155, 37,  208, 190, 229, 108, 82,
                     89,  166, 116, 210, 230, 244, 180, 192, 209, 102, #24
                     175, 194, 57,  75,  99,  182]

        self.__pi_inverse = [0] * 256
        for i, pi in enumerate(self.__pi):
            self.__pi_inverse[pi] = i

        self._GF = [0] * 256
        self._GF[0] = 1
        self._logGF = [0] * 256

        mod = 255
        xor_const = 195 # p(x) = x**8 + x**7 + x**6 + x + 1 => 0001 1100 0011 => 451 (mod 256) = 195
        for i in range(1, 256):
            tmp = (self._GF[i - 1] << 1)
            if tmp > 255:
                tmp = (tmp & mod) ^ xor_const
            self._GF[i] = tmp
            self._logGF[tmp] = i

        self._logGF[0] = 0
        self._logGF[1] = 0

        self.__perm = [self._logGF[i] for i in [148, 32, 133, 16, 194, 192, 1, 251, 1, 192, 194, 16, 133, 32, 148, 1]]

    def init_key(self, key):
        self._key = [0] * 11
        self._key[1] = key[:16]
        self._key[2] = key[16:]
        
        # c_all = []
        for i in range (1, 5):
            tmp = [0] * 15
            tmp_c_i = [i for i in range(8 * (i - 1) + 1, 8 * (i - 1) + 9)]
            c = [self._L(tmp + [c_i]) for c_i in tmp_c_i]
            # c_all.append(c)
            # a = []
            a1 = self._key[2 * i - 1]
            a0 = self._key[2 * i]
            for it in range(8):
                f = self._LSX(c[it], a1)
                tmp_a = a1
                a1 = [a_i ^ k_i for a_i, k_i in zip(f, a0)]
                a0 = tmp_a
                # a.append((a1, a0))
            # return a
            self._key[2 * i + 1] = a1
            self._key[2 * i + 2] = a0
        # return c_all

    def _Sbox(self, word):
        return self.__pi[word]

    def _Sbox_inverse(self, word):
        return self.__pi_inverse[word]

    def reduce_xor(self, l):
        res = l[0]
        for elem in l[1:]:
            res = res ^ elem
        return res

    def _R_round(self, a):
        l_a = self.reduce_xor(list(map(lambda pair: self._GF[(pair[0] + self._logGF[pair[1]]) % 255] if pair[1] != 0 else 0 ,
                                        zip(self.__perm, a)))) 
        return [l_a] + a[:-1]

    def _R_round_inverse(self, a):
        l_a = self.reduce_xor(list(map(lambda pair: self._GF[(pair[0] + self._logGF[pair[1]]) % 255] if pair[1] != 0 else 0 ,
                                        zip(self.__perm, a[1:] + [a[0]])))) 
        return a[1:] + [l_a]

    def _L(self, a):
        for r_round in range(16):
            a = self._R_round(a)
        return a

    def _L_inverse(self, a):
        for r_round in range(16):
            a = self._R_round_inverse(a)
        return a

    def _K(self, a, key):
        return [a_i ^ k_i for a_i, k_i in zip(a, key)]

    def _LSX(self, a, key):
        return self._L([self._Sbox(word) for word in self._K(a, key)])

    def _LSX_inverse(self, a, key):
        return [self._Sbox_inverse(word) for word in self._L_inverse(self._K(a, key))]

    def text_to_blocks(self, text):
        return [text[i: i + self._block_size] for i in range(0, len(text), self._block_size)]

    def encrypt_1_block(self, block):
        for it in range(1, 10):
            block = self._LSX(block, self._key[it])
        return self._K(block, self._key[10])

    def encrypt(self, blocked_text):
        return [self.encrypt_1_block(block) for block in blocked_text]

    def encrypt_ofb(self, blocked_text, iv):
        encrypted_text = []
        # len_bt = len(blocked_text) - 1
        for i, block in enumerate(blocked_text):
            iv_head = self.encrypt_1_block(iv[ :self._block_size])
            encrypted_text.append(self._K(block, iv_head))
            iv = iv[self._block_size: ] + iv_head
            # if i % 1000 == 0:
                # print("completed {} out of {}".format(i, len_bt))
        # print("completed {} out of {}".format(i, len_bt))

        return encrypted_text

    def decrypt_1_block(self, block):
        for it in range(9):
            block = self._LSX_inverse(block, self._key[10 - it])
        return self._K(block, self._key[1])

    def decrypt(self, blocked_text):
        return [self.decrypt_1_block(block) for block in blocked_text]

    def decrypt_ofb(self, blocked_text, iv):
        decrypted_text = []
        # len_bt = len(blocked_text) - 1
        for i, block in enumerate(blocked_text):
            iv_head = self.encrypt_1_block(iv[ :self._block_size])
            decrypted_text.append(self._K(block, iv_head))
            iv = iv[self._block_size: ] + iv_head
            # if i % 1000 == 0:
                # print("completed {} out of {}".format(i, len_bt))
        # print("completed {} out of {}".format(i, len_bt))

        return decrypted_text


if __name__ == '__main__':
    args = parser.parse_args()
    try:
        if not args.test:
            gr_cipher = Grasshopper()

            if args.key is None:
                raise ValueError('Key-file is not allowed')
            key_path = os.path.normpath(os.path.expanduser(args.key))
            with open(key_path, 'rb') as key_file:
                gr_cipher.init_key([sym for sym in key_file.read()])

            if args.infile is None:
                input_text = gr_cipher.text_to_blocks([ord(sym) for sym in input()])
            else:
                in_path = os.path.normpath(os.path.expanduser(args.infile))
                with open(in_path, 'rb') as input_file:
                    input_text = gr_cipher.text_to_blocks([sym for line in input_file.readlines() for sym in line])

            if args.IV is None:
                iv = [0] * 16
            else:
                iv_path = os.path.normpath(os.path.expanduser(args.IV))
                with open(iv_path, 'rb') as iv_file:
                    iv = [sym for line in iv_file.readlines() for sym in line]

            if args.encrypt:
                if args.mode == 'ofb':
                    ciphered_text = gr_cipher.encrypt_ofb(input_text, iv)
                ciphered_text = gr_cipher.encrypt(input_text)
            if args.decrypt:
                if args.mode == 'ofb':
                    ciphered_text = gr_cipher.decrypt_ofb(input_text, iv)
                ciphered_text = gr_cipher.decrypt(input_text)

            if args.outfile is None:
                result_text = []
                sys.stdout.buffer.write(bytes([w for block in ciphered_text for w in block]))
                
            else:
                out_file = os.path.normpath(os.path.expanduser(args.outfile))
                with open(out_file, 'wb') as out_file:
                    out_file.write(bytes([w for block in ciphered_text for w in block]))

        else:
            # # # TESTS
            testfiles.test_files(args.key, args.infile, args.outfile)


    except ValueError as err:
        print(err, '\n')



# запуск тестов и проверка соответствия 'plaintext' и 'ciphertext' тому как работает программа на зашифрование и дешифрование
# python3 grasshopper.py -t -k tests/1block/test_0/key -i tests/1block/test_0/plaintext -o tests/1block/test_0/ciphertext

# запуск программы на зашифрование с указанными ключом и входным/выходным файлами
# python3 grasshopper.py -e -k tests/1block/test_0/key -i tests/1block/test_0/plaintext -o ciphertext_test

# запуск программы на зашифрование с указанными ключом и входным/выходным файлами в режиме ofb
# python3 grasshopper.py -e -k tests/ecb_completion2/test_pdf/key -i tests/ecb_completion2/test_pdf/plaintext.pdf -o ciphertext_test  -mode ofb
# python3 grasshopper.py -d -k tests/ecb_completion2/test_pdf/key -i ciphertext_test -o plaintext_test.pdf  -mode ofb

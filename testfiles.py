import os
import sys
import grasshopper

def test_files(key_, plaintext_, ciphertext_):
    gr_cipher = grasshopper.Grasshopper()

    if key_ is None:
        raise ValueError('Key-file is not allowed')
    key_path = os.path.normpath(os.path.expanduser(key_))
    with open(key_path, 'rb') as key_file:
        gr_cipher.init_key([sym for sym in key_file.read()])

    if plaintext_ is None:
        raise ValueError('File with ciphertext is not allowed')
    else:
        plaintext_path = os.path.normpath(os.path.expanduser(plaintext_))
        with open(plaintext_path, 'rb') as plaintext_file:
            plaintext = [sym for line in plaintext_file.readlines() for sym in line]
    encrypted_text = [w for block in gr_cipher.encrypt(gr_cipher.text_to_blocks(plaintext)) for w in block]

    if ciphertext_ is None:
        raise ValueError('File with ciphertext is not allowed')
    else:
        ciphertext_path = os.path.normpath(os.path.expanduser(ciphertext_))
        with open(ciphertext_path, 'rb') as ciphertext_file:
            ciphertext = [sym for line in ciphertext_file.readlines() for sym in line]

    decrypted_text = [w for block in gr_cipher.decrypt(gr_cipher.text_to_blocks(ciphertext)) for w in block]

    out_file = os.path.normpath(os.path.expanduser('test_encryption'))
    with open(out_file, 'wb') as out_file:
        out_file.write(bytes([w for w in encrypted_text]))

    out_file = os.path.normpath(os.path.expanduser('test_decryption'))
    with open(out_file, 'wb') as out_file:
        out_file.write(bytes([w for w in decrypted_text]))

    print("\tTESTS:\n")
    print('Encrypt("{}") == "{}"\t>>>>>\t{}\n\nDecrypt("{}") == "{}"\t>>>>>\t{}'.format(plaintext_, ciphertext_, encrypted_text == ciphertext,
                                                                           ciphertext_, plaintext_, decrypted_text == plaintext))
    print('\n')



# запуск тестов и проверка соответствия 'plaintext' и 'ciphertext' тому как работает программа на зашифрование и дешифрование

# python3 grasshopper.py -t -k tests/1block/test_0/key -i tests/1block/test_0/plaintext -o tests/1block/test_0/ciphertext
# python3 grasshopper.py -t -k tests/1block/test_1/key -i tests/1block/test_1/plaintext -o tests/1block/test_1/ciphertext
# python3 grasshopper.py -t -k tests/1block/test_2/key -i tests/1block/test_2/plaintext -o tests/1block/test_2/ciphertext
# python3 grasshopper.py -t -k tests/1block/test_3/key -i tests/1block/test_3/plaintext -o tests/1block/test_3/ciphertext
# python3 grasshopper.py -t -k tests/1block/test_4/key -i tests/1block/test_4/plaintext -o tests/1block/test_4/ciphertext
# python3 grasshopper.py -t -k tests/1block/test_5/key -i tests/1block/test_5/plaintext -o tests/1block/test_5/ciphertext
# python3 grasshopper.py -t -k tests/1block/test_6/key -i tests/1block/test_6/plaintext -o tests/1block/test_6/ciphertext
# python3 grasshopper.py -t -k tests/1block/test_7/key -i tests/1block/test_7/plaintext -o tests/1block/test_7/ciphertext
# python3 grasshopper.py -t -k tests/1block/test_8/key -i tests/1block/test_8/plaintext -o tests/1block/test_8/ciphertext
# python3 grasshopper.py -t -k tests/1block/test_9/key -i tests/1block/test_9/plaintext -o tests/1block/test_9/ciphertext
# python3 grasshopper.py -t -k tests/1block/test_standard/key -i tests/1block/test_standard/plaintext -o tests/1block/test_standard/ciphertext



import grasshopper

block_size = 16

 # # TESTS
print("\n<<<\tofb GOST tests\t>>>")

def test_hex(text):
      s = [hex(w).split('x')[-1] for w in text]
      return ''.join(i if len(i) == 2 else '0' + i for i in s)

cipher_test = grasshopper.Grasshopper()
K = '8899aabbccddeeff0011223344556677fedcba98765432100123456789abcdef'
cipher_test.init_key([int(K[i: i + 2], 16) for i in range(0, len(K), 2)])

IV = '1234567890abcef0a1b2c3d4e5f0011223344556677889901213141516171819'
iv_ = [int(IV[i: i + 2], 16) for i in range(0, len(IV), 2)]


print("\n\tEncrypt test:\n")

message = '1122334455667700ffeeddccbbaa9988'
a = cipher_test.text_to_blocks([int(message[i: i + 2], 16) for i in range(0, len(message), 2)])
iv_head = cipher_test.encrypt_1_block(iv_[ :block_size])
# print(test_hex(iv_head))
print('Input_block(1234567890abcef0a1b2c3d4e5f00112)\t== Output_block(90a2391de4e25c2400f1a49232d0241d)\t>>>>>\t',
      test_hex(iv_head) == '90a2391de4e25c2400f1a49232d0241d')
print('Encrypt(1122334455667700ffeeddccbbaa9988)\t== 81800a59b1842b24ff1f795e897abd95\t\t\t>>>>>\t',
      ''.join([test_hex(a_i) for a_i in cipher_test.encrypt_ofb(a, iv_)]) == '81800a59b1842b24ff1f795e897abd95')
message = '81800a59b1842b24ff1f795e897abd95'
a = cipher_test.text_to_blocks([int(message[i: i + 2], 16) for i in range(0, len(message), 2)])
print('Decrypt(81800a59b1842b24ff1f795e897abd95)\t== 1122334455667700ffeeddccbbaa9988\t\t\t>>>>>\t',
      ''.join([test_hex(a_i) for a_i in cipher_test.decrypt_ofb(a, iv_)]) == '1122334455667700ffeeddccbbaa9988', '\n')
iv_ = iv_[block_size: ] + iv_head

message = '00112233445566778899aabbcceeff0a'
a = cipher_test.text_to_blocks([int(message[i: i + 2], 16) for i in range(0, len(message), 2)])
iv_head = cipher_test.encrypt_1_block(iv_[ :block_size])
print('Input_block(23344556677889901213141516171819)\t== Output_block(ed4a659440d99cc3072c8b8d517dd9b5)\t>>>>>\t',
      test_hex(iv_head) == 'ed4a659440d99cc3072c8b8d517dd9b5')
print('Encrypt(00112233445566778899aabbcceeff0a)\t== ed5b47a7048cfab48fb521369d9326bf\t\t\t>>>>>\t',
      ''.join([test_hex(a_i) for a_i in cipher_test.encrypt_ofb(a, iv_)]) == 'ed5b47a7048cfab48fb521369d9326bf')
message = 'ed5b47a7048cfab48fb521369d9326bf'
a = cipher_test.text_to_blocks([int(message[i: i + 2], 16) for i in range(0, len(message), 2)])
print('Decrypt(ed5b47a7048cfab48fb521369d9326bf)\t== 00112233445566778899aabbcceeff0a\t\t\t>>>>>\t',
      ''.join([test_hex(a_i) for a_i in cipher_test.decrypt_ofb(a, iv_)]) == '00112233445566778899aabbcceeff0a', '\n')
iv_ = iv_[block_size: ] + iv_head

message = '112233445566778899aabbcceeff0a00'
a = cipher_test.text_to_blocks([int(message[i: i + 2], 16) for i in range(0, len(message), 2)])
iv_head = cipher_test.encrypt_1_block(iv_[ :block_size])
print('Input_block(90a2391de4e25c2400f1a49232d0241d)\t== Output_block(778064e869c6cf3951a55c30fed78013)\t>>>>>\t',
      test_hex(iv_head) == '778064e869c6cf3951a55c30fed78013')
print('Encrypt(112233445566778899aabbcceeff0a00)\t== 66a257ac3ca0b8b1c80fe7fc10288a13\t\t\t>>>>>\t',
      ''.join([test_hex(a_i) for a_i in cipher_test.encrypt_ofb(a, iv_)]) == '66a257ac3ca0b8b1c80fe7fc10288a13', '\n')
iv_ = iv_[block_size: ] + iv_head

message = '2233445566778899aabbcceeff0a0011'
a = cipher_test.text_to_blocks([int(message[i: i + 2], 16) for i in range(0, len(message), 2)])
iv_head = cipher_test.encrypt_1_block(iv_[ :block_size])
print('Input_block(ed4a659440d99cc3072c8b8d517dd9b5)\t== Output_block(020dff9500640ef90a92eead099a3141)\t>>>>>\t',
      test_hex(iv_head) == '020dff9500640ef90a92eead099a3141')
print('Encrypt(2233445566778899aabbcceeff0a0011)\t== 203ebbc066138660a0292243f6903150\t\t\t>>>>>\t',
      ''.join([test_hex(a_i) for a_i in cipher_test.encrypt_ofb(a, iv_)]) == '203ebbc066138660a0292243f6903150')
message = '203ebbc066138660a0292243f6903150'
a = cipher_test.text_to_blocks([int(message[i: i + 2], 16) for i in range(0, len(message), 2)])
print('Decrypt(203ebbc066138660a0292243f6903150)\t== 2233445566778899aabbcceeff0a0011\t\t\t>>>>>\t',
      ''.join([test_hex(a_i) for a_i in cipher_test.decrypt_ofb(a, iv_)]) == '2233445566778899aabbcceeff0a0011', '\n')
iv_ = iv_[block_size: ] + iv_head

print('\n')






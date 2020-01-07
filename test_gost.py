import grasshopper

 # # TESTS
print("\n<<<\tGOST tests\t>>>")

def test_hex(text):
    s = [hex(w).split('x')[-1] for w in text]
    return ''.join(i if len(i) == 2 else '0' + i for i in s)

cipher_test = grasshopper.Grasshopper()


message0 = 'ffeeddccbbaa99881122334455667700'
S0 = [int(message0[i: i + 2], 16) for i in range(0, len(message0), 2)]
message1 = 'b66cd8887d38e8d77765aeea0c9a7efc'
S1 = [int(message1[i: i + 2], 16) for i in range(0, len(message1), 2)]
message2 = '559d8dd7bd06cbfe7e7b262523280d39'
S2 = [int(message2[i: i + 2], 16) for i in range(0, len(message2), 2)]
message3 = '0c3322fed531e4630d80ef5c5a81c50b'
S3 = [int(message3[i: i + 2], 16) for i in range(0, len(message3), 2)]

print("\n\tSbox tests:\n")
print('S(ffeeddccbbaa99881122334455667700) == b66cd8887d38e8d77765aeea0c9a7efc\t>>>>>\t',
      test_hex([cipher_test._Sbox(m) for m in S0]) == 'b66cd8887d38e8d77765aeea0c9a7efc')

print('S(b66cd8887d38e8d77765aeea0c9a7efc) == 559d8dd7bd06cbfe7e7b262523280d39\t>>>>>\t',
      test_hex([cipher_test._Sbox(m) for m in S1]) == '559d8dd7bd06cbfe7e7b262523280d39')

print('S(559d8dd7bd06cbfe7e7b262523280d39) == 0c3322fed531e4630d80ef5c5a81c50b\t>>>>>\t',
      test_hex([cipher_test._Sbox(m) for m in S2]) == '0c3322fed531e4630d80ef5c5a81c50b')

print('S(0c3322fed531e4630d80ef5c5a81c50b) == 23ae65633f842d29c5df529c13f5acda\t>>>>>\t',
      test_hex([cipher_test._Sbox(m) for m in S3]) ==  '23ae65633f842d29c5df529c13f5acda')


message0 = '00000000000000000000000000000100'
S0 = [int(message0[i: i + 2], 16) for i in range(0, len(message0), 2)]
message1 = '94000000000000000000000000000001'
S1 = [int(message1[i: i + 2], 16) for i in range(0, len(message1), 2)]
message2 = 'a5940000000000000000000000000000'
S2 = [int(message2[i: i + 2], 16) for i in range(0, len(message2), 2)]
message3 = '64a59400000000000000000000000000'
S3 = [int(message3[i: i + 2], 16) for i in range(0, len(message3), 2)]

print("\n\tR tests:\n")
print('R(00000000000000000000000000000100) == 94000000000000000000000000000001\t>>>>>\t',
      test_hex(cipher_test._R_round(S0)) == '94000000000000000000000000000001')

print('R(94000000000000000000000000000001) == a5940000000000000000000000000000\t>>>>>\t',
      test_hex(cipher_test._R_round(S1)) == 'a5940000000000000000000000000000')

print('R(a5940000000000000000000000000000) == 64a59400000000000000000000000000\t>>>>>\t',
      test_hex(cipher_test._R_round(S2)) == '64a59400000000000000000000000000')

print('R(64a59400000000000000000000000000) == 0d64a594000000000000000000000000\t>>>>>\t',
      test_hex(cipher_test._R_round(S3)) == '0d64a594000000000000000000000000')


message0 = '64a59400000000000000000000000000'
S0 = [int(message0[i: i + 2], 16) for i in range(0, len(message0), 2)]
message1 = 'd456584dd0e3e84cc3166e4b7fa2890d'
S1 = [int(message1[i: i + 2], 16) for i in range(0, len(message1), 2)]
message2 = '79d26221b87b584cd42fbc4ffea5de9a'
S2 = [int(message2[i: i + 2], 16) for i in range(0, len(message2), 2)]
message3 = '0e93691a0cfc60408b7b68f66b513c13'
S3 = [int(message3[i: i + 2], 16) for i in range(0, len(message3), 2)]

print("\n\tL tests:\n")
print('L(64a59400000000000000000000000000) == d456584dd0e3e84cc3166e4b7fa2890d\t>>>>>\t',
      test_hex(cipher_test._L(S0)) == 'd456584dd0e3e84cc3166e4b7fa2890d')

print('L(d456584dd0e3e84cc3166e4b7fa2890d) == 79d26221b87b584cd42fbc4ffea5de9a\t>>>>>\t',
      test_hex(cipher_test._L(S1)) == '79d26221b87b584cd42fbc4ffea5de9a')

print('L(79d26221b87b584cd42fbc4ffea5de9a) == 0e93691a0cfc60408b7b68f66b513c13\t>>>>>\t',
      test_hex(cipher_test._L(S2)) == '0e93691a0cfc60408b7b68f66b513c13')

print('L(0e93691a0cfc60408b7b68f66b513c13) == e6a8094fee0aa204fd97bcb0b44b8580\t>>>>>\t',
      test_hex(cipher_test._L(S3)) == 'e6a8094fee0aa204fd97bcb0b44b8580')


print("\n\tKEYS tests:\n")
k_str = '8899aabbccddeeff0011223344556677fedcba98765432100123456789abcdef'
k = [int(k_str[i: i + 2], 16) for i in range(0, len(k_str), 2)]
cipher_test.init_key(k)

# print(test_hex(cipher_test.init_key(k)[0]) == 'c3d5fa01ebe36f7a9374427ad7ca8949')

# c = cipher_test.init_key(k)
# c_test = ['6ea276726c487ab85d27bd10dd849401', 'dc87ece4d890f4b3ba4eb92079cbeb02', 'b2259a96b4d88e0be7690430a44f7f03',
#           '7bcd1b0b73e32ba5b79cb140f2551504', '156f6d791fab511deabb0c502fd18105', 'a74af7efab73df160dd208608b9efe06',
#           'c9e8819dc73ba5ae50f5b570561a6a07', 'f6593616e6055689adfba18027aa2a08']
# for i, c_i in enumerate(c[0]):
#     print(test_hex(c_i), test_hex(c_i) == c_test[i])

# f = cipher_test.init_key(k)
# f_test = [('c3d5fa01ebe36f7a9374427ad7ca8949', '8899aabbccddeeff0011223344556677'),
#         ('37777748e56453377d5e262d90903f87', 'c3d5fa01ebe36f7a9374427ad7ca8949'),
#         ('f9eae5f29b2815e31f11ac5d9c29fb01', '37777748e56453377d5e262d90903f87'),
#         ('e980089683d00d4be37dd3434699b98f', 'f9eae5f29b2815e31f11ac5d9c29fb01'),
#         ('b7bd70acea4460714f4ebe13835cf004', 'e980089683d00d4be37dd3434699b98f'),
#         ('1a46ea1cf6ccd236467287df93fdf974', 'b7bd70acea4460714f4ebe13835cf004'),
#         ('3d4553d8e9cfec6815ebadc40a9ffd04', '1a46ea1cf6ccd236467287df93fdf974'),
#         ('db31485315694343228d6aef8cc78c44', '3d4553d8e9cfec6815ebadc40a9ffd04')]

# for i, f_i in enumerate(f):
#     print(test_hex(f_i[0]), test_hex(f_i[0]) == f_test[i][0], f_test[i][0])
#     print(test_hex(f_i[1]), test_hex(f_i[1]) == f_test[i][1], f_test[i][1])

iter_keys = [test_hex(key) for key in cipher_test._key[1:]]

print('K1 == 8899aabbccddeeff0011223344556677\t>>>>>\t', 
      iter_keys[0]== '8899aabbccddeeff0011223344556677')

print('K2 == fedcba98765432100123456789abcdef\t>>>>>\t', 
      iter_keys[1] == 'fedcba98765432100123456789abcdef')

print('K3 == db31485315694343228d6aef8cc78c44\t>>>>>\t', 
      iter_keys[2] == 'db31485315694343228d6aef8cc78c44')

print('K4 == 3d4553d8e9cfec6815ebadc40a9ffd04\t>>>>>\t', 
      iter_keys[3] == '3d4553d8e9cfec6815ebadc40a9ffd04')

print('K5 == 57646468c44a5e28d3e59246f429f1ac\t>>>>>\t', 
      iter_keys[4] == '57646468c44a5e28d3e59246f429f1ac')

print('K6 == bd079435165c6432b532e82834da581b\t>>>>>\t', 
      iter_keys[5] == 'bd079435165c6432b532e82834da581b')

print('K7 == 51e640757e8745de705727265a0098b1\t>>>>>\t', 
      iter_keys[6] == '51e640757e8745de705727265a0098b1')

print('K8 == 5a7925017b9fdd3ed72a91a22286f984\t>>>>>\t', 
      iter_keys[7] == '5a7925017b9fdd3ed72a91a22286f984')

print('K9 == bb44e25378c73123a5f32f73cdb6e517\t>>>>>\t', 
      iter_keys[8] == 'bb44e25378c73123a5f32f73cdb6e517')

print('K10 == 72e9dd7416bcf45b755dbaa88e4a4043\t>>>>>\t', 
      iter_keys[9] == '72e9dd7416bcf45b755dbaa88e4a4043')


# message = '1122334455667700ffeeddccbbaa9988'
message = '00112233445566778899aabbcceeff0a'
a = cipher_test.text_to_blocks([int(message[i: i + 2], 16) for i in range(0, len(message), 2)])

print("\n\tEncrypt test:\n")
print('Encrypt(00112233445566778899aabbcceeff0a) == b429912c6e0032f9285452d76718d08b\t>>>>>\t',
      ''.join([test_hex(a_i) for a_i in cipher_test.encrypt(a)]) == 'b429912c6e0032f9285452d76718d08b')


message = 'f0ca33549d247ceef3f5a5313bd4b157'
a = cipher_test.text_to_blocks([int(message[i: i + 2], 16) for i in range(0, len(message), 2)])

print("\n\tDecrypt test:\n")
print('tDecrypt(f0ca33549d247ceef3f5a5313bd4b157) == 112233445566778899aabbcceeff0a00\t>>>>>\t',
      ''.join([test_hex(a_i) for a_i in cipher_test.decrypt(a)]) == '112233445566778899aabbcceeff0a00')

print('\n')






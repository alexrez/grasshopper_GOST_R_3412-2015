Программа написана в учебных целях в рамках курса "Введение в криптографию" (ВМК МГУ, 2019)
Реализован алгоритм "Кузнечик" с режимом шифрования гаммирование с обратной связью по выходу.

grasshopper.py:

  -h, --help  show this help message and exit
  -mode MODE
  -k KEY      key file
  -i INFILE   source file (default: stdin)
  -o OUTFILE  result file (default: stdout)
  -v IV       IV file
  -e          encryption mode
  -d          decrypt mode
  -t          compare encryption/decrypt result with given files

запуск тестов и проверка соответствия 'plaintext' и 'ciphertext' тому как работает программа на зашифрование и дешифрование:
grasshopper.py -t -k tests/1block/test_0/key -i tests/1block/test_0/plaintext -o tests/1block/test_0/ciphertext

запуск программы на зашифрование/расшифрование с указанными ключом и входным/выходным файлами:
grasshopper.py -e -k keyfile -i plaintext -o ciphertext
grasshopper.py -d -k keyfile -i ciphertext -o plaintext

запуск программы на зашифрование/расшифрование с указанными ключом и входным/выходным файлами в режиме ofb:
grasshopper.py -e -k keyfile -i plaintext -o ciphertext  -mode ofb
grasshopper.py -d -k keyfile -i ciphertext -o plaintext  -mode ofb

проверка тестов ГОСТ 3412-2015:
test_gost.py

проверка тестов ГОСТ 3413-2015 для режима гаммирования с обратной связью по выходу (ofb):
test_gost_ofb.py
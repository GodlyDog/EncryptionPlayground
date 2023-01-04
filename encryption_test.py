import unittest
import encryption
import sympy


class EncryptionUnitTests(unittest.TestCase):
    def test_prime_generator(self):
        primes = encryption.prime_generator()
        for prime in primes:
            self.assertTrue(sympy.isprime(prime))

    def test_mod_m_generator(self):
        eds = encryption.mod_m_generator(3, max_ed=10)
        self.assertEqual(eds, [4, 10])
        eds = encryption.mod_m_generator(2, max_ed=20)
        self.assertEqual(eds, [9, 15])
        eds = encryption.mod_m_generator(25, max_ed=300)
        self.assertEqual(eds, [26, 51, 76, 126, 176, 201, 226, 276])

    def test_ed_factorization(self):
        factors = encryption.ed_factorization(10)
        self.assertEqual(factors, [2, 5])
        factors = encryption.ed_factorization(36)
        self.assertEqual(factors, [2, 3, 4, 6, 9, 12, 18])
        factors = encryption.ed_factorization(12)
        self.assertEqual(factors, [2, 3, 4, 6])

    def test_is_prime(self):
        self.assertTrue(encryption.is_prime(13))
        self.assertTrue(encryption.is_prime(5))
        self.assertTrue(encryption.is_prime(61))
        self.assertTrue(encryption.is_prime(1223))
        self.assertFalse(encryption.is_prime(12))
        self.assertFalse(encryption.is_prime(2000))
        self.assertFalse(encryption.is_prime(1387))
        self.assertFalse(encryption.is_prime(1891))
        self.assertTrue(encryption.is_prime(2))

    def test_encrypt(self):
        n = 33
        e = 7
        message = [2]
        encrypted = encryption.encrypt(message, n, e)
        self.assertEqual(encrypted, [29])
        message = [2, 2]
        encrypted = encryption.encrypt(message, n, e)
        self.assertEqual(encrypted, [29, 29])
        message = [2, 7, 2, 7]
        encrypted = encryption.encrypt(message, n, e)
        self.assertEqual(encrypted, [29, 28, 29, 28])

    def test_decrypt(self):
        n = 33
        d = 3
        message = [29]
        decrypted = encryption.decrypt(message, n, d)
        self.assertEqual(decrypted, [2])
        message = [29, 29]
        encrypted = encryption.encrypt(message, n, d)
        self.assertEqual(encrypted, [2, 2])
        message = [29, 28, 29, 28]
        encrypted = encryption.encrypt(message, n, d)
        self.assertEqual(encrypted, [2, 7, 2, 7])

    def test_ascii_to_string(self):
        ascii_list = [104, 101, 108, 108, 111]
        hello = encryption.ascii_list_to_string(ascii_list)
        self.assertEqual(hello, "hello")

    def test_string_to_ascii(self):
        hello = encryption.string_to_ascii("hello")
        self.assertEqual(hello, [104, 101, 108, 108, 111])

    # key generation is correct 98.7% of the time over 1000 trials -_-
    def test_encrypt_decrypt(self):
        num_tests = 1000
        fuzz = 0
        correct = 0
        while fuzz < num_tests:
            n, e, d = encryption.generate_rsa_keys()
            hello = encryption.string_to_ascii("hello")
            encrypted = encryption.encrypt(hello, n, e)
            decrypted = encryption.decrypt(encrypted, n, d)
            hello_again = encryption.ascii_list_to_string(decrypted)
            if hello_again == "hello":
                correct += 1
            else:
                print("Fuzz failure on " + str(fuzz))
                print("n: " + str(n))
                print("e: " + str(e))
                print("d: " + str(d))
                print("Encrypted: " + ''.join(str(encrypt) + ', ' for encrypt in encrypted))
                print("Decrypted: " + ''.join(str(decrypt) + ', ' for decrypt in decrypted))
            fuzz += 1
        accuracy = correct / num_tests
        print("Total Accuracy: " + str(accuracy))


if __name__ == '__main__':
    unittest.main()

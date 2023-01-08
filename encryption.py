import math
import random

LOW = 233
HIGH = 743
MAX_ED = HIGH ** 2
MIN_E = 284
MIN_D = 284

# for actually decent encryption, LOW would need to be roughly 2^500 and HIGH would need to be roughly 2^512
# considerations for the other variables would also probably be necessary
# padding would also be necessary, and defense against Wiener's attack also necessary

ACCEPTED_CHARACTERS = 'a b  cdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!"#$%&()*+,-./:;<=>?@[\]^_`{|}~'


def is_prime(x):
    if x == 2:
        return True
    for i in range(2, math.ceil(math.sqrt(x))+1):
        if x % i == 0:
            return False
    return True


def key_validation(n, e, d):
    message = ACCEPTED_CHARACTERS
    ascii_message = string_to_ascii(message)
    encrypted = encrypt(ascii_message, n, e)
    decrypted = decrypt(encrypted, n, d)
    returned_message = ascii_list_to_string(decrypted)
    return returned_message == message


def prime_generator():
    primes = []
    # high and low are upper and lower bounds for prime numbers here
    # range is inclusive of the lower bound, but not the upper bound
    for i in range(LOW, HIGH+1):
        prime = True
        # optimized by only checking up to sqrt(i), which is sufficient to guarantee primality
        for j in range(2, math.ceil(math.sqrt(i))+1):
            if i % j == 0:
                prime = False
                break
        if prime:
            primes.append(i)
    return primes


def mod_m_generator(m, max_ed=MAX_ED):
    eds = []
    for ed in range(m+1, max_ed+1):
        if ed % m == 1 and not is_prime(ed):
            eds.append(ed)
    return eds


def ed_factorization(ed):
    factors = []
    for i in range(2, math.ceil(ed/2)+1):
        if ed % i == 0:
            factors.append(i)
    return factors


def generate_rsa_keys():
    eds = []
    n = 0
    e = 0
    d = 0
    key_valid = False
    while (len(eds) < 4) or (n < 1000) or (e < MIN_E) or (d < MIN_D) or not key_valid:
        primes = prime_generator()
        p = random.choice(primes)
        q = random.choice(primes)
        n = p*q
        m = (p-1)*(q-1)
        eds = mod_m_generator(m)
        if len(eds) > 3:
            ed = random.choice(eds)
            ed_factors = ed_factorization(ed)
            e = random.choice(ed_factors)
            d = ed/e
        else:
            ed = 0
            e = 0
            d = 0
        key_valid = key_validation(n, e, int(d))
    return n, e, int(d)


def string_to_ascii(string):
    M = [ord(character) for character in string]
    return M


def encrypt(message, n, e):
    encrypted = [character ** e % n for character in message]
    return encrypted


def decrypt(message, n, d):
    decrypted = [character ** d % n % 255 for character in message]
    return decrypted


def ascii_list_to_string(encrypted):
    mess = ''.join(chr(int(char)) for char in encrypted)
    return mess

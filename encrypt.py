import encryption


def keys(encryption_type):
    if encryption_type == 'rsa':
        return list(encryption.generate_rsa_keys())


def encrypt(message, encryption_type, key_tuple):
    if encryption_type == 'rsa':
        message = encryption.string_to_ascii(message)
        n, e = key_tuple
        return encryption.encrypt(message, n, e)


def decrypt(message, encryption_type, key):
    if encryption_type == 'rsa':
        n, e, d = key
        decrypted = encryption.decrypt(message, n, d)
        return encryption.ascii_list_to_string(decrypted)

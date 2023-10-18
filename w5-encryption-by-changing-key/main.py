def encrypt_by_add_mod(string, key):
    '''
    >>> encrypt_by_add_mod('Hello',123)
    'Ãàççê'
    >>> encrypt_by_add_mod(encrypt_by_add_mod('Hello',123),133)
    'Hello'
    >>> encrypt_by_add_mod(encrypt_by_add_mod('Cryptography',10),246)
    'Cryptography'
    '''
    encryptedStr = []
    for c in string:
        encryptedStr.append(chr((ord(c) + key) % 256))

    return ''.join(encryptedStr)

def encrypt_xor_with_changing_key_by_prev_cipher(string, key, action = 'encrypt'):
    '''
    >>> encrypt_xor_with_changing_key_by_prev_cipher('Hello',123,'encrypt')
    '3V:V9'
    >>> encrypt_xor_with_changing_key_by_prev_cipher(encrypt_xor_with_changing_key_by_prev_cipher('Hello',123,'encrypt'),123,'decrypt')
    'Hello'
    >>> encrypt_xor_with_changing_key_by_prev_cipher(encrypt_xor_with_changing_key_by_prev_cipher('Cryptography',10,'encrypt'),10,'decrypt')
    'Cryptography'
    '''
    processedStr = []

    if action == 'encrypt':
        for c in string:
            key = ord(c) ^ key
            processedStr.append(chr(key))
    elif action == 'decrypt':
        revStr = ''.join(reversed(string))
        for i in range(0, len(string)):
            dec = (key if (i >= (len(string) - 1)) else ord(revStr[1 + i])) ^ ord(revStr[i])
            processedStr.append(chr(dec))
        processedStr = ''.join(reversed(processedStr))
    else:
        return 'Wrong action'

    return ''.join(processedStr)

def do_chunk(string, length):
    chunk = []
    for iKey in range(0, length):
        group = []
        for i in range(0, len(string)):
            if (i % length == iKey):
                group.append(string[i])
        chunk.append(group)
    return chunk

def do_unchunk(string, maxLength):
    output = []
    for c in do_chunk(string, maxLength):
        output += c
    return ''.join(output)

def encrypt_xor_with_changing_key_by_prev_cipher_longer_key(string, key_list, action):
    '''
    >>> key_list = [0x20, 0x44, 0x54,0x20]
    >>> encrypt_xor_with_changing_key_by_prev_cipher_longer_key('abcdefg', key_list, 'encrypt')
    'A&7D$@P'
    >>> encrypt_xor_with_changing_key_by_prev_cipher_longer_key('aaabbbb', key_list, 'encrypt')
    'A%5B#GW'
    >>> encrypt_xor_with_changing_key_by_prev_cipher_longer_key(
    ...    encrypt_xor_with_changing_key_by_prev_cipher_longer_key('abcdefg',key_list,'encrypt'),
    ...        key_list,'decrypt')
    'abcdefg'
    >>> encrypt_xor_with_changing_key_by_prev_cipher_longer_key(
    ...    encrypt_xor_with_changing_key_by_prev_cipher_longer_key('Hellobello, it will work for a long message as well',key_list,'encrypt'),
    ...        key_list,'decrypt')
    'Hellobello, it will work for a long message as well'
    '''

    chunk = do_chunk(string, len(key_list))
    xored = ''.join(
        encrypt_xor_with_changing_key_by_prev_cipher(
            chunk[i],
            key_list[i],
            action
        ) for i in range(0, len(chunk)))
    return do_unchunk(xored, len(chunk[0]))
def filluphex(hexStr):
    leftOver = len(hexStr) % 2
    return ((2 - leftOver) * '0' if leftOver > 0 else '') + hexStr

def hex2string(hexStr):
    '''
    >>> hex2string('61')
    'a'
    >>> hex2string('776f726c64')
    'world'
    >>> hex2string('68656c6c6f')
    'hello'
    '''
    return ''.join(
        chr( # int to ASCII
            int(hexStr[0 + i:2 + i], 16) # hex to int
        )
        for i in range(0, len(hexStr), 2))

def string2hex(str):
    '''
    >>> string2hex('a')
    '61'
    >>> string2hex('hello')
    '68656c6c6f'
    >>> string2hex('world')
    '776f726c64'
    >>> string2hex('foo')
    '666f6f'
    '''
    return ''.join(
        hex( # int to hex
            ord(c) # string to int
        )[2:]  for c in str)

def hex_xor(str1Hex, str2Hex):
    '''
    >>> hex_xor('aabbf11','12345678')
    '189fe969'
    >>> hex_xor('12cc','12cc')
    '0000'
    >>> hex_xor('1234','2345')
    '3171'
    >>> hex_xor('111','248')
    '359'
    >>> hex_xor('8888888','1234567')
    '9abcdef'
    '''
    cStr2Hex = str2Hex
    while (len(str2Hex) < len(str1Hex)):
        str2Hex = str2Hex + cStr2Hex

    return '{1:0{0}x}'.format(
        len(str1Hex),
        int(str1Hex, 16) ^ int(str2Hex, 16)
    )

def encrypt_single_byte_xor(plainHexStr, singleKeyHexStr):
    '''
    >>> encrypt_single_byte_xor('aaabbccc','00')
    'aaabbccc'
    >>> encrypt_single_byte_xor(string2hex('hello'), 'aa')
    'c2cfc6c6c5'
    >>> hex2string(encrypt_single_byte_xor(encrypt_single_byte_xor(string2hex('hello'),'aa'), 'aa'))
    'hello'
    >>> hex2string(encrypt_single_byte_xor(encrypt_single_byte_xor(string2hex('Encrypt and decrypt are the same'),'aa'),'aa'))
    'Encrypt and decrypt are the same'
    '''
    return hex_xor(plainHexStr, singleKeyHexStr)


def isReadable(str, threshold = 90):
    alphaCount = 0
    for c in str.upper():
        # validate words with upper char and space
        if (ord(c) >= 65 and ord(c) <= 90) or ord(c) == 32:
            alphaCount = alphaCount + 1

    return alphaCount / len(str) * 100 > threshold

def decrypt_single_byte_xor(ciphertextHex):
    '''
    >>> decrypt_single_byte_xor('e9c88081f8ced481c9c0d7c481c7ced4cfc581ccc480')
    'Hi! You have found me!'
    >>> decrypt_single_byte_xor('b29e9f96839085849d9085989e9f82d1889e84d199908794d197989f95d1859994d181908282869e8395d0')
    'Congratulations you have find the password!'
    >>> decrypt_single_byte_xor('e1ded996ddd8d9c1c596c1ded7c296dfc596ded7c6c6d3d8dfd8d18996e1ded3c4d396d7db96ff89')
    'Who knows what is happening? Where am I?'
    '''
    # Try all possible keys
    tests = []
    for possibleKey in range(256):
        decryptedStr = hex2string(hex_xor(ciphertextHex, hex(possibleKey)[2:]))

        # filter only english words
        if(all(ord(c) > 31 and ord(c) < 127 for c in decryptedStr) and isReadable(decryptedStr)):
            tests.append(decryptedStr)
            return decryptedStr

    return 'Not Found'
def fillupbyte(binStr):
    leftOver = len(binStr) % 8
    return ((8 - leftOver) * '0' if leftOver > 0 else '') + binStr

def hex2bin(hexStr):
    # binary conversion
    hex_ = int(hexStr.replace(' ', ''), 16)
    binStr = '' + bin(hex_)[2:]
    return fillupbyte(binStr)

def int2base64(intStr):
    std_base64chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    return std_base64chars[intStr]

def bin2hex(binStr):
    # group of 6 bits
    siXlength = 6
    groupOfSix = list(binStr[0 + i:siXlength + i] for i in range(0, len(binStr), siXlength))
    lastGroupLength = siXlength - len(groupOfSix[len(groupOfSix) - 1])
    groupOfSix[len(groupOfSix) - 1] = groupOfSix[len(groupOfSix) - 1] + '0' * lastGroupLength

    # the group to base 64
    base64Str = ''.join(int2base64(int(c, 2)) for c in groupOfSix)
    return base64Str + ('=' * (4 - (len(base64Str) % 4)) if len(base64Str) % 4 > 0 else '')

def hex2base64(hexStr):
    '''
    >>> hex2base64('61')
    'YQ=='
    >>> hex2base64('7368726f6f6d')
    'c2hyb29t'
    >>> hex2base64('123456789abcde')
    'EjRWeJq83g=='
    '''
    binStr = hex2bin(hexStr)
    return bin2hex(binStr)

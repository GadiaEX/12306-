import base64
import chardet
hex16 = r'\xe7\x94\x9f\xe6\x88\x90\xe9\xaa\x8c\xe8\xaf\x81\xe7\xa0\x81\xe6\x88\x90\xe5'
#hex16 = hex16.replace(r'\x', '')

a = chardet.universaldetector.UniversalDetector(hex16)

#hex16 = hex16.encode('raw_unicode_escape').decode('utf-8')
#hex16 = base64.b16decode(hex16.decode())
#hex16 = base64.b16decode(hex16)
print(a)


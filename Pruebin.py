from bitstring import BitArray, BitStream, ConstBitStream

b = BitStream()
b.append('uint:9='+str(10))
print(b.bin)
print(b.int)
# comprimido = open("compri.sg", "wb")
# comprimido.write(b.tobytes())
# comprimido.close()
#
# comprimido = open("compri.sg", "rb")
# lect = BitStream(comprimido.read())
# print(lect.read(1))
# s = ConstBitStream(filename="D:/Users/Guille/Documents/Repositorios/Compresor2019_SimonGui/compri.sg")
# k = s.read('uint:9')
# while s.pos+9 < s.len:
#
#     k = s.read('uint:9')
#     print(chr(k))
#

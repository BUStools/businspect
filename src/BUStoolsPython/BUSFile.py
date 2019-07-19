from .BUSHeader import BUSHeader
from .BUSRecord import BUSRecord
from .byteDecoding import byteDecoding

class BUSFile:
#    bpDecoding = {
#        '00': 'A',
#        '01': 'C',
#        '10': 'G',
#        '11': 'T'
#        }
    bpDefault = 'x'

    def __init__(self):
        self.f = None

    def __init__(self, fileName, mode = 'r'):
        self.open(fileName, mode)

    def open(self, fileName, mode = 'r'):
        self.f = open(fileName, mode + 'b')

    def close(self):
        self.f.close()

    def flush(self):
        self.f.flush()

    def fileno(self):
        return self.f.fileno()

    def isatty(self):
        return self.f.isatty()

    def readable(self):
        return self.f.readable()

    def readheader(self):
        prefix = self.f.read1(BUSHeader.preSize)

        assert (prefix == bytearray(b'BUS\x00')), 'File is not a BUS file'

        ver = int.from_bytes(self.f.read1(BUSHeader.verSize), byteorder='little')
        bclen = int.from_bytes(self.f.read1(BUSHeader.bclenSize), byteorder='little')
        umilen = int.from_bytes(self.f.read1(BUSHeader.umilenSize), byteorder='little')
        tlen = int.from_bytes(self.f.read1(BUSHeader.tlenSize), byteorder='little')
        text = self.f.read1(tlen).decode()

        head = BUSHeader()
        head.ver = ver
        head.bclen = bclen
        head.umilen = umilen
        head.text = text

        self.bclen = bclen
        self.umilen = umilen
        self.bcbytelen = int(bclen / 4 + 0.5)
        self.umibytelen = int(umilen / 4 + 0.5)

        return head

    def readline(self):
        bc = list(self.f.read1(BUSRecord.bcSize))[::-1]
        umi = list(self.f.read1(BUSRecord.umiSize))[::-1]
        ec = int.from_bytes(self.f.read1(BUSRecord.ecSize), byteorder='little', signed=True)
        count = int.from_bytes(self.f.read1(BUSRecord.countSize), byteorder='little', signed=True)
        flags = int.from_bytes(self.f.read1(BUSRecord.flagsSize), byteorder='little')
        pad = self.f.read1(BUSRecord.padSize)

        if len(bc) == 0:
            return None

        rec = BUSRecord()
        rec.bc = ''.join(byteDecoding[byte] for byte in bc[-self.bcbytelen:])[-self.bclen:]
        rec.umi = ''.join(byteDecoding[byte] for byte in umi[-self.umibytelen:])[-self.umilen:]
        rec.ec = ec
        rec.count = count

        return rec

    def __strByteArray(b):
        b = [format(elt, 'b') for elt in list(b)]
        b = ['0' * (8 - len(elt)) + elt[-len(elt):] for elt in b]
        b = [[elt[i:i+2] for i in range(0, len(elt), 2)] for elt in b]
        b = [i for j in b for i in j[::-1]][::-1]
        return b

    def __iter__(self):
        return self

    def __next__(self):
        l = self.readline()
        if (l == None):
            raise StopIteration
        return l


if __name__ == '__main__':
    f = BUSFile('/home/leliu/bustools/test/output.sorted.bus')
    h = f.readheader()
    x = 0
    for rec in f:
        ++x
#    for i in range(10):
#        l = f.readline()
#        print(l)

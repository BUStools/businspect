class BUSHeader:
    preSize = 4
    verSize = 4
    bclenSize = 4
    umilenSize = 4
    tlenSize = 4

    def __init__(self):
        self.ver = ''
        self.bclen = -1
        self.umilen = -1
        self.text = ''

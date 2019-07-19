class BUSRecord:
    bcSize = 8
    umiSize = 8
    ecSize = 4
    countSize = 4
    flagsSize = 4
    padSize = 4

    def __init__(self):
        self.bc = ''
        self.umi = ''
        self.ec = -1
        self.count = 0
        self.flags = 0

    def __str__(self):
        return '{}, {}, {}, {}'.format(
            self.bc,
            self.umi,
            self.ec,
            self.count
            )



class Flood:
    """

    Flood implmeents regular flooding, to return the offsets along a
    square whose side-length is a function of the step-size

    """

    def __init__(self):
        self.step = 0

    def getOffsets(self, step):
        offsets = []
        for x in range(-1 * step, step):
            offsets.append( [x, step] )
            offsets.append( [x, -step] )
        for y in range(-1 * step + 1, step - 1):
            offsets.append( [step, y] )
            offsets.append( [-step, y] )
        return offsets

    def nextStep(self):
        self.step += 1
        offsets = self.getOffsets(self.step);
        return offsets

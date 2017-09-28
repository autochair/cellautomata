
class JFA:
    """

    JFA implements the jump-flood algorithm and should provide a
    selection of jump offsets for a given index in a two-dimensional
    array given the current step and the max side-length of the array

    """

    # static class variables
    unit_offsets = (
        (-1,1),
        (0,1),
        (1,1),
        (1,0),
        (1,-1),
        (0,-1),
        (-1,-1),
        (-1,0))

    def __init__(self, N):
        # should calculate N from log2(sidelength) instead 
        self.N = n
        self.step = 0

    def getOffsets(self, base):
        offsets = []
        if (base > 0):
            offsets = [[x*base,y*base] for (x,y) in unit_offsets]
        return offsets

    def nextStep(self):
        offsets = []
        if (self.step < self.N):
            self.step += 1
            base = pow(2, self.N - self.step)
            offsets = self.getOffsets(base);
        return offsets

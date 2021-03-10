class FreightCalculator:
    def __init__(self, durian):
        self.durian = durian

    def calculate(self):
        if self.durian == 0:
            return 0
        else:
            if self.durian == 1:
                return 30
            else:
                return 30 * (self.durian - 1)

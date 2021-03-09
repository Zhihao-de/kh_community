class CreditCalculator():
    def __int__(self, details):
        self.details = details
        self.durian_weight = 0
        self.nest_weight = 0
        self.credits = 0

    def calculate(self):
        """
        计算一个订单的积分
        """
        for detail in self.details:
            if detail.category in []:
                self.durian_weight = detail.weight
            else:
                self.nest_weight = detail.weight

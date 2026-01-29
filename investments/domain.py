class PaymentResult:
    pass


class PaymentSuccess(PaymentResult):
    def __init__(self, investment):
        self.investment = investment


class ExpiredInvestment(PaymentResult):
    pass


class CapacityExceeded(PaymentResult):
    pass

import numpy as np
from models.black_scholes import BlackScholes
from tools.static_def import PayoffType
from products.option import Option
from models.black import Black


class OptionOnFutures(Option):

    def model(self):
        return Black(self.T, self.S, self.K, self.r, self.sigma, self.payout)


if __name__ == "__main__":
    call_option = OptionOnFutures(100, 100, 2, 0.01, 0.2, PayoffType.PUT)
    print(call_option.model().delta())
    print(call_option.payout)
    call_option.plot()

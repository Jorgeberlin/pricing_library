from hesperides.contracts.european_option import EuropeanOption
from hesperides.models.binomial_model import BinomialModel
from hesperides.engines.binomial_engine import BinomialEngine


class BinomialPricer:

    @staticmethod
    def price(
        contract: EuropeanOption,
        model: BinomialModel,
    ) -> float:

        return BinomialEngine.price(
            strike=contract.strike,
            maturity=contract.maturity,
            is_call=contract.is_call,
            spot=model.spot,
            rate=model.rate,
            up=model.up,
            down=model.down

        )




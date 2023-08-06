""" The main module """
from decimal import Decimal
from typing import List
import logging
from enum import Enum, auto

from pricedb import PriceModel


class DownloadSources(Enum):
    """ Available sources for price download """
    alphavantage = auto(),
    fixerio = auto(),
    boerse_frankfurt = auto(),
    morningstar = auto(),
    morningstar_de = auto(),
    reuters = auto(),
    vanguard_au = auto(),
    yahoo_finance = auto()


class Quote:
    """ The main application object. 
    Select the downloading source first q.set_source(<name>)
    then call q.fetch("ASX", "VAS").
    The list of sources is available through q.sources property.
    """
    symbol = None
    exchange = None
    source = None
    _currency = None

    """ The main application object """
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def fetch(self, exchange: str, symbols: List[str]):
        """ The main method to fetch prices.
        exchange = the name of the exchange, commodity *namespace* in GnuCash;
        symbols = the list of symbols (just the company ticker!) to fetch;
        """
        assert isinstance(exchange, str)
        #assert isinstance(symbols, List[str])
        #assert symbols

        if not symbols:
            raise ValueError("The symbols are missing.")
        
        # fetch the prices using the given module.
        result = []
        for symbol in symbols:
            price = self.__download(exchange, symbol, self._currency, self.source)
            if price:
                result.append(price)

        return result

    def currency(self, source: str, destination: str) -> PriceModel:
        """ Fetches the currency exchange rate of the 1st currency in 2nd.
        i.e. currency("AUD", "EUR") will return the rate for AUD in Euros. (0.71)
        """
        source = source.upper()
        destination = destination.upper()

        # the default currency rate provider
        default_provider = "Fixerio"

        result = self.__download("CURRENCY", source, destination, default_provider)

        return result

    @property
    def sources(self) -> List[str]:
        """ Available sources for prices """
        result = []
        for source in DownloadSources:
            result.append(source.name)
        return result

    def set_currency(self, currency: str):
        """ Sets the output currency """
        assert currency

        self._currency = currency.upper()

    def set_source(self, source: str):
        """ Set the download source to use to fetch the prices. """
        self.source = source.lower()

    def __download(self, exchange: str, symbol: str, currency: str = None, source: str = None):
        """ Download single latest price """
        from pricedb import SecuritySymbol
        from .alphavantage import AlphaVantageDownloader
        from .morningstar import MorningstarDownloader
        from .morningstar_de import MorningstarDeDownloader
        from .vanguard_au import VanguardAuDownloader
        from .boerse_frankfurt import FwbDownloader
        from .yahoo_finance import YahooFinanceDownloader
        from .fixerio import Fixerio
        from .reuters import Reuters

        assert source is not None
        assert isinstance(source, str)

        if exchange:
            exchange = exchange.upper()
        symbol = symbol.upper()
        if currency:
            currency = currency.upper()
        source = source.lower()
        actor = None
        price = None

        security_symbol = SecuritySymbol("", "")
        security_symbol.parse(symbol)
        if not security_symbol.namespace:
            security_symbol.namespace = exchange

        # todo: read import modules dynamically?

        if source == DownloadSources.morningstar.name:
            actor = MorningstarDownloader()
        elif source == DownloadSources.morningstar_de.name:
            actor = MorningstarDeDownloader()
        elif source == DownloadSources.vanguard_au.name:
            actor = VanguardAuDownloader()
        elif source == DownloadSources.alphavantage.name:
            actor = AlphaVantageDownloader()
        elif source == DownloadSources.fixerio.name:
            actor = Fixerio()
        elif source == DownloadSources.boerse_frankfurt.name:
            actor = FwbDownloader()
        elif source == DownloadSources.reuters.name:
            actor = Reuters()
        elif source == DownloadSources.yahoo_finance.name:
            actor = YahooFinanceDownloader()
        else:
            raise ValueError("No source specified for price download.")

        if actor:
            actor.logger = self.logger
            try:
                price = actor.download(security_symbol, currency)
            except AttributeError as e:
                self.logger.error(str(e))

        return price

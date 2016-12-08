from easyctp.pipeline import FilterInvalidItem, SaveInflux
from easyctp.quotation import MarketDataApi
from easyctp.trader import EasyTrader


class MarketDataFacade:
    @classmethod
    def to_influx(cls, user, password, broker, front, instrument_ids, influxdb_uri, worker=10, trade_front=None):
        if instrument_ids == 'all':
            trader = EasyTrader()
            trader.login(user=user, password=password, broker=broker,
                         front=trade_front)
            instrument_ids = trader.query_all_instruments()

        md = MarketDataApi()
        market_data = md.prepare(user=user, password=password, broker=broker,
                                 front=front,
                                 instrument_ids=instrument_ids)

        pipe = SaveInflux(
            FilterInvalidItem(market_data), worker=worker, host=influxdb_uri)
        pipe.start()

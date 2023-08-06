import unittest

import betfairlightweight
from betfairlightweight import StreamListener


class HistoricalStreamTest(unittest.TestCase):
    def test_historical_stream(self):
        trading = betfairlightweight.APIClient("username", "password", app_key="appKey")
        stream = trading.streaming.create_historical_stream(
            file_path="tests/resources/historicaldata/BASIC-1.132153978",
            listener=StreamListener(),
        )
        stream.start()

        assert stream.listener.stream_type == "marketSubscription"
        assert stream.listener.stream_unique_id == 0
        assert stream.listener.clk == "3522512789"

        assert stream.listener.stream._updates_processed == 480
        assert len(stream.listener.stream._caches) == 1

        market = stream.listener.stream._caches.get("1.132153978")
        assert len(market.runners) == 14
        assert stream._running is False


class HistoricalRaceStreamTest(unittest.TestCase):
    def test_historical_stream(self):
        trading = betfairlightweight.APIClient("username", "password", app_key="appKey")
        stream = trading.streaming.create_historical_stream(
            file_path="tests/resources/historicaldata/RACE-1.140075353",
            listener=StreamListener(),
            operation="raceSubscription",
        )
        stream.start()

        for cache in stream.listener.stream._caches.values():
            cache.create_resource(1, False)

        assert stream.listener.stream_type == "raceSubscription"
        assert stream.listener.stream_unique_id == 0

        assert stream.listener.stream._updates_processed == 4
        assert len(stream.listener.stream._caches) == 2

        market = stream.listener.stream._caches.get("1.1234567")
        assert len(market.rrc) == 2

        market = stream.listener.stream._caches.get("1.173853449")
        assert len(market.rrc) == 4

        assert stream._running is False

from datetime import datetime
from zoneinfo import ZoneInfo
import time
import json
import scrapy
from scrapy.http import TextResponse
from mibus.items import BusArrival


class BusinfoSpider(scrapy.Spider):
    name = "businfo"
    allowed_domains = ["bis.mibus.com.pa", "bisapi.mibus.com.pa"]
    start_urls = ["http://bis.mibus.com.pa/"]

    def __init__(self, name=None, bus_stops='["ESTVARA"]', **kwargs):
        super().__init__(name, **kwargs)
        if bus_stops:
            self.bus_stops: list[str] = json.loads(bus_stops)

    def parse(self, response: TextResponse):
        for bus_stop in self.bus_stops:
            yield response.follow(
                "https://bisapi.mibus.com.pa/api/getArrive.bis?stopCd=" + bus_stop,
                self.parse_bus_arrival,
            )

    def parse_bus_arrival(self, response: TextResponse):
        d: bytes = response.headers["Date"]
        request_time = datetime.strptime(
            d.decode("utf8"), "%a, %d %b %Y %H:%M:%S %Z"
        ).replace(tzinfo=ZoneInfo("GMT"))
        arrival_info = response.json()
        if arrival_info["result"]["code"] == "000001":
            return

        stop_id = arrival_info["body"]["stopCd"]
        request_time = request_time.astimezone(ZoneInfo("America/Panama"))
        for bus in arrival_info["body"]["list"]:
            item = BusArrival(
                request_time,
                stop_id,
                bus["rtId"],
                bus["fstVehId"],
                bus["fstSn"],
                bus["fstTraTime"],
                bus["secndVehId"],
                bus["secndSn"],
                bus["secndTraTime"],
            )

            yield item

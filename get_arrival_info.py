import json
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from mibus.spiders.businfo import BusinfoSpider

if __name__ == "__main__":
    with open("unique_paradas.json", "r", encoding="utf8") as f:
        unique_paradas = json.load(f)
        parada_ids = [parada["id_code"] for parada in unique_paradas]

    settings = get_project_settings()
    process = CrawlerProcess(settings=settings)
    process.crawl(BusinfoSpider, bus_stops=json.dumps(parada_ids))
    process.start()

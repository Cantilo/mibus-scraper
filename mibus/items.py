# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass
from typing import Optional, Tuple, List
import scrapy


class MibusItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


@dataclass
class Parada:
    coordinates: Tuple[float, float]
    parada_nomb: str
    id_code: str


@dataclass
class Ruta:
    id_code: str
    nomb: str


@dataclass
class Recorrido:
    route_id: str
    ruta: List[Tuple[float, float]]

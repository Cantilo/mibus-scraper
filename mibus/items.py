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
    route_id: str
    parada_index: int


@dataclass
class Ruta:
    id_code: str
    nomb: str


@dataclass
class Recorrido:
    route_id: str
    ruta: List[Tuple[float, float]]
    horario: str


@dataclass
class BusArrival:
    scraped_time: int
    stop_id: str
    ruta_id: str
    first_vehicle_id: int
    first_sn: int
    first_travel_time: int
    second_vehicle_id: int
    second_sn: int
    second_travel_time: int

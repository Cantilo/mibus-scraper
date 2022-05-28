# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pydispatch import dispatcher
from scrapy import signals
from scrapy.exporters import JsonItemExporter
from mibus.items import Parada, Recorrido


class MibusPipeline:
    files = {}
    exporters = {}
    destinations = {
        Parada.__name__: "paradas",
        Recorrido.__name__: "recorridos",
        dict.__name__: "info_rutas",
    }

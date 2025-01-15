from ast import literal_eval
import re
import base64
import chompjs
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.http import TextResponse

from mibus.items import Recorrido, Parada

ENCODED_PARADA_OFFSET = 10


class RutasSpider(scrapy.Spider):
    name = "rutas"
    allowed_domains = ["mibus.com.pa"]
    start_urls = ["https://www.mibus.com.pa/red-de-rutas/"]

    routes_js = LinkExtractor(r"routes.js", tags="script", attrs="src")
    re.compile(r"var (circle_marker_\w+) = L.circleMarker\(\n\s+[\[\]\d\.,\-\s]+")
    info_parada = re.compile(r"base64,([^\"]*)")

    def parse(self, response: TextResponse):
        # Follows the url to the routes.js file
        yield response.follow(
            self.routes_js.extract_links(response).pop(), self.parse_routes
        )

    def parse_routes(self, response: TextResponse):
        rutas = chompjs.parse_js_object(response.text)

        for route_info in rutas:
            route_id = route_info["route_id"]
            url = f"https://www.mibus.com.pa/wp-content/uploads/web-maps/htmls/{route_id}.html"
            yield response.follow(
                url,
                self.parse_page_for_route,
                cb_kwargs={
                    "route_id": route_id,
                    "route_name": route_info["route_long_name"],
                    "axis": route_info["axis"],
                    "route_type": route_info["type"],
                    "color": route_info["route_color"],
                },
            )
            yield route_info

    def parse_page_for_route(
        self,
        response: TextResponse,
        route_id: str,
        route_name: str,
        axis: str,
        route_type: str,
        color: str,
    ):
        # Need to get the bus route
        # Need to get the coordinates as well as the stop info
        code_lines = response.text.splitlines()
        enum_lines = enumerate(response.text.splitlines())
        maplegend = re.compile(r"<div.class=.legend-horario.>([^<]+)")
        parada_index = 1
        for i, line in enum_lines:
            if "var circle_marker_" in line:
                coords = literal_eval(code_lines[i + 1].strip()[:-1])

                encoded_content = self.info_parada.search(
                    code_lines[i + ENCODED_PARADA_OFFSET]
                )
                content = base64.decodebytes(encoded_content[1].encode("utf8"))
                r2 = response.replace(body=content)
                parada, id_code = r2.xpath(".//div/text()").getall()

                yield Parada(
                    parada_nomb=parada,
                    id_code=id_code,
                    coordinates=coords,
                    route_id=route_id,
                    parada_index=parada_index,
                )
                parada_index += 1
            elif "ant_path_" in line and "antPath" in line:
                ruta = code_lines[i + 1][:-1].strip()

            elif horario_legend := maplegend.match(line.strip()):
                horario = horario_legend[1]

        yield Recorrido(
            route_id,
            literal_eval(ruta),
            horario,
            route_type,
            color,
            axis,
            route_name,
        )

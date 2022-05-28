from ast import literal_eval
import re
import base64
import chompjs
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.http import TextResponse

from mibus.items import Recorrido, Parada


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
                url, self.parse_page_for_route, cb_kwargs={"route_id": route_id}
            )
            yield route_info

    def parse_page_for_route(self, response: TextResponse, route_id: str):
        # Need to get the bus route
        # Need to get the coordinates as well as the stop info
        code_lines = response.text.splitlines()
        for i, line in enumerate(code_lines):
            if "var circle_marker_" in line:
                coords = literal_eval(code_lines[i + 1].strip()[:-1])

                encoded_content = self.info_parada.search(code_lines[i + 9])
                content = base64.decodebytes(encoded_content[1].encode("utf8"))
                r2 = response.replace(body=content)
                parada, id_code = r2.xpath(".//div/text()").getall()

                yield Parada(parada_nomb=parada, id_code=id_code, coordinates=coords)
            elif "ant_path_" in line and "antPath" in line:
                ruta = code_lines[i + 1][:-1].strip()

                yield Recorrido(route_id, literal_eval(ruta))

import time
from urllib.parse import urlencode
import requests
import requests.cookies
from requests import Response
from lib.console import Console
from sqlite3 import Connection
from bs4 import BeautifulSoup

from lib.types import DisplayGallery, Gallery
from dataclasses import dataclass
from typing import Callable

from enum import Enum


class ScrollDirection(Enum):
    VERTICAL = 1
    HORIZONTAL = 2


@dataclass
class QuickFilter:
    icon: str
    label: str
    callback: Callable[..., list[DisplayGallery]]


class Extension:
    def __init__(
        self,
        handle: str,
        domain: str,
        cache_duration: int,
        base_url: str,
        logo: str,
        con: Connection,
        headers: dict[str, str],
        tag_categories: list[str] = [],
        quick_filters: dict[str, QuickFilter] = {},
        image_proxy_headers: dict = {},
        scroll_direction: ScrollDirection = ScrollDirection.HORIZONTAL
    ):
        self.handle = handle
        self.domain = domain
        self.cache_duration = cache_duration
        self.base_url = base_url
        self.logo = logo
        self.con = con
        self.cur = con.cursor()
        self._init_time = int(time.time())
        self._cache: dict[str, list[Gallery]] = {}
        self._session = requests.session()
        self.tag_categories: list[str] = tag_categories
        self.quick_filters: dict[str, QuickFilter] = quick_filters
        self.image_proxy_headers: dict = image_proxy_headers
        self.scroll_direction = scroll_direction

        for k, v in headers.items():
            self._session.headers.update({k: v})

        self.loadCookies(self.base_url)

    def loadCookies(self, url: str, additional=False):
        res = self.cur.execute(
            "SELECT key,value FROM cookies WHERE handle = ?", (self.handle,)
        )
        rows: list[tuple[str]] = res.fetchall()
        if len(rows) == 0 or additional:
            req = self._session.request(method="HEAD", url=url)
            if req.status_code != 200:
                Console.Error(
                    "Could not make initial HEAD request to base url", url
                )
            else:
                Console.Log("Successful request to base url", url)
                Console.Log("Persisting cookies in database for", self.handle)

                self.cur.executemany(
                    "INSERT INTO cookies VALUES(?,?,?)",
                    [(self.handle, x[0], x[1]) for x in req.cookies.items()],
                )
                self.con.commit()
        else:
            Console.Log(
                "Found cookies for '{}' in database".format(self.handle))
            cookies = {}
            for row in rows:
                cookies.update({row[0]: row[1]})
                requests.utils.add_dict_to_cookiejar(
                    self._session.cookies, cookies)

    def makeRequest(self, method: str, url: str, params: dict[str, str] = None) -> Response:
        res = self._session.request(method=method, url=url, params=params)
        return res

    def fetchGallery(self, id: str) -> Gallery:
        raise NotImplementedError("Subclasses must override fetchGallery.")

    def search() -> list[DisplayGallery]:
        pass

    def searchUi():
        pass

    def addQuickFilter(self, name: str, filter: QuickFilter):
        self.quick_filters.update({name: filter})

    def getSoup(self, path: str, method="GET") -> BeautifulSoup:
        # TODO
        #o = open("test/wt.html").read()
        #return BeautifulSoup(o, "html.parser")

        path = path if path[0] == "/" else "/"+path
        url = "{}{}".format(self.base_url, path)
        res = self._session.request(method=method, url=url)
        if res.status_code == 200:
            return BeautifulSoup(res.text, "html.parser")
        else:
            Console.Error("could not fetch", url)
            return None

    def getProxyImage(self, url: str):
        return "/img/proxy?{}".format(urlencode({"ext_handle": self.handle, "url": url}))

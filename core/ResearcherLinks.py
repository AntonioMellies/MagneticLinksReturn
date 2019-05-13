import re
import requests

from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from core.models.ObjReturn import ObjReturn

from collections import defaultdict


class ResearcherLinks:

    def __init__(self, url, depthLayers):
        self.url = url
        self.depthLayers = int(depthLayers)
        self.retObjs = set()
        self.pages_invalid = set()
        self.pages = set()
        self.magnet_liks = set()
        self.bsObj = None

    def searchLinks(self, url=None, current_layer=1):
        new_page = ""

        # Força pagina inicial
        if url is None:
            url = self.url

        try:
            if url not in self.pages_invalid:

                if self.depthLayers == 1:
                    # ------------------------
                    req = Request(url)
                    req.add_header('User-Agent', 'Mozilla/5.0')
                    html = urlopen(req)

                    self.bsObj = BeautifulSoup(html, "html.parser")
                    # print(current_layer, " - ", url)
                    # ------------------------

                    # Extraio links magneticos da pagina atual
                    self.get_magnet_liks()

                elif self.depthLayers > 1 and current_layer <= self.depthLayers:
                    # ------------------------ofer
                    req = Request(url)
                    req.add_header('User-Agent', 'Mozilla/5.0')
                    html = urlopen(req)

                    self.bsObj = BeautifulSoup(html, "html.parser")
                    # print(current_layer, " - ", url)
                    # ------------------------

                    # Extraio links magneticos da pagina atual
                    self.get_magnet_liks()

                    re_links = ('[.http: | .https:]')

                    for link in self.bsObj.findAll("a", href=re.compile(re_links)):
                        if "href" in link.attrs:
                            if link.attrs['href'] not in self.pages and link.attrs['href'] not in self.pages_invalid:
                                new_page = link.attrs['href']
                                self.pages.add(new_page)
                                self.searchLinks(new_page, current_layer=current_layer + 1)
            return self.retObjs
        except:
            self.pages_invalid.add(new_page)

    def get_magnet_liks(self):
        re_magnet = ('magnet{1}:\?xt=urn:btih:[a-zA-Z0-9&=%.-]*')
        for link in self.bsObj.findAll("a", href=re.compile(re_magnet)):
            link_magnet = link.attrs['href']
            if link_magnet not in self.magnet_liks:
                self.magnet_liks.add(link_magnet)
                self.get_info_magnet_link(link_magnet)

    def get_info_magnet_link(self,magnet_uri):

        # New object return
        objReturn = ObjReturn()

        # Set Link
        objReturn.set_link(magnet_uri)

        data = defaultdict(list)
        if not magnet_uri.startswith('magnet:'):
            return data
        else:
            magnet_uri = magnet_uri.strip('magnet:?')
            for segment in magnet_uri.split('&'):
                key, value = segment.split('=')
                if key == 'dn':
                    data['name'] = requests.utils.unquote(value).replace('+', '.')
                    name = requests.utils.unquote(value).replace('+', '.')
                    # Set name
                    objReturn.set_name(name)

                elif key == 'xt':
                    data['infoHash'] = value.strip('urn:btih:')
                    infoHash = value.strip('urn:btih:')
                    # Set infoHash
                    objReturn.set_infoHash(infoHash)

                elif key == 'tr':
                    data['trackers'].append(requests.utils.unquote(value))
                    trackers = requests.utils.unquote(value)
                    # Set trackers
                    objReturn.add_trackers(trackers)

                else:
                    data[key] = value

        # print(objReturn.trackers)
        self.retObjs.add(objReturn)
        return

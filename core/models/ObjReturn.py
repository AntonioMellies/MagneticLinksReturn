from typing import Any


class ObjReturn(object):

    def __init__(self):
        self.link = ""
        self.name = ""
        self.infoHash = ""
        self.trackers = set()

    def set_link(self,link):
        self.link = link

    def set_name(self,name):
        self.name = name

    def set_infoHash(self,infoHash):
        self.infoHash = infoHash

    def set_trackers(self,trackers):
        self.trackers = trackers

    def add_trackers(self,trackers):
        self.trackers.add(trackers)

